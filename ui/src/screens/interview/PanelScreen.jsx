const React = window.React;
const { useEffect, useRef, useState } = React;
import { apiRequest } from "../../api/client.js";
import { usePanelVoice } from "../../hooks/usePanelVoice.js";
import { Icon } from "../../components/Icon.jsx";

export function PanelScreen({ onSetup, isGuest }) {
  const [lobby, setLobby] = useState(null);
  const [session, setSession] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [draft, setDraft] = useState("");
  const [heard, setHeard] = useState("");
  const [unsent, setUnsent] = useState("");
  const [speaking, setSpeaking] = useState(false);
  const alive = useRef(true);
  const busyRef = useRef(false);
  const startToken = useRef(null);
  const voice = usePanelVoice(session?.id, session?.current?.number, setHeard, setError);
  const voiceBusy = voice.phase !== "idle";
  const personas = lobby?.personas || [];
  const personaName = id => personas.find(persona => persona.id === id)?.name || id;

  useEffect(() => {
    alive.current = true;
    loadLobby();
    return () => { alive.current = false; window.speechSynthesis?.cancel(); };
  }, []);

  useEffect(() => {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
    setHeard("");
  }, [session?.id, session?.current?.number]);

  async function loadLobby() {
    const result = await apiRequest("/api/panels");
    if (!alive.current) return;
    if (result.ok) setLobby(result);
    else setError(result.message);
  }

  async function advance(state) {
    if (state.status === "completed" || state.current) return;
    const result = await apiRequest(`/api/panels/${state.id}/advance`, {});
    if (!alive.current) return;
    if (result.session) setSession(result.session);
    if (!result.ok) setError(result.message);
  }

  async function perform(action) {
    if (busyRef.current || voiceBusy) return;
    busyRef.current = true;
    setBusy(true);
    setError("");
    window.speechSynthesis?.cancel();
    setSpeaking(false);
    try { await action(); }
    catch { if (alive.current) setError("Something went wrong. Reopen your saved panel to continue."); }
    finally { busyRef.current = false; if (alive.current) setBusy(false); }
  }

  function start() {
    perform(async () => {
      startToken.current ||= crypto.randomUUID();
      const result = await apiRequest("/api/panels/start", { request_id: startToken.current });
      if (!alive.current) return;
      if (!result.ok) { setError(result.message); return; }
      startToken.current = null;
      setSession(result.session);
      setDraft("");
      setUnsent("");
      await advance(result.session);
    });
  }

  function open(id) {
    perform(async () => {
      const result = await apiRequest(`/api/panels/${id}`);
      if (!alive.current) return;
      if (!result.ok) { setError(result.message); return; }
      setSession(result.session);
      setDraft("");
      setUnsent("");
      await advance(result.session);
    });
  }

  function submit(event) {
    event.preventDefault();
    if (!draft.trim() || !session.current) return;
    perform(async () => {
      const result = await apiRequest(`/api/panels/${session.id}/answer`, { question_number: session.current.number, answer: draft });
      if (!alive.current) return;
      if (result.session) setSession(result.session);
      if (!result.ok) {
        if (result.session && result.session.current?.number !== session.current.number) {
          setUnsent(draft);
          setDraft("");
        }
        setError(result.message);
        return;
      }
      setDraft("");
      setHeard("");
      await advance(result.session);
    });
  }

  function finish() {
    perform(async () => {
      const result = await apiRequest(`/api/panels/${session.id}/finish`, {});
      if (!alive.current) return;
      if (result.session) setSession(result.session);
      if (!result.ok) { setError(result.message); return; }
      setDraft("");
      await advance(result.session);
    });
  }

  function speak() {
    if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) { setError("Read-aloud is unavailable in this browser. The question is shown below."); return; }
    window.speechSynthesis.cancel();
    if (speaking) { setSpeaking(false); return; }
    const speech = new SpeechSynthesisUtterance(session.current.question);
    speech.lang = "en-US";
    speech.onend = () => { if (alive.current) setSpeaking(false); };
    speech.onerror = event => {
      if (!alive.current) return;
      setSpeaking(false);
      if (!["canceled", "interrupted"].includes(event.error)) setError("Question audio could not play. You can read the question and continue.");
    };
    setSpeaking(true);
    window.speechSynthesis.speak(speech);
  }

  const active = session?.current;
  return <main className="wrap panel-page">
    <div className="panel-heading"><div><span className="eyebrow">THE INTERVIEW ROOM</span><h1>{session ? session.profile.target_role : "A real conversation. More perspectives."}</h1><p className="muted">Practice telling your story—with questions built around you.</p></div>
      {session && <button className="btn btn-secondary" disabled={busy || voiceBusy} onClick={() => { window.speechSynthesis?.cancel(); setSpeaking(false); setSession(null); setDraft(""); setError(""); loadLobby(); }}>Back to panel sessions</button>}
    </div>
    {error && <p className="formError" role="alert">{error}</p>}
    {unsent && session && <details className="card panel-transcript"><summary>Previous draft was not submitted</summary><p className="panel-answer">{unsent}</p><p className="small muted">Another request had already changed that question. This draft was not added to the new question.</p></details>}
    {!lobby && <p role="status">{error ? <button className="btn btn-secondary" onClick={loadLobby}>Retry loading panel</button> : "Loading panel…"}</p>}
    {lobby && <>
      {!session && <section className="panel-welcome"><div><span className="pill pill-g">PERSONALIZED AI PRACTICE</span><h2>Three interviewers.<br/>One stronger you.</h2><p>Your skills, projects and ambitions set the agenda. Get comfortable with the conversation before the real thing.</p><div className="panel-format"><span><Icon name="users" size={17}/> 3 AI personas</span><span><Icon name="message-circle" size={17}/> 6 questions</span><span><Icon name="mic" size={17}/> Voice or text</span></div></div><img src="/Images/interview-panel.png" alt="Illustrated fictional AI interview panel"/></section>}
      <div className="panel-personas">{personas.map((persona, index) => <section key={persona.id} className={`card panel-persona ${active?.persona === persona.id ? "panel-active" : ""}`}>
        <span className="panel-avatar" aria-hidden="true"><Icon name={["code-xml", "layers", "users"][index]} size={24}/></span><h2>{persona.name}</h2><p className="small muted">{persona.focus}</p><span className="panel-role-status">{active?.persona === persona.id ? "Current interviewer" : `Questions ${index * 2 + 1}–${index * 2 + 2}`}</span>
      </section>)}</div>
      {!session ? <>
        <section className="card panel-card"><h2>Your panel briefing</h2>
          {lobby.profile ? <><p><strong>{lobby.profile.target_role}</strong> · {lobby.profile.experience_level}</p><p className="muted">Focus skills: {lobby.profile.skills.join(", ")}</p></> : <p>Save your target role and skills before starting. A resume is optional.</p>}
          <p className="muted">Six questions, one at a time. Type an answer or record in English, review the transcript, then submit. Read-aloud uses your browser voice. This version uses turn-by-turn audio.</p>
          <p className="small muted">Your profile and submitted answers are sent to the configured AI provider. Recordings are sent for transcription and removed from the app server afterward. Submitted answers and feedback are saved {isGuest ? "for this guest browser session" : "with your account"}. Unsaved drafts are lost when you leave.</p>
          <div className="setup-actions"><button className="btn btn-primary" disabled={!lobby.profile || busy} onClick={start}>{busy ? "Preparing your panel…" : "Start panel interview"}</button><button className="btn btn-secondary" disabled={busy} onClick={onSetup}>{lobby.profile ? "Edit my profile" : "Set up my profile"}</button></div>
        </section>
        <section className="panel-history"><h2>Your panel sessions</h2><p className="small muted">Your latest 20 sessions. Reopen to resume or read feedback.</p>{!lobby.sessions.length ? <p className="muted">Your first panel conversation starts here.</p> : lobby.sessions.map(item => <button disabled={busy} className="card panel-history-row" key={item.id} onClick={() => open(item.id)}><span><strong>{item.target_role}</strong><br/><span className="small muted">{new Date(item.created_at).toLocaleDateString()} · {item.answered} answers</span></span><span>{item.status === "completed" ? "View feedback" : "Resume"} →</span></button>)}</section>
      </> : <>
        <p className="small muted">{session.turns.length} of {lobby.total_turns} answers saved · This session uses the profile saved when it started.</p>
        {session.turns.length > 0 && <details className="card panel-transcript"><summary>Conversation so far · {session.turns.length} answers</summary>{session.turns.map(turn => <article key={turn.number}><h3>{turn.number}. {personaName(turn.persona)}</h3><p>{turn.question}</p><p className="panel-answer"><strong>You:</strong> {turn.answer}</p></article>)}</details>}
        {active && <section className="card panel-card">
          <span className="pill pill-g">{personaName(active.persona)} · Question {active.number} / {lobby.total_turns}</span><h2 className="panel-question">{active.question}</h2>
          <div className="setup-actions"><button className="btn btn-secondary" disabled={busy || voiceBusy} onClick={speak}>{speaking ? "Stop reading" : "Read question aloud"}</button>
            <button className="btn btn-secondary" disabled={busy || ["requesting", "transcribing"].includes(voice.phase)} onClick={() => { setError(""); setSpeaking(false); voice.phase === "recording" ? voice.stop() : voice.start(); }}>{voice.phase === "recording" ? `Stop recording · ${voice.seconds}s` : voice.phase === "requesting" ? "Waiting for microphone…" : voice.phase === "transcribing" ? "Transcribing…" : "Record answer"}</button>
          </div><p className="small muted">Recording stops after 2 minutes. You can always type instead.</p>
          {heard && <div className="panel-heard"><h3>Review your transcript</h3><p>{heard}</p><div className="setup-actions"><button className="btn btn-secondary" disabled={busy || voiceBusy} onClick={() => { setDraft(previous => previous ? previous + "\n" + heard : heard); setHeard(""); }}>Add to my answer</button><button className="btn" disabled={busy || voiceBusy} onClick={() => setHeard("")}>Discard transcript</button></div></div>}
          <form onSubmit={submit}><label className="panel-answer-label">Your answer<textarea className="inp" rows={6} maxLength={6000} required value={draft} disabled={busy || voiceBusy} onChange={event => setDraft(event.target.value)} placeholder="Explain your approach, reasoning and an example." /></label>
            <div className="setup-actions"><button className="btn btn-primary" disabled={busy || voiceBusy || !draft.trim()}>{busy ? "Preparing next step…" : "Submit answer →"}</button></div>
          </form>
        </section>}
        {!active && session.status !== "completed" && <section className="card panel-card" aria-live="polite"><h2>{session.status === "report_pending" ? "Your feedback" : "Next panel question"}</h2><p className="muted">{busy ? "The AI panel is preparing your next step…" : "Your submitted answers are saved. Continue when ready."}</p><button className="btn btn-primary" disabled={busy} onClick={() => perform(() => advance(session))}>{session.status === "report_pending" ? "Generate feedback" : "Prepare next question"}</button></section>}
        {session.status === "active" && session.turns.length > 0 && <div className="panel-finish"><p className="small muted">Finishing early uses submitted answers only. Submit or clear any draft first.</p><button className="btn btn-secondary" disabled={busy || voiceBusy || !!draft.trim() || !!heard} onClick={finish}>Finish now & get feedback</button></div>}
        {session.report && <section className="card panel-card"><span className="pill pill-g">PANEL FEEDBACK</span><h2>Your practice takeaways</h2><p>{session.report.summary}</p><p className="small muted">AI coaching based on {session.turns.length} submitted answers; this is not a hiring decision or a verified knowledge score.{session.turns.length < lobby.total_turns ? " This was a shortened session with limited evidence." : ""}</p>
          {session.report.feedback.map(item => <article className="panel-feedback" key={item.question_number}><h3>Question {item.question_number} · {personaName(session.turns[item.question_number - 1]?.persona)}</h3><dl className="setup-summary"><dt>What came through</dt><dd>{item.strength}</dd><dt>What to improve</dt><dd>{item.improvement}</dd><dt>Practice next</dt><dd>{item.practice_task}</dd></dl></article>)}
        </section>}
      </>}
    </>}
  </main>;
}
