const { useState, useRef, useEffect } = window.React;

// Recording stays local until Stop. Server audio is temporary; answers are reviewed before submission.
export function usePanelVoice(panelId, questionNumber, onTranscript, onError) {
  const [phase, setPhase] = useState("idle");
  const [seconds, setSeconds] = useState(0);
  const recorderRef = useRef(null);
  const controllerRef = useRef(null);
  const timerRef = useRef(null);
  const versionRef = useRef(0);
  const activeRef = useRef(false);

  function cancel() {
    versionRef.current++;
    activeRef.current = false;
    clearInterval(timerRef.current);
    controllerRef.current?.abort();
    const recorder = recorderRef.current;
    if (recorder) {
      recorder.onstop = null;
      recorder.onerror = null;
      try { if (recorder.state !== "inactive") recorder.stop(); }
      finally { recorder.stream.getTracks().forEach(track => track.stop()); }
    }
    recorderRef.current = null;
  }

  useEffect(() => {
    setPhase("idle");
    setSeconds(0);
    return cancel;
  }, [panelId, questionNumber]);

  function stop() {
    clearInterval(timerRef.current);
    const recorder = recorderRef.current;
    if (recorder?.state === "recording") {
      setPhase("transcribing");
      recorder.stop();
    }
  }

  async function start() {
    if (activeRef.current) return;
    activeRef.current = true;
    const version = ++versionRef.current;
    setPhase("requesting");
    let stream;
    try {
      if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error("Voice recording is unavailable in this browser. You can type your answer.");
      window.speechSynthesis?.cancel();
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (version !== versionRef.current) { stream.getTracks().forEach(track => track.stop()); return; }
      const mime = ["audio/webm", "audio/mp4", "audio/ogg"].find(type => MediaRecorder.isTypeSupported?.(type));
      const recorder = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
      recorderRef.current = recorder;
      const chunks = [];
      recorder.ondataavailable = event => { if (event.data.size) chunks.push(event.data); };
      recorder.onerror = () => {
        cancel();
        setPhase("idle");
        onError("Recording failed. Retry or type your answer.");
      };
      recorder.onstop = async () => {
        clearInterval(timerRef.current);
        stream.getTracks().forEach(track => track.stop());
        if (version !== versionRef.current) return;
        setPhase("transcribing");
        const actualMime = recorder.mimeType || mime || "audio/webm";
        const extension = actualMime.includes("mp4") ? "mp4" : actualMime.includes("ogg") ? "ogg" : "webm";
        const blob = new Blob(chunks, { type: actualMime });
        const controller = new AbortController();
        controllerRef.current = controller;
        const timeout = setTimeout(() => controller.abort(), 180000);
        try {
          if (!blob.size) throw new Error("Recording was empty. Please try again.");
          const body = new FormData();
          body.append("audio", blob, `answer.${extension}`);
          body.append("question_number", questionNumber);
          const response = await fetch(`/api/panels/${panelId}/transcribe`, { method: "POST", body, signal: controller.signal });
          if (response.status === 413) throw new Error("Recording is too large. Please record a shorter answer.");
          const result = await response.json();
          if (!response.ok || !result.ok) throw new Error(result.message || "Transcription failed.");
          if (version === versionRef.current) onTranscript(result.transcript);
        } catch (error) {
          if (version === versionRef.current) onError(error.name === "AbortError" ? "Transcription timed out. Retry or type your answer." : error.message);
        } finally {
          clearTimeout(timeout);
          if (version === versionRef.current) { activeRef.current = false; setPhase("idle"); }
        }
      };
      recorder.start(500);
      setSeconds(0);
      setPhase("recording");
      let elapsed = 0;
      timerRef.current = setInterval(() => {
        elapsed++;
        setSeconds(elapsed);
        if (elapsed >= 120) stop();
      }, 1000);
    } catch (error) {
      stream?.getTracks().forEach(track => track.stop());
      if (version === versionRef.current) {
        activeRef.current = false;
        setPhase("idle");
        onError(error.name === "NotAllowedError" ? "Microphone permission was denied. You can type your answer or enable the microphone and retry." : error.message);
      }
    }
  }

  return { phase, seconds, start, stop };
}
