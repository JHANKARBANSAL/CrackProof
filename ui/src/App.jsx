const React = window.React;
const { useState, useEffect, useReducer, useCallback, useRef } = React;
import { apiRequest } from "./api/client.js";
import { initialInterviewState, interviewReducer } from "./state/interviewReducer.js";
import { WorkspaceNav as Navbar } from "./components/WorkspaceNav.jsx";
import { LoginScreen } from "./screens/auth/LoginScreen.jsx";
import { SignupScreen } from "./screens/auth/SignupScreen.jsx";
import { DashboardScreen } from "./screens/dashboard/DashboardScreen.jsx";
import { ResumeSetupScreen } from "./screens/dashboard/ResumeSetupScreen.jsx";
import { PanelScreen } from "./screens/interview/PanelScreen.jsx";
import { TopicsScreen } from "./screens/dashboard/TopicsScreen.jsx";
import { ProgressScreen } from "./screens/dashboard/ProgressScreen.jsx";
import { HistoryScreen } from "./screens/history/HistoryScreen.jsx";
import { SubjectHistoryScreen } from "./screens/history/SubjectHistoryScreen.jsx";
import { QuestionPreviewScreen } from "./screens/history/QuestionPreviewScreen.jsx";
import { QuestionRecordingView } from "./screens/interview/QuestionRecordingView.jsx";
import { EvaluationStageView, TranscriptReviewView, EvaluationResultView } from "./screens/interview/EvaluationStageView.jsx";
import { FinalReportView } from "./screens/interview/FinalReportView.jsx";

