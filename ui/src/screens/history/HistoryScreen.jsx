const React = window.React;
const { useState, useEffect } = React;
import { apiRequest } from "../../api/client.js";
import { TOPIC_LIST, getTopicAnsweredCount } from "../dashboard/TopicsScreen.jsx";

/**
 * HistoryScreen Component
 * Displays 6 Subject Cards for history inspection.
 * Uses historyCounts from props so attempt numbers show immediately without delay.
 */
export function HistoryScreen({ user, isGuest, historyCounts = {}, onSelectSubject, onBack }) {
  // Initialize with the 6 subjects and immediate counts from historyCounts
  const [topics, setTopics] = useState(() =>
    TOPIC_LIST.map(t => ({
      name: t.name,
      display_name: t.displayName,
      icon: t.icon,
      subtitle: "View your past questions and answers",
      attempts: getTopicAnsweredCount(historyCounts, t.name, t.displayName) || 0
    }))
  );

  const displayName = isGuest
    ? "Guest"
    : user?.name || (user?.email ? user.email.split("@")[0] : "Candidate");
  const avatarInitial = (displayName[0] || "A").toUpperCase();

  // Background sync with server
  useEffect(() => {
    let active = true;
    async function load() {
      const res = await apiRequest("/api/history/topics");
      if (active && res && res.ok && res.topics) {
        setTopics(res.topics);
      }
    }
    load();
    return () => { active = false; };
  }, [isGuest]);

  return (
    <div className="history-overview-wrap">
      {/* Top Header */}
      <div className="history-top-header">
        <div className="history-brand-col">
          <img src="/Images/logo.png" alt="CrackProof" className="history-header-logo" />
          <div>
            <h1 className="history-header-title">History</h1>
            <p className="history-header-subtitle">Choose a subject to view your interview history.</p>
          </div>
        </div>

        <div className="history-header-right">
          <div className="history-quote-box">
            <span className="history-quote-text">
              "Review. Reflect. Improve.<br />That's how you go further."
            </span>
            <svg className="history-quote-plant" viewBox="0 0 24 24" fill="none" stroke="#166534" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22v-9" />
              <path d="M12 13c-3-3-6-2-8 1 0-4 4-7 8-7 4 0 8 3 8 7-2-3-5-4-8-1z" />
            </svg>
          </div>

          <div className="history-avatar-badge" title={displayName}>
            {avatarInitial}
          </div>
        </div>
      </div>

      {/* 2x3 Grid of 6 Subject Cards */}
      <div className="history-grid-6">
        {topics.map((t) => (
          <button
            key={t.name}
            type="button"
            className="history-subject-card"
            onClick={() => onSelectSubject(t.name)}
          >
            <div className="history-card-left">
              <img src={t.icon} alt={t.display_name} className="history-card-icon" />
              <div className="history-card-details">
                <h3 className="history-card-name">{t.display_name}</h3>
                <p className="history-card-desc">View your past questions and answers</p>
                <span className="history-badge-attempts">
                  {t.attempts || 0} attempt{(t.attempts || 0) === 1 ? "" : "s"}
                </span>
              </div>
            </div>
            <span className="history-card-chevron">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
