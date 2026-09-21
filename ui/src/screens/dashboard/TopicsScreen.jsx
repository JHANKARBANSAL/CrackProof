const React = window.React;
import { Icon } from "../../components/Icon.jsx";

export const TOPIC_LIST = [
  {
    name: "OOP",
    displayName: "Object Oriented Programming",
    icon: "/Images/cube.png",
    totalPool: 8
  },
  {
    name: "Java",
    displayName: "Java",
    icon: "/Images/java.png",
    totalPool: 8
  },
  {
    name: "DBMS",
    displayName: "DBMS",
    icon: "/Images/database.png",
    totalPool: 8
  },
  {
    name: "OS",
    displayName: "Operating Systems",
    icon: "/Images/gear.png",
    totalPool: 8
  },
  {
    name: "Computer Networks",
    displayName: "Computer Networks",
    icon: "/Images/network.png",
    totalPool: 8
  },
  {
    name: "DSA",
    displayName: "Data Structures & Algorithms",
    icon: "/Images/network.png",
    totalPool: 8
  }
];

export function getTopicAnsweredCount(historyCounts = {}, topicName = "", displayName = "") {
  if (!historyCounts || typeof historyCounts !== "object") return 0;

  if (typeof historyCounts[topicName] === "number") return historyCounts[topicName];
  if (typeof historyCounts[displayName] === "number") return historyCounts[displayName];

  const tn = topicName.toLowerCase();
  const dn = displayName.toLowerCase();
  let total = 0;

  for (const [key, count] of Object.entries(historyCounts)) {
    const k = (key || "").toLowerCase();
    const num = Number(count) || 0;
    if (k === tn || k === dn) {
      total += num;
    } else if (tn === "oop" && (k.includes("oop") || k.includes("object"))) {
      total += num;
    } else if (tn === "os" && (k.includes("os") || k.includes("operating"))) {
      total += num;
    } else if (tn === "dbms" && (k.includes("dbms") || k.includes("database"))) {
      total += num;
    } else if ((tn === "cn" || tn.includes("network")) && (k.includes("network") || k.includes("cn"))) {
      total += num;
    } else if (tn === "dsa" && (k.includes("dsa") || k.includes("structure") || k.includes("algorithm"))) {
      total += num;
    } else if (tn === "java" && k.includes("java")) {
      total += num;
    }
  }
  return total;
}

export function TopicsScreen({ onSelectTopic, onBack, historyCounts = {} }) {
  return (
    <div className="topic-page-frame">
      <div className="topic-header-row">
        <button
          className="btn-back-arrow"
          onClick={onBack}
          title="Back to Dashboard"
          aria-label="Back"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
        </button>

        <div className="topic-header-center">
          <span className="eyebrow">KNOWLEDGE PRACTICE</span><h1 className="topic-header-title">Make your fundamentals stronger.</h1>
          <p className="topic-header-subtitle">
            Choose a subject. Explain your thinking. Get feedback with sources.
          </p>
        </div>

        <div className="topic-header-script">
          6 subjects.<br />Your next breakthrough.
        </div>
      </div>

      <div className="topic-grid">
        {TOPIC_LIST.map((t) => {
          const answered = getTopicAnsweredCount(historyCounts, t.name, t.displayName);
          const countText = answered > 0
            ? `${answered} question${answered === 1 ? "" : "s"} answered`
            : "0 questions answered";

          return (
            <button
              key={t.name}
              type="button"
              className="topic-card"
              onClick={() => onSelectTopic(t.name)}
            >
              <span className="topic-symbol"><Icon name={{OOP:"layers",Java:"braces",DBMS:"database",OS:"cpu","Computer Networks":"network",DSA:"route"}[t.name]} size={30}/></span>
              <div className="topic-card-title-row">
                <span className="topic-card-title">{t.displayName}</span>
                <span className="topic-card-chev">&gt;</span>
              </div>
              <div className="topic-card-count">
                <p className="topic-detail">{{OOP:"Objects, design principles and clean abstractions.",Java:"Language fundamentals and practical reasoning.",DBMS:"Queries, data models and reliable transactions.",OS:"Processes, memory and what happens underneath.","Computer Networks":"Protocols, connections and the web in motion.",DSA:"Problem solving, complexity and trade-offs."}[t.name]}</p>{countText}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
