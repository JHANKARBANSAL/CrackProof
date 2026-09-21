const React = window.React;
import { WaveformCluster } from "../../components/WaveformCluster.jsx";
import { SpeakNaturallyCard } from "../../components/SpeakNaturallyCard.jsx";

export function InterviewTopBar({ topic, questionNumber, substep, onBack, onStopInterview }) {
  return (
    <div className="iv-topbar">
      <div className="iv-brand-wrap">
        <button
          type="button"
          className="btn-back-arrow"
          onClick={onBack}
          title="Back to Topics"
          aria-label="Back to Topics"
          style={{ width: "34px", height: "34px", flexShrink: 0 }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>

        <img
          src="/Images/logo.png"
          alt="CrackProof Logo"
          className="iv-logo"
          onClick={onBack}
          style={{ cursor: "pointer" }}
        />
        <div className="iv-breadcrumb">
          <b>{topic}</b>
          <span className="iv-sep">&gt;</span>
          <span>Question {questionNumber} of 5</span>
          {substep && (
            <>
              <span className="iv-sep">&gt;</span>
              <span>{substep}</span>
            </>
          )}
        </div>
      </div>

      <button type="button" className="btn-stop-interview" onClick={onStopInterview}>
        Stop Interview
      </button>
    </div>
  );
}

export const TIMELINE_STEPS = [
  { step: 1, label: "Question" },
  { step: 2, label: "Your Answer" },
  { step: 3, label: "Evaluation" },
  { step: 4, label: "Next Question" },
  { step: 5, label: "Complete" }
];

export function InterviewTimeline({ currentStep }) {
  return (
    <div className="iv-timeline">
      {TIMELINE_STEPS.map((item, idx) => {
        const isDone = item.step < currentStep;
        const isActive = item.step === currentStep;
        const isLast = idx === TIMELINE_STEPS.length - 1;

        return (
          <div
            key={item.step}
            className={`iv-step-item ${isActive ? "active" : ""} ${isDone ? "done" : ""}`}
          >
            {!isLast && <div className="iv-step-line" />}
            <div className="iv-step-circle">
              {item.step}
            </div>
            <span className="iv-step-label">{item.label}</span>
          </div>
        );
      })}
    </div>
  );
}

export function QuestionRecordingView({
  topic,
  questionNumber,
  questionText,
  isRecording,
  recSeconds,
  loading,
  onStartRecord,
  onStopRecord,
  onBack,
  onStopInterview
}) {
  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m < 10 ? "0" : ""}${m}:${s < 10 ? "0" : ""}${s}`;
  };

  return (
    <div className="iv-page-wrap">
      <div className="iv-card-frame">
        <InterviewTopBar
          topic={topic}
          questionNumber={questionNumber}
          onBack={onBack}
          onStopInterview={onStopInterview}
        />

        <div className="iv-body-grid">
          <InterviewTimeline currentStep={1} />

          <div>
            <div className="iv-question-card">
              <h2 className="iv-question-title">
                {questionText || "Preparing your question..."}
              </h2>
            </div>

            <div className="iv-voice-box">
              <div className="iv-voice-status">
                {loading ? (
                  <span className="idle-text" style={{ color: "var(--green)" }}>
                    Preparing your transcript...
                  </span>
                ) : isRecording ? (
                  <div>
                    <span className="recording-text">Recording...</span>
                    <span className="recording-timer">{formatTime(recSeconds)}</span>
                  </div>
                ) : (
                  <span className="idle-text">Click microphone to record your answer</span>
                )}
              </div>

              <div className="iv-rec-center-row">
                <WaveformCluster isRecording={isRecording} side="left" />

                <button
                  className={`btn-record-main ${isRecording ? "is-recording" : "is-idle"}`}
                  onClick={isRecording ? onStopRecord : onStartRecord}
                  disabled={loading}
                  title={isRecording ? "Click to stop recording" : "Click to start recording"}
                >
                  {isRecording ? (
                    <span className="stop-square" />
                  ) : (
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                      <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                      <line x1="12" y1="19" x2="12" y2="23" />
                      <line x1="8" y1="23" x2="16" y2="23" />
                    </svg>
                  )}
                </button>

                <WaveformCluster isRecording={isRecording} side="right" />
              </div>

              <div className="iv-voice-subtext">
                {loading
                  ? "Please wait while your answer is transcribed."
                  : isRecording
                  ? "Click to stop recording"
                  : "Click microphone to start speaking"}
              </div>
            </div>
          </div>

          <SpeakNaturallyCard isRecording={isRecording} />
        </div>
      </div>
    </div>
  );
}
