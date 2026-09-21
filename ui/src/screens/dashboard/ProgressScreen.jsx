const React = window.React;
import { formatReadiness } from "../../api/client.js";
import { TOPIC_LIST, getTopicAnsweredCount } from "./TopicsScreen.jsx";

/**
 * ProgressScreen Component
 * Displays candidate mastery, KPIs, and subject completion progress bars.
 */
export function ProgressScreen({ user, isGuest, history = [], historyCounts = {}, onStartInterview, onSelectTopic, onOpenPastReport, onBack }) {
  const totalQuestions = history.reduce((acc, r) => acc + (r.questions_answered || 0), 0);
  const totalInterviews = history.length;
  const activeTopicsCount = TOPIC_LIST.filter(t => getTopicAnsweredCount(historyCounts, t.name, t.displayName) > 0).length;
  const latestReadiness = history.length > 0 ? formatReadiness(history[0].readiness) : null;

  return (
    <div className="wrap" style={{ paddingTop: "24px", paddingBottom: "50px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "22px" }}>
        <button
          type="button"
          className="btn-back-arrow"
          onClick={onBack}
          title="Back to Dashboard"
          aria-label="Back to Dashboard"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>
        <div>
          <span className="eyebrow">YOUR PRACTICE, IN PERSPECTIVE</span>
          <h1 style={{ fontSize: "1.75rem", margin: "2px 0 0" }}>Interview Progress & Analytics</h1>
        </div>
      </div>

      {/* Hero Banner */}
      <div className="hero-row" style={{ marginBottom: "28px" }}>
        <div>
          <span className="eyebrow" style={{ color: "var(--green)" }}>Progress Over Perfection</span>
          <h2 style={{ fontSize: "1.6rem", marginTop: "6px" }}>
            See how far your practice has taken you.
          </h2>
          <p className="muted" style={{ marginTop: "8px", lineHeight: "1.5" }}>
            Review your real-time grounded evaluations across all 6 computer science core subjects.
          </p>
          <button
            type="button"
            className="btn btn-primary"
            style={{ marginTop: "18px", padding: "12px 24px" }}
            onClick={onStartInterview}
          >
            Practice Next Interview →
          </button>
        </div>

        <div className="hero-card-right">
          <img
            src="/Images/interview-desk.png"
            alt="Your interview preparation workspace"
            className="progress-hero-img"
          />
        </div>
      </div>

      {/* 4 Metric KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "16px", marginBottom: "32px" }}>
        <div className="card" style={{ padding: "20px" }}>
          <span className="small muted">Total Questions Practiced</span>
          <div style={{ fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" }}>
            {totalQuestions}
          </div>
          <span className="small muted" style={{ color: "var(--green)", fontWeight: 600 }}>
            {totalQuestions > 0 ? "Real evaluation evidence" : "Ready for question 1"}
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <span className="small muted">Interviews Practiced</span>
          <div style={{ fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" }}>
            {totalInterviews}
          </div>
          <span className="small muted">
            {totalInterviews > 0 ? `${totalInterviews} session${totalInterviews === 1 ? "" : "s"} with evaluated answers` : "No evaluated sessions yet"}
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <span className="small muted">Subjects Practiced</span>
          <div style={{ fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" }}>
            {activeTopicsCount} / 6
          </div>
          <span className="small muted">
            {6 - activeTopicsCount > 0 ? `${6 - activeTopicsCount} subjects remaining` : "All subjects covered!"}
          </span>
        </div>

        <div className="card" style={{ padding: "20px" }}>
          <span className="small muted">Latest Readiness Verdict</span>
          <div style={{ marginTop: "10px" }}>
            {latestReadiness ? (
              <span className={`pill ${latestReadiness.pill}`} style={{ fontSize: "0.92rem", padding: "6px 14px" }}>
                {latestReadiness.text}
              </span>
            ) : (
              <span className="pill pill-muted" style={{ fontSize: "0.92rem", padding: "6px 14px" }}>
                Not Evaluated Yet
              </span>
            )}
          </div>
          <span className="small muted" style={{ display: "block", marginTop: "8px" }}>
            Textbook grounded benchmark
          </span>
        </div>
      </div>

      {/* Subject Mastery Progress Bars */}
      <div style={{ marginBottom: "34px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "14px" }}>
          <h2 style={{ fontSize: "1.25rem" }}>Subject Practice Progress</h2>
          <span className="small muted">6 Core Technical Domains</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 310px), 1fr))", gap: "16px" }}>
          {TOPIC_LIST.map((t) => {
            const answered = getTopicAnsweredCount(historyCounts, t.name, t.displayName);
            const pool = t.totalPool || 8;
            const pct = Math.min(100, Math.round((answered / pool) * 100));

            return (
              <div key={t.name} className="card" style={{ padding: "18px 20px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "12px" }}>
                  <img src={t.icon} alt={t.displayName} style={{ width: "42px", height: "42px", objectFit: "contain" }} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: "1rem", color: "var(--ink)" }}>{t.displayName}</div>
                    <span className="small muted">{answered} questions answered</span>
                  </div>
                  <button
                    type="button"
                    className="btn btn-secondary small"
                    onClick={() => onSelectTopic(t.name)}
                    style={{ padding: "6px 12px", fontSize: "0.82rem" }}
                  >
                    Practice →
                  </button>
                </div>

                <div style={{ height: "6px", width: "100%", background: "#EAECF0", borderRadius: "999px", overflow: "hidden" }}>
                  <div
                    style={{
                      height: "100%",
                      width: `${pct}%`,
                      background: pct > 0 ? "var(--green)" : "transparent",
                      borderRadius: "999px",
                      transition: "width 0.4s ease"
                    }}
                  />
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", marginTop: "6px" }}>
                  <span className="small muted" style={{ fontSize: "0.78rem" }}>{pct}% of practice goal</span>
                  <span className="small muted" style={{ fontSize: "0.78rem" }}>{answered} / {pool} answers</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
