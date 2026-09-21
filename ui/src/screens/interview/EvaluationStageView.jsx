const React = window.React;
const { useState, useEffect, useRef, useCallback } = React;
import { InterviewTopBar, InterviewTimeline } from "./QuestionRecordingView.jsx";

export function EvaluationStageView({
  topic,
  questionNumber,
  questionText,
  transcript,
  audioBlob,
  audioPath,
  evaluation,
  batchDone,
  loading,
  initialStage = "transcript", // "transcript" for Evaluation1.png, "evaluation" for Evaluation2.png
  onUpdateTranscript,
  onSubmitEvaluation,
  onNextQuestion,
  onFinish,
  onBack,
  onStopInterview,
  onRetry
}) {
  const [stage, setStage] = useState(evaluation ? (initialStage || "evaluation") : "transcript");
  const [isEditing, setIsEditing] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [evalTab, setEvalTab] = useState("right"); // "right" | "missing" | "misconceptions" | "depth" | "reasoning"
  const [activeSource, setActiveSource] = useState(null);
  const audioInstanceRef = useRef(null);
  const audioUrlRef = useRef(null);

  // Sync stage if evaluation completes or initialStage changes
  useEffect(() => {
    if (evaluation && initialStage === "evaluation") {
      setStage("evaluation");
    } else if (initialStage === "transcript" && !evaluation) {
      setStage("transcript");
    }
  }, [evaluation, initialStage]);

  // Audio playback handler
  const handleTogglePlayAudio = useCallback(() => {
    if (audioInstanceRef.current && isPlayingAudio) {
      audioInstanceRef.current.pause();
      setIsPlayingAudio(false);
      return;
    }

    if (audioInstanceRef.current) {
      audioInstanceRef.current.play().then(() => setIsPlayingAudio(true)).catch(() => setIsPlayingAudio(false));
      return;
    }
    let srcUrl = null;
    if (audioBlob) {
      srcUrl = URL.createObjectURL(audioBlob);
      audioUrlRef.current = srcUrl;
    }

    if (!srcUrl) {
      alert("No audio recording available to play.");
      return;
    }

    const audio = new Audio(srcUrl);
    audioInstanceRef.current = audio;
    audio.onended = () => setIsPlayingAudio(false);
    audio.onerror = () => setIsPlayingAudio(false);
    audio.play().then(() => {
      setIsPlayingAudio(true);
    }).catch((err) => {
      console.error("Audio playback error:", err);
      setIsPlayingAudio(false);
    });
  }, [audioBlob, audioPath, isPlayingAudio]);

  // Clean up audio on unmount
  useEffect(() => {
    return () => {
      if (audioInstanceRef.current) {
        audioInstanceRef.current.pause();
      }
      if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
      audioInstanceRef.current = null;
      audioUrlRef.current = null;
    };
  }, [audioBlob]);

  // Handle transition from Evaluation1 -> Evaluation2
  const handleGoToEvaluation = useCallback(async () => {
    if (evaluation) {
      setStage("evaluation");
      return;
    }
    if (onSubmitEvaluation && !loading) {
      const succeeded = await onSubmitEvaluation();
      if (succeeded) setStage("evaluation");
    }
  }, [evaluation, onSubmitEvaluation, loading]);

  // Safe source resolver for "View Source" link
  const handleViewSource = (item, tabCategory) => {
    let source = null;
    let claimText = "";

    if (typeof item === "string") {
      claimText = item;
    } else if (item && typeof item === "object") {
      claimText = item.text || item.claim || item.concept || item.description || "";
      source = item.source;
    }

    if (!source && evaluation?.citations && evaluation.citations.length > 0) {
      const match = evaluation.citations.find(c => c.claim && claimText && c.claim.trim().toLowerCase() === claimText.trim().toLowerCase());
      if (match && evaluation.sources) {
        source = evaluation.sources.find(s => s.number === match.source_number);
      }
    }

    setActiveSource({
      title: source?.title || "No reference linked to this claim",
      section: source?.section || "",
      url: /^https?:\/\//i.test(source?.url || "") ? source.url : null,
      claim: claimText,
      number: source?.number || 1
    });
  };

  // Dynamic banner copy based on evaluation verdict
  let bannerTitle = "Good start!";
  let bannerSubtitle = "You have the core idea. Let's look at what's missing to make it complete.";

  if (evaluation?.verdict === "CORRECT") {
    bannerTitle = "Great work!";
    bannerSubtitle = "You demonstrated solid technical understanding and covered essential core principles.";
  } else if (evaluation?.verdict === "INCORRECT") {
    bannerTitle = "Needs more practice!";
    bannerSubtitle = "Let's review the authoritative textbook references to build firm technical grounding.";
  }

  return (
    <div className="iv-page-wrap">
      <div className="iv-card-frame">
        <InterviewTopBar
          topic={topic}
          questionNumber={questionNumber}
          substep="Evaluation"
          onBack={onBack}
          onStopInterview={onStopInterview}
        />

        <div className="iv-body-grid">
          {/* Left Column: Timeline - Step 3 Evaluation is active */}
          <InterviewTimeline currentStep={3} />

          {/* Center Column: Evaluation Container */}
          <div>
            <div className="eval-card-main">
              {/* STAGE 1: EVALUATION1.PNG ("Your Transcript" active, "Evaluation" to the right) */}
              {stage === "transcript" && (
                <div>
                  {/* Top Navigation Tabs matching mockup/Evaluation1.png */}
                  <div className="eval-top-tabs">
                    <button
                      type="button"
                      className="eval-top-tab active"
                      onClick={() => setStage("transcript")}
                    >
                      Your Transcript
                    </button>
                    <button
                      type="button"
                      className="eval-top-tab"
                      onClick={handleGoToEvaluation}
                      disabled={loading || (!evaluation && !transcript?.trim())}
                      title="View Technical Evaluation"
                    >
                      Evaluation {loading ? "(Evaluating...)" : ""}
                    </button>
                  </div>

                  {/* Card Body matching mockup/Evaluation1.png */}
                  <div className="eval-card-body">
                    {/* Transcript Card with Edit button */}
                    <div className="eval1-transcript-card">
                      <button
                        type="button"
                        className="eval1-edit-btn"
                        onClick={() => setIsEditing(!isEditing)}
                        disabled={loading || !onUpdateTranscript}
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" />
                        </svg>
                        <span>{isEditing ? "Done" : "Edit"}</span>
                      </button>

                      {isEditing ? (
                        <textarea
                          className="inp"
                          rows={5}
                          style={{
                            width: "100%",
                            padding: "14px",
                            fontSize: "0.98rem",
                            lineHeight: 1.6,
                            resize: "vertical",
                            marginTop: "24px",
                            fontFamily: "inherit"
                          }}
                          value={transcript}
                          onChange={(e) => onUpdateTranscript(e.target.value)}
                          placeholder="Type or edit your answer transcript..."
                        />
                      ) : (
                        <p className="eval1-transcript-text">
                          {transcript || "No transcript available. Please record your answer."}
                        </p>
                      )}
                    </div>

                    {/* Status Banner with checkmark and Listen to Audio button */}
                    <div className="eval1-status-banner">
                      <div className="eval1-status-left">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                          <circle cx="12" cy="12" r="10" fill="#12B76A" />
                          <path d="M8 12.5L10.5 15L16 9.5" stroke="#FFFFFF" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                        <span>Review the transcript before evaluating.</span>
                      </div>

                      <button
                        type="button"
                        className="eval1-btn-listen"
                        onClick={handleTogglePlayAudio}
                      >
                        {isPlayingAudio ? (
                          <>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                              <rect x="6" y="4" width="4" height="16" />
                              <rect x="14" y="4" width="4" height="16" />
                            </svg>
                            Pause Audio
                          </>
                        ) : (
                          <>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                              <polygon points="5 3 19 12 5 21 5 3" />
                            </svg>
                            Listen to Audio
                          </>
                        )}
                      </button>
                    </div>

                    {/* Bottom Action Bar: Re-record (optional) + Continue Button */}
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "24px" }}>
                      {onRetry ? (
                        <button
                          type="button"
                          className="btn btn-ghost"
                          style={{ display: "inline-flex", alignItems: "center", gap: "6px" }}
                          onClick={onRetry}
                          title="Re-record your answer to this question"
                        >
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                            <path d="M1 4v6h6" />
                            <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
                          </svg>
                          Re-record Answer
                        </button>
                      ) : <div />}

                      <button
                        type="button"
                        className="eval1-btn-continue"
                        onClick={handleGoToEvaluation}
                        disabled={loading || !transcript?.trim()}
                      >
                        {loading ? "Evaluating Answer..." : "Continue →"}
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* STAGE 2: EVALUATION2.PNG ("What You Got Right", "What's Missing", etc. + sprout banner) */}
              {stage === "evaluation" && (
                <div>
                  {/* Top Navigation Tabs matching mockup/Evaluation2.png */}
                  <div className="eval-top-tabs">
                    <button
                      type="button"
                      className="eval-top-tab"
                      onClick={() => setStage("transcript")}
                      title="Back to Your Transcript"
                      style={{ color: "#667085", marginRight: "6px" }}
                    >
                      ← Your Transcript
                    </button>
                    <button
                      type="button"
                      className={`eval-top-tab ${evalTab === "right" ? "active" : ""}`}
                      onClick={() => setEvalTab("right")}
                    >
                      What You Got Right
                    </button>
                    <button
                      type="button"
                      className={`eval-top-tab ${evalTab === "missing" ? "active" : ""}`}
                      onClick={() => setEvalTab("missing")}
                    >
                      What's Missing
                    </button>
                    <button
                      type="button"
                      className={`eval-top-tab ${evalTab === "misconceptions" ? "active" : ""}`}
                      onClick={() => setEvalTab("misconceptions")}
                    >
                      Misconceptions
                    </button>
                    <button
                      type="button"
                      className={`eval-top-tab ${evalTab === "depth" ? "active" : ""}`}
                      onClick={() => setEvalTab("depth")}
                    >
                      Depth Evidence
                    </button>
                    <button
                      type="button"
                      className={`eval-top-tab ${evalTab === "reasoning" ? "active" : ""}`}
                      onClick={() => setEvalTab("reasoning")}
                    >
                      Reasoning
                    </button>
                  </div>

                  {/* Card Body matching mockup/Evaluation2.png */}
                  <div className="eval-card-body">
                    {/* Active Tab Content Area */}
                    <div style={{ minHeight: "150px" }}>
                      {/* 1. What You Got Right Tab */}
                      {evalTab === "right" && (
                        <div>
                          {(!evaluation?.correct_points || evaluation.correct_points.length === 0) ? (
                            <p className="small muted" style={{ padding: "18px 0" }}>
                              No core points were accurately identified in this response.
                            </p>
                          ) : (
                            evaluation.correct_points.map((point, idx) => {
                              const text = typeof point === "string" ? point : (point?.text || point?.claim || JSON.stringify(point));
                              return (
                                <div key={idx} className="eval2-item-row">
                                  <div className="eval2-item-left">
                                    <div className="eval2-check-circle">
                                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                                        <path d="M7 12.5L10.5 16L17 9" stroke="#FFFFFF" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
                                      </svg>
                                    </div>
                                    <p className="eval2-item-text">{text}</p>
                                  </div>
                                  <button
                                    type="button"
                                    className="eval2-view-source"
                                    onClick={() => handleViewSource(point, "right")}
                                  >
                                    View Source
                                  </button>
                                </div>
                              );
                            })
                          )}
                        </div>
                      )}

                      {/* 2. What's Missing Tab */}
                      {evalTab === "missing" && (
                        <div>
                          {(!evaluation?.missing_core_concepts || evaluation.missing_core_concepts.length === 0) ? (
                            <p className="small muted" style={{ padding: "18px 0" }}>
                              No essential concepts were missed for this question.
                            </p>
                          ) : (
                            evaluation.missing_core_concepts.map((item, idx) => {
                              const text = typeof item === "string" ? item : (item?.text || item?.claim || item?.concept || JSON.stringify(item));
                              return (
                                <div key={idx} className="eval2-item-row">
                                  <div className="eval2-item-left">
                                    <div className="eval2-check-circle" style={{ background: "#F79009" }}>
                                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                                        <line x1="12" y1="8" x2="12" y2="13" stroke="#FFFFFF" strokeWidth="2.8" strokeLinecap="round" />
                                        <circle cx="12" cy="17" r="1.5" fill="#FFFFFF" />
                                      </svg>
                                    </div>
                                    <p className="eval2-item-text">{text}</p>
                                  </div>
                                  <button
                                    type="button"
                                    className="eval2-view-source"
                                    onClick={() => handleViewSource(item, "missing")}
                                  >
                                    View Source
                                  </button>
                                </div>
                              );
                            })
                          )}
                        </div>
                      )}

                      {/* 3. Misconceptions Tab */}
                      {evalTab === "misconceptions" && (
                        <div>
                          {(!evaluation?.misconceptions || evaluation.misconceptions.length === 0) ? (
                            <p className="small muted" style={{ padding: "18px 0" }}>
                              No factual misconceptions were detected in your explanation.
                            </p>
                          ) : (
                            evaluation.misconceptions.map((item, idx) => {
                              const text = typeof item === "string" ? item : (item?.text || item?.claim || JSON.stringify(item));
                              return (
                                <div key={idx} className="eval2-item-row">
                                  <div className="eval2-item-left">
                                    <div className="eval2-check-circle" style={{ background: "#F04438" }}>
                                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                                        <line x1="18" y1="6" x2="6" y2="18" stroke="#FFFFFF" strokeWidth="2.8" strokeLinecap="round" />
                                        <line x1="6" y1="6" x2="18" y2="18" stroke="#FFFFFF" strokeWidth="2.8" strokeLinecap="round" />
                                      </svg>
                                    </div>
                                    <p className="eval2-item-text">{text}</p>
                                  </div>
                                  <button
                                    type="button"
                                    className="eval2-view-source"
                                    onClick={() => handleViewSource(item, "misconceptions")}
                                  >
                                    View Source
                                  </button>
                                </div>
                              );
                            })
                          )}
                        </div>
                      )}

                      {/* 4. Depth Evidence Tab */}
                      {evalTab === "depth" && (
                        <div>
                          {(!evaluation?.deeper_concepts_to_probe || evaluation.deeper_concepts_to_probe.length === 0) ? (
                            <p className="small muted" style={{ padding: "18px 0" }}>
                              Core depth dimensions were assessed according to syllabus standard.
                            </p>
                          ) : (
                            evaluation.deeper_concepts_to_probe.map((item, idx) => {
                              const text = typeof item === "string" ? item : (item?.text || item?.concept || JSON.stringify(item));
                              return (
                                <div key={idx} className="eval2-item-row">
                                  <div className="eval2-item-left">
                                    <div className="eval2-check-circle" style={{ background: "#2E90FA" }}>
                                      ✦
                                    </div>
                                    <p className="eval2-item-text">{text}</p>
                                  </div>
                                  <button
                                    type="button"
                                    className="eval2-view-source"
                                    onClick={() => handleViewSource(item, "depth")}
                                  >
                                    View Source
                                  </button>
                                </div>
                              );
                            })
                          )}
                        </div>
                      )}

                      {/* 5. Reasoning Tab */}
                      {evalTab === "reasoning" && (
                        <div>
                          {evaluation?.reasoning && (
                            <div style={{ background: "#F9FAFB", border: "1px solid #EAECF0", borderRadius: "10px", padding: "16px 20px", marginBottom: "16px" }}>
                              <div style={{ fontWeight: 700, fontSize: "0.92rem", color: "#101828", marginBottom: "6px" }}>
                                Technical Evaluator Analysis:
                              </div>
                              <p className="small" style={{ lineHeight: 1.6, color: "#344054", margin: 0 }}>
                                {evaluation.reasoning}
                              </p>
                            </div>
                          )}

                          {Array.isArray(evaluation?.citations) && evaluation.citations.length > 0 && (
                            <div>
                              <div style={{ fontWeight: 600, fontSize: "0.88rem", color: "#101828", marginBottom: "8px" }}>
                                Authoritative Textbook Citations:
                              </div>
                              {evaluation.citations.map((c, idx) => (
                                <div key={idx} className="eval2-item-row" style={{ padding: "10px 0" }}>
                                  <span className="small" style={{ color: "#344054", flex: 1 }}>
                                    "{typeof c === "string" ? c : (c.claim || JSON.stringify(c))}"
                                  </span>
                                  <button
                                    type="button"
                                    className="eval2-view-source"
                                    onClick={() => handleViewSource(c, "citations")}
                                  >
                                    [Source {c.source_number || idx + 1}]
                                  </button>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Bottom Banner Card matching mockup/Evaluation2.png */}
                    <div className="eval2-bottom-banner">
                      <div className="eval2-banner-left">
                        <div className="eval2-big-check">
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M7 12.5L10.5 16L17 9" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                          </svg>
                        </div>
                        <div>
                          <div className="eval2-banner-title">
                            {bannerTitle}
                          </div>
                          <p className="eval2-banner-sub">
                            {bannerSubtitle}
                          </p>
                        </div>
                      </div>

                      <div className="eval2-banner-right">
                        {/* Sprout SVG matching Evaluation2.png */}
                        <svg width="74" height="74" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <ellipse cx="50" cy="85" rx="32" ry="6" fill="#88A090" opacity="0.4" />
                          <path d="M50 85V44" stroke="#257853" strokeWidth="4.5" strokeLinecap="round" />
                          <path d="M50 64C50 64 26 62 18 46C16 41 20 36 28 38C38 41 48 53 50 64Z" fill="#58A87D" />
                          <path d="M50 58C50 58 74 56 82 40C84 35 80 30 72 32C62 35 52 47 50 58Z" fill="#75C296" />
                          <circle cx="50" cy="34" r="4.5" fill="#58A87D" />
                        </svg>
                      </div>
                    </div>

                    {/* Action Bar Below Banner */}
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "24px" }}>
                      <button
                        type="button"
                        className="btn btn-ghost"
                        onClick={() => setStage("transcript")}
                        style={{ display: "inline-flex", alignItems: "center", gap: "6px" }}
                      >
                        ← Back to Transcript
                      </button>

                      {batchDone ? (
                        <button
                          type="button"
                          className="btn btn-primary"
                          style={{ padding: "12px 30px" }}
                          onClick={onFinish}
                          disabled={loading}
                        >
                          View Final Report →
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="btn btn-primary"
                          style={{ padding: "12px 30px" }}
                          onClick={onNextQuestion}
                          disabled={loading}
                        >
                          Next Question →
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Modal / Popup for "View Source" */}
      {activeSource && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(16, 24, 40, 0.6)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 9999,
            padding: "20px"
          }}
          onClick={() => setActiveSource(null)}
        >
          <div
            style={{
              background: "#FFFFFF",
              borderRadius: "14px",
              maxWidth: "540px",
              width: "100%",
              padding: "24px",
              boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "14px" }}>
              <div>
                <span className="eyebrow" style={{ color: "var(--green)" }}>Evaluation Reference</span>
                <h3 style={{ fontSize: "1.2rem", margin: "4px 0 0", color: "#101828" }}>
                  {activeSource.title}
                </h3>
                {activeSource.section && (
                  <div className="small muted" style={{ marginTop: "2px" }}>
                    Curriculum Section: {activeSource.section}
                  </div>
                )}
              </div>
              <button
                type="button"
                onClick={() => setActiveSource(null)}
                style={{ background: "none", border: "none", fontSize: "1.5rem", cursor: "pointer", color: "#98A2B3", lineHeight: 1 }}
              >
                ×
              </button>
            </div>

            <div style={{ background: "#F9FAFB", border: "1px solid #EAECF0", borderRadius: "8px", padding: "14px 16px", margin: "16px 0", lineHeight: 1.6, fontSize: "0.92rem", color: "#344054" }}>
              {activeSource.claim ? (
                <p style={{ margin: 0 }}>
                  <b>Evaluated Claim:</b> "{activeSource.claim}"
                </p>
              ) : (
                <p style={{ margin: 0 }}>
                  No claim-specific reference is available.
                </p>
              )}
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px", marginTop: "18px" }}>
              {activeSource.url && (
                <a
                  href={activeSource.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-primary small"
                  style={{ padding: "8px 16px", textDecoration: "none" }}
                >
                  Open Source Reference ↗
                </a>
              )}
              <button
                type="button"
                className="btn btn-secondary small"
                style={{ padding: "8px 16px" }}
                onClick={() => setActiveSource(null)}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: TranscriptReviewView (Step 2: "Your Transcript")
   ------------------------------------------------------------------------------
   Renders EvaluationStageView configured for reviewing and editing transcript.
   ============================================================================== */
export function TranscriptReviewView(props) {
  return <EvaluationStageView {...props} initialStage="transcript" />;
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: EvaluationResultView (Step 3: "Evaluation Result")
   ------------------------------------------------------------------------------
   Renders EvaluationStageView configured for displaying detailed evaluation results.
   ============================================================================== */
export function EvaluationResultView(props) {
  return <EvaluationStageView {...props} initialStage="evaluation" />;
}