/* ==============================================================================
   REACT ERROR BOUNDARY COMPONENT
   ------------------------------------------------------------------------------
   Prevents unhandled rendering exceptions from crashing the entire app into a white screen
   ============================================================================== */
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, info) {
    console.error("CrackProof UI Error Boundary caught an error:", error, info);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: "40px 20px", textAlign: "center", maxWidth: "600px", margin: "60px auto" }}>
          <h2 style={{ color: "#D92D20", marginBottom: "12px" }}>Something went wrong</h2>
          <p style={{ color: "#667085", lineHeight: 1.5 }}>
            {this.state.error?.message || "An unexpected error occurred while rendering the view."}
          </p>
          <button
            type="button"
            className="btn btn-primary"
            style={{ marginTop: "20px", padding: "10px 24px" }}
            onClick={() => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

/* ==============================================================================
   MAIN APPLICATION COMPONENT: App
   ------------------------------------------------------------------------------
   Hooks used:
   - [HOOK: useState]   - route ('login'|'signup'|'dash'|'topics'|'interview'|'report')
   - [HOOK: useState]   - user session state, guest flag, history list
   - [HOOK: useReducer] - interview state machine
   - [HOOK: useEffect]  - auto-login check (/api/me), history fetch
   - [HOOK: useCallback]- memoized handlers passed as props
   ============================================================================== */
export function App() {
  // [ROUTING via useState]
  const [route, setRoute] = useState("login");

  // [HOOK: useState] Global App State
  const [user, setUser] = useState(null);
  const [isGuest, setIsGuest] = useState(false);
  const [history, setHistory] = useState([]);
  const [initialSignupEmail, setInitialSignupEmail] = useState("");

  // [HOOK: useState] History & Stop Interview State
  const [selectedHistorySubject, setSelectedHistorySubject] = useState("Java");
  const [historySubjectQuestions, setHistorySubjectQuestions] = useState([]);
  const [selectedQuestionIndex, setSelectedQuestionIndex] = useState(0);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [isStopping, setIsStopping] = useState(false);

  // [HOOK: useReducer] Interview State Machine
  const [interview, dispatch] = useReducer(interviewReducer, initialInterviewState);

  // Audio recording refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerIntervalRef = useRef(null);
  const operationRef = useRef(0);
  const busyRef = useRef(false);
  const recordingVersionRef = useRef(0);
  const startingRecordingRef = useRef(false);
  const navigationRef = useRef(0);
  const transcriptionRef = useRef(null);

  const cancelRecording = useCallback(() => {
    recordingVersionRef.current += 1;
    startingRecordingRef.current = false;
    clearInterval(timerIntervalRef.current);
    transcriptionRef.current?.abort();
    transcriptionRef.current = null;
    const recorder = mediaRecorderRef.current;
    if (recorder) {
      recorder.onstop = null;
      recorder.ondataavailable = null;
      recorder.onerror = null;
      try {
        if (recorder.state !== "inactive") recorder.stop();
      } finally {
        recorder.stream.getTracks().forEach(track => track.stop());
      }
    }
    mediaRecorderRef.current = null;
  }, []);

  // [HOOK: useCallback] Navigation Handler
  const navigate = useCallback((targetScreen) => {
    navigationRef.current += 1;
    setRoute(targetScreen);
    window.scrollTo(0, 0);
  }, []);

  // The server checks account or guest-cookie ownership for all history.
  const loadHistory = useCallback(async () => {
    const navigation = navigationRef.current;
    const res = await apiRequest("/api/history");
    if (navigation !== navigationRef.current) return;
    if (res.ok && res.interviews) {
      setHistory(res.interviews);
    }
  }, []);

  // [HOOK: useEffect] DO NOT auto-redirect to dashboard on initial mount!
  // User always lands on the Welcome Back / Sign In screen and enters only
  // when they explicitly click "Sign In" or "Continue as Guest".
  useEffect(() => {
    // Session check runs silently without forcing navigation
  }, []);

  // [HOOK: useEffect] Reload history whenever navigating to Dashboard, Topics, or Progress screen
  useEffect(() => {
    if (route === "dash" || route === "topics" || route === "progress") {
      loadHistory();
    }
  }, [route, loadHistory]);

  // [HOOK: useCallback] Login Handler
  const handleLogin = useCallback(async (email, password) => {
    const res = await apiRequest("/api/login", { email, password });
    if (res.ok && res.user) {
      setUser(res.user);
      setIsGuest(false);
      navigate("dash");
      return null;
    }
    return res.message || "Invalid credentials.";
  }, [navigate]);

  // [HOOK: useCallback] Signup Handler
  const handleSignup = useCallback(async (name, email, password) => {
    const res = await apiRequest("/api/signup", { name, email, password });
    if (res.ok && res.user) {
      setUser(res.user);
      setIsGuest(false);
      navigate("dash");
      return null;
    }
    return res.message || "Could not create account.";
  }, [navigate]);

  // [HOOK: useCallback] Guest Login Handler
  const handleGuestLogin = useCallback(async () => {
    const res = await apiRequest("/api/logout", {});
    if (!res.ok) {
      alert(res.message || "Could not enter guest mode. Please try again.");
      return;
    }
    setUser(null);
    setHistory([]);
    setIsGuest(true);
    navigate("dash");
  }, [navigate]);

  // [HOOK: useCallback] Logout Handler
  const handleLogout = useCallback(async () => {
    const res = await apiRequest("/api/logout", {});
    if (!res.ok) {
      alert(res.message || "Could not sign out. Please try again.");
      return;
    }
    operationRef.current += 1;
    busyRef.current = false;
    cancelRecording();
    setUser(null);
    setHistory([]);
    setIsGuest(false);
    dispatch({ type: "RESET" });
    navigate("login");
  }, [navigate, cancelRecording]);

  // [HOOK: useCallback] History selection handlers
  const handleSelectHistorySubject = useCallback(async (subjectName) => {
    setSelectedHistorySubject(subjectName);
    setHistoryLoading(true);
    setHistorySubjectQuestions([]);
    navigate("history_subject");
    const navigation = navigationRef.current;
    const url = `/api/history/subject/${encodeURIComponent(subjectName)}`;
    const res = await apiRequest(url);
    if (navigation !== navigationRef.current) return;
    setHistoryLoading(false);
    if (res && res.ok) {
      setHistorySubjectQuestions(res.questions || []);
    } else {
      setHistorySubjectQuestions([]);
      alert(res.message || "Could not load your history. Please try again.");
    }
  }, [navigate, isGuest]);

  const handleSelectHistoryQuestion = useCallback((index) => {
    setSelectedQuestionIndex(index);
    navigate("history_question");
  }, [navigate]);

  // [HOOK: useCallback] Start Interview Topic (Immediate feedback, prevents blank screen)
  const handleStartTopic = useCallback(async (topic) => {
    if (busyRef.current) return;
    busyRef.current = true;
    const operation = ++operationRef.current;
    dispatch({ type: "START_LOADING", payload: { topic } });
    navigate("interview");
    const res = await apiRequest("/api/start", { topic });
    if (operation !== operationRef.current) return;
    busyRef.current = false;
    if (res && res.ok) {
      dispatch({
        type: "START_INTERVIEW",
        payload: {
          topic,
          interviewId: res.interview_id,
          questionNumber: res.question_number || 1,
          questionText: res.question
        }
      });
    } else {
      alert(res?.message || "Failed to start interview.");
      navigate("topics");
    }
  }, [navigate]);

  // [HOOK: useCallback] Recording controls
  const handleStartRecord = useCallback(async () => {
    if (busyRef.current || startingRecordingRef.current || mediaRecorderRef.current?.state === "recording") return;
    startingRecordingRef.current = true;
    const recordingVersion = ++recordingVersionRef.current;
    audioChunksRef.current = [];
    let stream;
    try {
      if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === "undefined") {
        throw new Error("Audio recording is unavailable in this browser. Please use a supported browser on HTTPS or localhost.");
      }
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      if (recordingVersion !== recordingVersionRef.current) {
        stream.getTracks().forEach(track => track.stop());
        return;
      }

      // Auto-detect supported audio recording mimeType across Chrome, Safari, Firefox
      let mimeType = "";
      if (typeof MediaRecorder.isTypeSupported === "function") {
        if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
          mimeType = "audio/webm;codecs=opus";
        } else if (MediaRecorder.isTypeSupported("audio/webm")) {
          mimeType = "audio/webm";
        } else if (MediaRecorder.isTypeSupported("audio/mp4")) {
          mimeType = "audio/mp4";
        } else if (MediaRecorder.isTypeSupported("audio/ogg")) {
          mimeType = "audio/ogg";
        }
      }

      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      recorder.onstop = async () => {
        clearInterval(timerIntervalRef.current);
        // Stop all hardware tracks only after recording completes
        try {
          if (recorder.stream) {
            recorder.stream.getTracks().forEach((track) => track.stop());
          }
        } catch (e) {}
        if (recordingVersion !== recordingVersionRef.current) return;

        const actualMime = recorder.mimeType || mimeType || "audio/webm";
        let ext = "webm";
        if (actualMime.includes("mp4")) ext = "mp4";
        else if (actualMime.includes("ogg")) ext = "ogg";
        else if (actualMime.includes("wav")) ext = "wav";

        const blob = new Blob(audioChunksRef.current, { type: actualMime });

        if (blob.size === 0) {
          alert("Recording was too short or empty. Please speak your answer into the microphone and click Stop.");
          dispatch({ type: "RECORDING_FAILED" });
          return;
        }

        const formData = new FormData();
        formData.append("interview_id", interview.interviewId);
        formData.append("question_number", interview.questionNumber);
        formData.append("audio", blob, `answer.${ext}`);

        const controller = new AbortController();
        transcriptionRef.current = controller;
        const timeout = setTimeout(() => controller.abort(), 180000);
        try {
          const res = await fetch("/api/transcribe", { method: "POST", body: formData, signal: controller.signal });
          const data = await res.json();
          if (recordingVersion !== recordingVersionRef.current) return;
          if (data && data.ok) {
            dispatch({
              type: "SET_TRANSCRIPT",
              payload: {
                transcript: data.transcript || "",
                audioPath: data.audio_path,
                audioBlob: blob
              }
            });
          } else {
            const msg = data?.message || data?.problem || "No speech detected. Please speak into your microphone and try again.";
            alert(msg);
            dispatch({ type: "RECORDING_FAILED" });
          }
        } catch (err) {
          if (recordingVersion !== recordingVersionRef.current) return;
          alert("Transcription server connection error. Please try again.");
          dispatch({ type: "RECORDING_FAILED" });
        } finally {
          clearTimeout(timeout);
          if (transcriptionRef.current === controller) transcriptionRef.current = null;
        }
      };
      recorder.onerror = () => {
        cancelRecording();
        dispatch({ type: "RECORDING_FAILED" });
        alert("Recording failed. Please check your microphone and try again.");
      };

      // Timeslice of 500ms guarantees chunks stream in smoothly
      recorder.start(500);
      dispatch({ type: "START_RECORDING" });

      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = setInterval(() => {
        dispatch({ type: "TICK_TIMER" });
      }, 1000);
    } catch (e) {
      stream?.getTracks().forEach(track => track.stop());
      if (recordingVersion !== recordingVersionRef.current) return;
      alert(e.name === "NotAllowedError" ? "Please allow microphone access to record your answer." : e.message || "Could not start recording. Please check your microphone.");
    } finally {
      if (recordingVersion === recordingVersionRef.current) startingRecordingRef.current = false;
    }
  }, [interview.interviewId, interview.questionNumber, cancelRecording]);

  const handleStopRecord = useCallback(() => {
    if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);

    const recorder = mediaRecorderRef.current;
    if (!recorder) return;

    dispatch({ type: "STOP_RECORDING" });

    try {
      if (recorder.state !== "inactive") {
        recorder.stop();
      }
    } catch (e) {
      console.error("Error stopping recorder:", e);
      dispatch({ type: "RECORDING_FAILED" });
    }
  }, []);

  // [HOOK: useCallback] Submit Answer for Evaluation
  const handleSubmitEvaluation = useCallback(async () => {
    if (busyRef.current || !interview.transcript.trim()) return false;
    busyRef.current = true;
    const operation = ++operationRef.current;
    dispatch({ type: "START_EVALUATION" });
    const res = await apiRequest("/api/evaluate", {
      interview_id: interview.interviewId,
      question_number: interview.questionNumber,
      transcript: interview.transcript,
      audio_path: interview.audioPath
    });
    if (operation !== operationRef.current) return false;
    busyRef.current = false;

    if (res.ok) {
      dispatch({
        type: "SET_EVALUATION",
        payload: {
          evaluation: { ...res.evaluation, sources: res.sources || res.evaluation.sources || [] },
          batchDone: res.batch_complete
        }
      });
      loadHistory();
      return true;
    } else {
      dispatch({ type: "SET_ERROR", payload: res.message || "Evaluation failed. Please retry." });
      alert(res.message || "Evaluation error.");
      return false;
    }
  }, [interview.interviewId, interview.questionNumber, interview.transcript, interview.audioPath, loadHistory]);

  // [HOOK: useCallback] Next Question Handler
  const handleNextQuestion = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    const operation = ++operationRef.current;
    dispatch({ type: "START_EVALUATION" });
    const res = await apiRequest("/api/next", { interview_id: interview.interviewId, question_number: interview.questionNumber });
    if (operation !== operationRef.current) return;
    busyRef.current = false;
    if (res.ok) {
      dispatch({
        type: "SET_NEXT_QUESTION",
        payload: {
          questionNumber: res.question_number,
          questionText: res.question
        }
      });
    } else {
      dispatch({ type: "SET_ERROR", payload: res.message });
      alert(res.message || "Could not load the next question. Please retry.");
    }
  }, [interview.interviewId, interview.questionNumber]);

  // [HOOK: useCallback] Back from Interview - cleans up audio tracks, resets state, and returns to topics
  const handleBackFromInterview = useCallback(() => {
    operationRef.current += 1;
    busyRef.current = false;
    cancelRecording();
    dispatch({ type: "RESET" });
    navigate("topics");
  }, [navigate, cancelRecording]);

  // [HOOK: useCallback] Open Report
  const handleFinishReport = useCallback(async () => {
    if (busyRef.current) return;
    busyRef.current = true;
    const operation = ++operationRef.current;
    setIsStopping(true);
    const res = await apiRequest("/api/report", { interview_id: interview.interviewId });
    if (operation !== operationRef.current) return;
    busyRef.current = false;
    setIsStopping(false);
    if (res && res.ok) {
      loadHistory();
      dispatch({ type: "SET_REPORT", payload: res });
      navigate("report");
    } else {
      dispatch({ type: "SET_ERROR", payload: res.message });
      alert(res.message || "Could not prepare your report. Your completed answers are saved; please retry.");
    }
  }, [interview.interviewId, loadHistory, navigate]);

  const handleStopInterview = useCallback(async () => {
    if (busyRef.current) return;
    cancelRecording();
    const hasCompletedAnswers = interview.questionNumber > 1 || interview.status === "EVALUATION";
    if (!hasCompletedAnswers) {
      handleBackFromInterview();
      return;
    }
    // If report generation fails, return to the current question with a retry path.
    if (interview.status === "RECORDING") dispatch({ type: "RECORDING_FAILED" });
    await handleFinishReport();
  }, [interview.questionNumber, interview.status, cancelRecording, handleBackFromInterview, handleFinishReport]);

  // [HOOK: useCallback] Open Past Report from Dashboard History
  const handleOpenPastReport = useCallback(async (id) => {
    if (busyRef.current) return;
    busyRef.current = true;
    const navigation = navigationRef.current;
    const res = await apiRequest(`/api/interview/${encodeURIComponent(id)}`);
    busyRef.current = false;
    if (navigation !== navigationRef.current) return;
    if (res.ok && res.interview?.report) {
      dispatch({ type: "RESET" });
      dispatch({ type: "SET_REPORT", payload: { ...res.interview.report, topic: res.interview.report.topic || res.interview.topic } });
      navigate("report");
    } else {
      alert(res.message || "This saved report is unavailable.");
    }
  }, [navigate]);

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      operationRef.current += 1;
      cancelRecording();
    };
  }, [cancelRecording]);

  // Compute topic counts for TopicsScreen
  const historyCounts = history.reduce((acc, row) => {
    acc[row.topic] = (acc[row.topic] || 0) + (row.questions_answered || 0);
    return acc;
  }, {});

  /* ==============================================================================
     RENDER ROUTER
     ------------------------------------------------------------------------------
     Conditionally renders active screen based on state
     ============================================================================== */
  return (
    <div className={!["login", "signup", "interview", "history_subject", "history_question"].includes(route) ? "workspace-shell" : ""}>
      {/* Show Navbar on all logged in screens, but interview and subject history drill-downs have their own layouts */}
      {route !== "login" && route !== "signup" && route !== "interview" && route !== "history_subject" && route !== "history_question" && (
        <Navbar
          user={user}
          isGuest={isGuest}
          activeRoute={route}
          onNavigate={navigate}
          onLogout={handleLogout}
        />
      )}

      {route === "login" && (
        <LoginScreen
          onLogin={handleLogin}
          onSwitchToSignup={(em) => { setInitialSignupEmail(em); navigate("signup"); }}
          onGuestLogin={handleGuestLogin}
        />
      )}

      {route === "signup" && (
        <SignupScreen
          initialEmail={initialSignupEmail}
          onSignup={handleSignup}
          onSwitchToLogin={() => navigate("login")}
        />
      )}

      {route === "dash" && (
        <DashboardScreen
          user={user}
          isGuest={isGuest}
          history={history}
          onStartInterview={() => navigate("topics")}
          onSetupInterview={() => navigate("profile")}
          onOpenPanel={() => navigate("panel")}
          onOpenPastReport={handleOpenPastReport}
        />
      )}

      {route === "profile" && <ResumeSetupScreen isGuest={isGuest} onPractice={() => navigate("topics")} onPanel={() => navigate("panel")} />}
      {route === "panel" && <PanelScreen isGuest={isGuest} onSetup={() => navigate("profile")} />}

      {route === "topics" && (
        <TopicsScreen
          onSelectTopic={handleStartTopic}
          onBack={() => navigate("dash")}
          historyCounts={historyCounts}
        />
      )}

      {route === "progress" && (
        <ProgressScreen
          user={user}
          isGuest={isGuest}
          history={history}
          historyCounts={historyCounts}
          onStartInterview={() => navigate("topics")}
          onSelectTopic={handleStartTopic}
          onOpenPastReport={handleOpenPastReport}
          onBack={() => navigate("dash")}
        />
      )}

      {route === "history" && (
        <HistoryScreen
          user={user}
          isGuest={isGuest}
          historyCounts={historyCounts}
          onSelectSubject={handleSelectHistorySubject}
          onBack={() => navigate("dash")}
        />
      )}

      {route === "history_subject" && (
        <SubjectHistoryScreen
          subject={selectedHistorySubject}
          questions={historySubjectQuestions}
          loading={historyLoading}
          onSelectQuestion={handleSelectHistoryQuestion}
          onBack={() => navigate("history")}
          onNavigate={navigate}
          onStartInterview={handleStartTopic}
        />
      )}

      {route === "history_question" && (
        <QuestionPreviewScreen
          subject={selectedHistorySubject}
          questions={historySubjectQuestions}
          currentIndex={selectedQuestionIndex}
          onBack={() => navigate("history_subject")}
          onNavigateIndex={(idx) => setSelectedQuestionIndex(idx)}
          onNavigate={navigate}
        />
      )}

      {route === "interview" && (
        <div>
          {interview.status === "LOADING" && (
            <div className="interview-loading-container">
              <img src="/Images/logo.png" alt="CrackProof Logo" className="interview-pulse-logo" />
              <h2 style={{ fontSize: "1.5rem", fontWeight: 700, color: "#101828", marginBottom: "8px" }}>
                Preparing your {interview.topic} Technical Interview
              </h2>
              <p style={{ color: "#667085", fontSize: "0.98rem" }}>
                Formulating foundational questions and setting up textbook evaluation rubrics...
              </p>
            </div>
          )}

          {interview.status === "QUESTION" && (
            <QuestionRecordingView
              topic={interview.topic}
              questionNumber={interview.questionNumber}
              questionText={interview.questionText}
              isRecording={false}
              recSeconds={0}
              loading={interview.loading}
              onStartRecord={handleStartRecord}
              onStopRecord={handleStopRecord}
              onBack={handleBackFromInterview}
              onStopInterview={handleStopInterview}
            />
          )}

          {interview.status === "RECORDING" && (
            <QuestionRecordingView
              topic={interview.topic}
              questionNumber={interview.questionNumber}
              questionText={interview.questionText}
              isRecording={true}
              recSeconds={interview.recSeconds}
              loading={interview.loading}
              onStartRecord={handleStartRecord}
              onStopRecord={handleStopRecord}
              onBack={handleBackFromInterview}
              onStopInterview={handleStopInterview}
            />
          )}

          {interview.status === "REVIEW" && (
            <TranscriptReviewView
              topic={interview.topic}
              questionNumber={interview.questionNumber}
              questionText={interview.questionText}
              transcript={interview.transcript}
              audioBlob={interview.audioBlob}
              loading={interview.loading}
              onUpdateTranscript={(val) => dispatch({ type: "UPDATE_TRANSCRIPT", payload: val })}
              onSubmitEvaluation={handleSubmitEvaluation}
              onRetry={handleStartRecord}
              onBack={handleBackFromInterview}
              onStopInterview={handleStopInterview}
            />
          )}

          {interview.status === "EVALUATION" && (
            <EvaluationResultView
              topic={interview.topic}
              questionNumber={interview.questionNumber}
              questionText={interview.questionText}
              transcript={interview.transcript}
              audioBlob={interview.audioBlob}
              audioPath={interview.audioPath}
              loading={interview.loading}
              evaluation={interview.evaluation}
              batchDone={interview.batchDone}
              onNextQuestion={handleNextQuestion}
              onFinish={handleFinishReport}
              onBack={handleBackFromInterview}
              onStopInterview={handleStopInterview}
            />
          )}
        </div>
      )}

      {route === "report" && (
        <FinalReportView
          report={interview.report}
          onRestartTopic={() => handleStartTopic(interview.report?.topic || "Java")}
          onChooseNewTopic={() => navigate("topics")}
          onReturnDashboard={() => navigate("dash")}
        />
      )}

      {/* Immediate Stop Interview Feedback Overlay */}
      {isStopping && (
        <div className="stop-loading-backdrop">
          <div className="stop-loading-card">
            <div className="stop-spinner" />
            <h3 style={{ fontSize: "1.25rem", fontWeight: 700, color: "#101828", margin: "0 0 8px" }}>
              Ending Interview Session
            </h3>
            <p style={{ color: "#667085", fontSize: "0.92rem", margin: 0 }}>
              Compiling your demonstrated strengths, knowledge gaps, and evaluation report...
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

/* ==============================================================================
   MOUNT REACT APP
   ============================================================================== */
const rootElement = document.getElementById("root");
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  );
}
