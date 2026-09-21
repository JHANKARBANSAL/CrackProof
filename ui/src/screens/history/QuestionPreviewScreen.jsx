const React = window.React;
const { useState } = React;
import { TOPIC_LIST } from "../dashboard/TopicsScreen.jsx";

/**
 * QuestionPreviewScreen Component
 * Detailed view of a past interview question: question text, candidate transcript, and evaluation tabs.
 */
export function QuestionPreviewScreen({ subject, questions = [], currentIndex = 0, onBack, onNavigateIndex, onNavigate }) {
  const [activeTab, setActiveTab] = useState("right"); // 'right' | 'missing' | 'misconceptions' | 'evidence' | 'reasoning'

  const q = questions[currentIndex] || {};
  const ev = q.evaluation || {};

  const topicObj = TOPIC_LIST.find(t => t.name.toLowerCase() === subject.toLowerCase() || t.displayName.toLowerCase() === subject.toLowerCase()) || {
    name: subject,
    displayName: subject,
    icon: "/Images/java.png"
  };

  const verdictClass = q.verdict === "CORRECT" ? "correct" : q.verdict === "PARTIAL" ? "partial" : "needswork";
  const verdictLabel = q.verdict === "CORRECT" ? "CORRECT" : q.verdict === "PARTIAL" ? "PARTIAL" : "NEEDS WORK";

  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < questions.length - 1;

  const correctPoints = ev.correct_points || [];
  const missingPoints = ev.missing_core_concepts || [];
  const misconceptions = ev.misconceptions || [];
  const evidenceList = ev.evidence || [];
  const reasoning = ev.reasoning || "No evaluation explanation was saved for this answer.";

  return (
    <div className="sub-hist-container">
      {/* Left Sidebar */}
      <aside className="sub-hist-sidebar">
        <div>
          <div className="sub-hist-brand" onClick={() => onNavigate("dash")}>
            <img src="/Images/logo.png" alt="CrackProof" className="sub-hist-brand-img" />
            <span className="sub-hist-brand-name">CrackProof</span>
          </div>

          <nav className="sub-hist-nav-menu">
            <button type="button" className="sub-hist-nav-item" onClick={() => onNavigate("dash")}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                <polyline points="9 22 9 12 15 12 15 22" />
              </svg>
              Home
            </button>
            <button type="button" className="sub-hist-nav-item" onClick={() => onNavigate("topics")}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
                <line x1="8" y1="21" x2="16" y2="21" />
                <line x1="12" y1="17" x2="12" y2="21" />
              </svg>
              Interviews
            </button>
            <button type="button" className="sub-hist-nav-item" onClick={() => onNavigate("progress")}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="20" x2="18" y2="10" />
                <line x1="12" y1="20" x2="12" y2="4" />
                <line x1="6" y1="20" x2="6" y2="14" />
              </svg>
              Progress
            </button>
            <button type="button" className="sub-hist-nav-item active" onClick={() => onNavigate("history")}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              History
            </button>
            <button type="button" className="sub-hist-nav-item" onClick={() => onNavigate("dash")}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
              </svg>
              Settings
            </button>
          </nav>
        </div>

        <div className="sub-hist-sidebar-footer">
          <div className="sub-hist-footer-quote">
            Consistent<br />Practice<br />Creates<br />Confident You.
          </div>
          <img src="/Images/mountain.png" alt="Mountain summit flag" className="sub-hist-footer-img" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="sub-hist-main">
        <div className="preview-actions-bar">
          <button type="button" className="sub-hist-back-btn" onClick={onBack} style={{ margin: 0 }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="19" y1="12" x2="5" y2="12" />
              <polyline points="12 19 5 12 12 5" />
            </svg>
            Back to {topicObj.displayName} History
          </button>

          <div className="preview-prev-next">
            <button
              type="button"
              className="preview-pn-btn"
              disabled={!hasPrev}
              onClick={() => onNavigateIndex(currentIndex - 1)}
            >
              &lt; Previous
            </button>
            <button
              type="button"
              className="preview-pn-btn"
              disabled={!hasNext}
              onClick={() => onNavigateIndex(currentIndex + 1)}
            >
              Next &gt;
            </button>
          </div>
        </div>

        <div className="preview-main-q-header">
          <div>
            <h1 className="preview-main-q-title">{q.question || "Interview Question"}</h1>
            <p className="preview-main-q-time">{q.timestamp}</p>
          </div>

          <div className="preview-main-q-meta">
            <span className={`badge-status ${verdictClass}`}>
              {q.verdict === "CORRECT" && (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              )}
              {q.verdict === "PARTIAL" && (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
              )}
              {q.verdict === "NEEDS_WORK" && (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="12" y1="19" x2="12" y2="5" />
                  <polyline points="5 12 12 5 19 12" />
                </svg>
              )}
              {verdictLabel}
            </span>

            <span className="preview-main-score">
              Score: {q.score_display || `${q.score}/10`}
            </span>
          </div>
        </div>

        {/* Candidate Answer Transcript */}
        <div className="preview-card">
          <h2 className="preview-card-title">Your Answer</h2>
          <div className="preview-answer-body">
            {q.transcript ? q.transcript : <span className="muted" style={{ fontStyle: "italic" }}>No spoken or written transcript recorded for this question.</span>}
          </div>
        </div>

        {/* Evaluation Summary */}
        <div className="preview-card">
          <h2 className="preview-card-title">Evaluation Summary</h2>

          <div className="preview-tabs-row">
            <button
              type="button"
              className={`preview-tab-btn ${activeTab === "right" ? "active" : ""}`}
              onClick={() => setActiveTab("right")}
            >
              What You Got Right ({correctPoints.length})
            </button>
            <button
              type="button"
              className={`preview-tab-btn ${activeTab === "missing" ? "active" : ""}`}
              onClick={() => setActiveTab("missing")}
            >
              What's Missing ({missingPoints.length})
            </button>
            <button
              type="button"
              className={`preview-tab-btn ${activeTab === "misconceptions" ? "active" : ""}`}
              onClick={() => setActiveTab("misconceptions")}
            >
              Misconceptions ({misconceptions.length})
            </button>
            <button
              type="button"
              className={`preview-tab-btn ${activeTab === "evidence" ? "active" : ""}`}
              onClick={() => setActiveTab("evidence")}
            >
              Depth Evidence ({evidenceList.length})
            </button>
            <button
              type="button"
              className={`preview-tab-btn ${activeTab === "reasoning" ? "active" : ""}`}
              onClick={() => setActiveTab("reasoning")}
            >
              Reasoning
            </button>
          </div>

          <div>
            {activeTab === "right" && (
              correctPoints.length === 0 ? (
                <p className="muted" style={{ fontStyle: "italic", margin: 0 }}>
                  No correct technical points demonstrated in this attempt.
                </p>
              ) : (
                <ul className="preview-bullet-list">
                  {correctPoints.map((pt, i) => (
                    <li key={i} className="preview-bullet-item">
                      <span className="preview-bullet-icon" style={{ color: "#12B76A" }}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                          <circle cx="12" cy="12" r="10" />
                          <polyline points="16 9 10 15 7 12" />
                        </svg>
                      </span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              )
            )}

            {activeTab === "missing" && (
              missingPoints.length === 0 ? (
                <p className="muted" style={{ fontStyle: "italic", margin: 0 }}>
                  None! All foundational core concepts were satisfactorily covered.
                </p>
              ) : (
                <ul className="preview-bullet-list">
                  {missingPoints.map((pt, i) => (
                    <li key={i} className="preview-bullet-item">
                      <span className="preview-bullet-icon" style={{ color: "#F79009" }}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <circle cx="12" cy="12" r="10" />
                          <line x1="12" y1="8" x2="12" y2="12" />
                          <line x1="12" y1="16" x2="12.01" y2="16" />
                        </svg>
                      </span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              )
            )}

            {activeTab === "misconceptions" && (
              misconceptions.length === 0 ? (
                <p className="muted" style={{ fontStyle: "italic", margin: 0 }}>
                  No conceptual misconceptions or fallacies were detected in your response.
                </p>
              ) : (
                <ul className="preview-bullet-list">
                  {misconceptions.map((pt, i) => (
                    <li key={i} className="preview-bullet-item">
                      <span className="preview-bullet-icon" style={{ color: "#D92D20" }}>
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <circle cx="12" cy="12" r="10" />
                          <line x1="15" y1="9" x2="9" y2="15" />
                          <line x1="9" y1="9" x2="15" y2="15" />
                        </svg>
                      </span>
                      <span>{typeof pt === "string" ? pt : pt.misconception || JSON.stringify(pt)}</span>
                    </li>
                  ))}
                </ul>
              )
            )}

            {activeTab === "evidence" && (
              evidenceList.length === 0 ? (
                <p className="muted" style={{ fontStyle: "italic", margin: 0 }}>
                  No structured depth dimension evidence recorded.
                </p>
              ) : (
                <ul className="preview-bullet-list">
                  {evidenceList.map((evItem, i) => {
                    const isDem = evItem.status === "DEMONSTRATED";
                    const isPart = evItem.status === "PARTIALLY_DEMONSTRATED";
                    const iconColor = isDem ? "#12B76A" : isPart ? "#F79009" : "#98A2B3";
                    return (
                      <li key={i} className="preview-bullet-item">
                        <span className="preview-bullet-icon" style={{ color: iconColor }}>
                          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                            <circle cx="12" cy="12" r="10" />
                            {isDem ? <polyline points="16 9 10 15 7 12" /> : <line x1="12" y1="8" x2="12" y2="12" />}
                          </svg>
                        </span>
                        <div>
                          <strong style={{ color: "#101828" }}>{evItem.evidence_type}: </strong>
                          <span style={{ color: "#475467" }}>{evItem.evidence_from_answer || evItem.status}</span>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )
            )}

            {activeTab === "reasoning" && (
              <div style={{ lineHeight: 1.65, color: "#344054", fontSize: "0.95rem" }}>
                {reasoning}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
