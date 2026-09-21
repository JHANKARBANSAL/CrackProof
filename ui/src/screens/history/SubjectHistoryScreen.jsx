const React = window.React;
const { useState, useMemo } = React;
import { TOPIC_LIST } from "../dashboard/TopicsScreen.jsx";

/**
 * SubjectHistoryScreen Component
 * Displays past questions answered for a specific subject with filters (All, Correct, Partial, Needs Work).
 */
export function SubjectHistoryScreen({ subject, questions = [], loading, onSelectQuestion, onBack, onNavigate, onStartInterview }) {
  const [filter, setFilter] = useState("ALL");

  const topicObj = TOPIC_LIST.find(t => t.name.toLowerCase() === subject.toLowerCase() || t.displayName.toLowerCase() === subject.toLowerCase()) || {
    name: subject,
    displayName: subject,
    icon: "/Images/java.png"
  };

  const filteredQuestions = useMemo(() => {
    if (filter === "CORRECT") return questions.filter(q => q.verdict === "CORRECT");
    if (filter === "PARTIAL") return questions.filter(q => q.verdict === "PARTIAL");
    if (filter === "NEEDS_WORK") return questions.filter(q => q.verdict === "NEEDS_WORK");
    return questions;
  }, [questions, filter]);

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

      {/* Main Content Area */}
      <main className="sub-hist-main">
        <button type="button" className="sub-hist-back-btn" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Back to All Subjects
        </button>

        <div className="sub-hist-title-row">
          <div className="sub-hist-heading-group">
            <img src={topicObj.icon} alt={topicObj.displayName} className="sub-hist-subject-icon" />
            <div>
              <h1 className="sub-hist-subject-title">{topicObj.displayName} – History</h1>
              <p className="sub-hist-subject-sub">Your past {topicObj.displayName} interview questions and answers.</p>
            </div>
          </div>

          <select
            className="sub-hist-filter-select"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="ALL">All Results ({questions.length})</option>
            <option value="CORRECT">Correct ({questions.filter(q => q.verdict === "CORRECT").length})</option>
            <option value="PARTIAL">Partial ({questions.filter(q => q.verdict === "PARTIAL").length})</option>
            <option value="NEEDS_WORK">Needs Work ({questions.filter(q => q.verdict === "NEEDS_WORK").length})</option>
          </select>
        </div>

        {loading ? (
          <div style={{ textAlign: "center", padding: "60px 20px", color: "#667085" }}>
            <p>Loading questions history...</p>
          </div>
        ) : filteredQuestions.length === 0 ? (
          <div className="preview-card" style={{ textAlign: "center", padding: "48px 24px" }}>
            <h3 style={{ fontSize: "1.2rem", fontWeight: 700, color: "#101828", marginBottom: "8px" }}>
              No {filter !== "ALL" ? filter.toLowerCase().replace("_", " ") : ""} questions recorded yet
            </h3>
            <p style={{ color: "#667085", maxWidth: "460px", margin: "0 auto 20px" }}>
              Practice technical interview questions in {topicObj.displayName} to generate real-time AI evaluations and grounded evidence.
            </p>
            <button
              type="button"
              className="btn btn-primary"
              style={{ padding: "10px 22px" }}
              onClick={() => onStartInterview(topicObj.name)}
            >
              Start {topicObj.displayName} Interview →
            </button>
          </div>
        ) : (
          <div className="sub-hist-list">
            {filteredQuestions.map((q, idx) => {
              const verdictClass = q.verdict === "CORRECT" ? "correct" : q.verdict === "PARTIAL" ? "partial" : "needswork";
              const verdictLabel = q.verdict === "CORRECT" ? "CORRECT" : q.verdict === "PARTIAL" ? "PARTIAL" : "NEEDS WORK";

              return (
                <div
                  key={q.id || idx}
                  className="sub-hist-q-card"
                  onClick={() => onSelectQuestion(questions.findIndex(item => item.id === q.id))}
                >
                  <div className="sub-hist-q-left">
                    <h3 className="sub-hist-q-text">{q.question}</h3>
                    <p className="sub-hist-q-time">{q.timestamp}</p>
                  </div>

                  <div className="sub-hist-q-right">
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

                    <span className="sub-hist-score">
                      Score: {q.score_display || `${q.score}/10`}
                    </span>

                    <span className="sub-hist-chev">
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="9 18 15 12 9 6" />
                      </svg>
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}
