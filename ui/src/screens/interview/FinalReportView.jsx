const React = window.React;
import { formatReadiness, niceDimensionName } from "../../api/client.js";

/**
 * FinalReportView Component
 * Displays overall candidate readiness, dimension scores, and textbook grounding summary.
 */
export function FinalReportView({ report, onRestartTopic, onChooseNewTopic, onReturnDashboard }) {
  const readinessVal = report?.metrics?.overall_readiness || report?.readiness;
  const readiness = formatReadiness(readinessVal);
  const profile = report?.dimension_profile || report?.depth_profile || {};
  const summary = report?.summary || report?.assessment?.summary || (report?.in_progress ? "These results cover your completed answers so far." : "The written assessment is unavailable. Your evaluated answers and calculated results are saved.");
  const questionsCount = report?.metrics?.questions_answered ?? report?.questions_answered ?? 0;

  return (
    <div className="wrap" style={{ paddingTop: "24px", paddingBottom: "50px", position: "relative" }}>
      <button
        type="button"
        className="btn-back-arrow"
        onClick={onReturnDashboard}
        title="Back to Dashboard"
        aria-label="Back"
        style={{ position: "absolute", left: "0", top: "24px" }}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="19" y1="12" x2="5" y2="12" />
          <polyline points="12 19 5 12 12 5" />
        </svg>
      </button>

      <div style={{ textAlign: "center", marginBottom: "28px" }}>
          <span className="eyebrow">{report?.in_progress ? "Interview In Progress" : "Interview Complete"}</span>
        <h1 style={{ fontSize: "1.75rem", marginTop: "6px" }}>Candidate Evaluation Report</h1>
        <p className="small muted" style={{ marginTop: "4px" }}>
          {report?.topic || "Technical Interview"} · {questionsCount} questions evaluated
        </p>
      </div>

      {/* Overall Card */}
      <div className="card readiness" style={{ padding: "26px", marginBottom: "20px" }}>
        <h3>Performance in This Interview</h3>
        <div style={{ margin: "14px 0" }}>
          <span className={`pill ${readiness.pill}`} style={{ fontSize: "1rem", padding: "8px 18px" }}>
            {readiness.text}
          </span>
        </div>
        <p className="small muted" style={{ lineHeight: 1.5 }}>
          {summary}
        </p>
        {report?.limited_evidence && <p className="small muted">This report uses fewer than five completed answers, so it covers a limited sample of your knowledge.</p>}
      </div>

      {/* Dimension Profile Breakdown */}
      <div className="card readiness" style={{ padding: "26px", marginBottom: "28px" }}>
        <h3>Profile Breakdown</h3>
        <div className="scores" style={{ marginTop: "16px", display: "grid", gap: "14px" }}>
          {Object.entries(profile).map(([dim, score]) => {
            let numScore = 0;
            let displayScore = "";
            let pct = 0;

            if (typeof score === "number") {
              numScore = score;
              displayScore = `${score}/10`;
              pct = Math.min(100, Math.round((numScore / 10) * 100));
            } else if (score && typeof score === "object") {
              if (score.score !== undefined) {
                numScore = Number(score.score) || 0;
                displayScore = `${numScore}/10`;
                pct = Math.min(100, Math.round((numScore / 10) * 100));
              } else if (score.tested !== undefined) {
                const tested = score.tested || 0;
                if (tested > 0) {
                  const demonstrated = score.demonstrated || 0;
                  const partial = score.partially_demonstrated || 0;
                  displayScore = `${demonstrated} demonstrated, ${partial} partial / ${tested} tested`;
                  pct = Math.min(100, Math.round((demonstrated / tested) * 100));
                } else {
                  displayScore = "Not Tested";
                  pct = 0;
                }
              } else {
                displayScore = "Not available";
                pct = 0;
              }
            } else {
              displayScore = String(score);
              pct = 0;
            }

            return (
              <div key={dim}>
                <div className="score-top" style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                  <span>{niceDimensionName(dim)}</span>
                  <b>{displayScore}</b>
                </div>
                <div className="rbar" style={{ height: "8px", background: "#EAEFEA", borderRadius: "4px", overflow: "hidden" }}>
                  <i style={{ display: "block", height: "100%", width: `${pct}%`, background: pct > 0 ? "var(--green)" : "#D0D5DD", borderRadius: "4px" }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {report?.assessment && (
        <div className="card" style={{ padding: "26px", marginBottom: "28px" }}>
          {[
            ["demonstrated_strengths", "Demonstrated Strengths"],
            ["developing_areas", "Developing Areas"],
            ["recurring_knowledge_gaps", "Knowledge Gaps"],
            ["persistent_misconceptions", "Misconceptions to Review"],
            ["insufficiently_tested_areas", "Areas Not Sufficiently Tested"],
            ["recommended_revision_topics", "Recommended Revision Topics"]
          ].map(([field, label]) => report.assessment[field]?.length > 0 && (
            <section key={field} style={{ marginBottom: "18px" }}>
              <h3>{label}</h3>
              <ul style={{ paddingLeft: "20px", lineHeight: 1.6 }}>
                {report.assessment[field].map((item, index) => <li key={index}>{item}</li>)}
              </ul>
            </section>
          ))}
        </div>
      )}

      {/* Next Actions */}
      <div style={{ display: "flex", gap: "12px", justifyContent: "center", flexWrap: "wrap" }}>
        <button className="btn btn-primary" style={{ padding: "12px 24px" }} onClick={onRestartTopic}>
          Practice Another 5 Questions
        </button>
        <button className="btn btn-ghost" style={{ padding: "12px 24px" }} onClick={onChooseNewTopic}>
          Choose Different Topic
        </button>
        <button className="btn btn-ghost" style={{ padding: "12px 24px" }} onClick={onReturnDashboard}>
          Return to Dashboard
        </button>
      </div>
    </div>
  );
}
