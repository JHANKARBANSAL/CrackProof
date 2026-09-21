/**
 * ==============================================================================
 * CrackProof - React Frontend (App.jsx)
 * ==============================================================================
 * Concepts Used:
 * 1. Functional Components
 * 2. [HOOK: useState]   - Local state for forms, tabs, inputs, loading states
 * 3. [HOOK: useEffect]  - Lifecycle effects (session restore, history load, timers)
 * 4. [HOOK: useReducer] - State machine for interview flow (recording, transcribe, eval)
 * 5. [HOOK: useCallback]- Memoized callbacks passed as props to prevent re-renders
 * 6. [PROPS]            - Passing data & handler functions down to child components
 * 7. [ROUTING]          - Client-side navigation between screens
 * 
 * Note: Simple, clean, readable React without complex build tools!
 * ==============================================================================
 */

const { useState, useEffect, useReducer, useCallback, useRef, useMemo } = React;

/* ==============================================================================
   API HELPER (Fetch Wrapper)
   ============================================================================== */
async function apiRequest(path, data = null) {
  const options = { method: data ? "POST" : "GET" };
  if (data) {
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(data);
  }

  try {
    const res = await fetch(path, options);
    return await res.json();
  } catch (err) {
    return {
      ok: false,
      message: "Could not reach server. Make sure python3 server.py is running."
    };
  }
}

/* Formatters */
function formatReadiness(val) {
  if (val === "STRONG" || val === "READY") return { text: "Ready", pill: "pill-g" };
  if (val === "DEVELOPING" || val === "ALMOST_READY") return { text: "Almost Ready", pill: "pill-a" };
  if (val === "NEEDS_IMPROVEMENT") return { text: "Needs Practice", pill: "pill-n" };
  return { text: "In Progress", pill: "pill-b" };
}

function niceDimensionName(dim) {
  const map = {
    FUNDAMENTAL: "Core Concepts",
    REASONING: "Technical Reasoning",
    APPLICATION: "Real-World Application",
    EDGE_CASE: "Edge Cases & Depth"
  };
  return map[dim] || dim;
}

/* ==============================================================================
   4. [HOOK: useReducer] - Centralized Interview State Machine
   ------------------------------------------------------------------------------
   Why useReducer? 
   Interview mein bohot saare related states hote hain:
   (question -> recording -> transcribing -> review -> evaluating -> report).
   useReducer sabhi transitions ko predictable aur clean banata hai.
   ============================================================================== */
const initialInterviewState = {
  status: "IDLE",            // 'IDLE' | 'RECORDING' | 'REVIEW' | 'EVALUATION' | 'REPORT'
  topic: "",
  interviewId: null,
  questionNumber: 1,
  questionText: "",
  recSeconds: 0,
  transcript: "",
  audioPath: null,
  audioBlob: null,
  evaluation: null,
  batchDone: false,
  report: null,
  loading: false,
  error: null
};

function interviewReducer(state, action) {
  switch (action.type) {
    case "START_LOADING":
      return {
        ...initialInterviewState,
        status: "LOADING",
        topic: action.payload.topic,
        loading: true
      };

    case "START_INTERVIEW":
      return {
        ...initialInterviewState,
        status: "QUESTION",
        topic: action.payload.topic,
        interviewId: action.payload.interviewId,
        questionNumber: action.payload.questionNumber || 1,
        questionText: action.payload.questionText,
        loading: false
      };

    case "START_RECORDING":
      return {
        ...state,
        status: "RECORDING",
        recSeconds: 0,
        error: null
      };

    case "TICK_TIMER":
      return {
        ...state,
        recSeconds: state.recSeconds + 1
      };

    case "STOP_RECORDING":
      return {
        ...state,
        loading: true
      };

    case "RECORDING_FAILED":
      return {
        ...state,
        status: "QUESTION",
        loading: false,
        recSeconds: 0
      };

    case "SET_TRANSCRIPT":
      return {
        ...state,
        status: "REVIEW",
        loading: false,
        transcript: action.payload.transcript,
        audioPath: action.payload.audioPath,
        audioBlob: action.payload.audioBlob
      };

    case "UPDATE_TRANSCRIPT":
      return {
        ...state,
        transcript: action.payload
      };

    case "START_EVALUATION":
      return {
        ...state,
        loading: true,
        error: null
      };

    case "SET_EVALUATION":
      return {
        ...state,
        status: "EVALUATION",
        loading: false,
        evaluation: action.payload.evaluation,
        batchDone: action.payload.batchDone
      };

    case "SET_NEXT_QUESTION":
      return {
        ...state,
        status: "QUESTION",
        questionNumber: action.payload.questionNumber,
        questionText: action.payload.questionText,
        transcript: "",
        audioPath: null,
        audioBlob: null,
        evaluation: null,
        loading: false
      };

    case "SET_REPORT":
      return {
        ...state,
        status: "REPORT",
        report: action.payload,
        loading: false
      };

    case "SET_ERROR":
      return {
        ...state,
        loading: false,
        error: action.payload
      };

    case "RESET":
      return initialInterviewState;

    default:
      return state;
  }
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: Navbar
   ------------------------------------------------------------------------------
   Parent (App) se props receive karta hai:
   - user: Logged in user object (id, email, name)
   - isGuest: Boolean flag for guest mode
   - activeRoute: Current active screen name
   - onNavigate: Screen switch callback
   - onLogout: Logout callback
   ============================================================================== */
function Navbar({ user, isGuest, activeRoute, onNavigate, onLogout }) {
  // User name display resolution:
  const displayName = isGuest
    ? "Guest"
    : user?.name || (user?.email ? user.email.split("@")[0] : "Candidate");

  const avatarInitial = (displayName[0] || "U").toUpperCase();

  return (
    <div className="nav">
      <div className="nav-in">
        <div className="nav-brand" onClick={() => onNavigate("dash")} style={{ cursor: "pointer" }}>
          <img src="/Images/logo.png" alt="CrackProof Logo" className="nav-logo" />
        </div>

        <div className="nav-links">
          <button
            type="button"
            className={activeRoute === "dash" ? "on" : ""}
            onClick={() => onNavigate("dash")}
          >
            Home
          </button>
          <button
            type="button"
            className={activeRoute === "topics" ? "on" : ""}
            onClick={() => onNavigate("topics")}
          >
            Interviews
          </button>
          <button
            type="button"
            className={activeRoute === "progress" ? "on" : ""}
            onClick={() => onNavigate("progress")}
          >
            Progress
          </button>
          <button
            type="button"
            className={(activeRoute === "history" || activeRoute === "history_subject" || activeRoute === "history_question") ? "on" : ""}
            onClick={() => onNavigate("history")}
          >
            History
          </button>
        </div>

        <div className="userChip">
          <span className="small muted" title={user?.email || ""}>
            {displayName}
          </span>
          <div className="avatar" title={`Logged in as ${displayName}`}>
            {avatarInitial}
          </div>

          {/* Vertical divider line separating Profile Icon and Sign Out */}
          <div className="nav-vertical-divider" aria-hidden="true" />

          {/* Sign Out button shifted to the right */}
          <button
            type="button"
            className="btn-nav-signout"
            onClick={onLogout}
            title="Sign out of CrackProof"
          >
            Sign out
          </button>
        </div>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: LoginScreen
   ------------------------------------------------------------------------------
   Hooks: [useState] for form inputs and errors
   Props: onLogin, onSwitchToSignup, onGuestLogin
   ============================================================================== */
function LoginScreen({ onLogin, onSwitchToSignup, onGuestLogin }) {
  // [HOOK: useState] Local component state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!email.trim() || !password) {
      setError("Please enter both your email and password.");
      return;
    }

    setError("");
    setLoading(true);
    const err = await onLogin(email.trim(), password);
    setLoading(false);
    if (err) setError(err);
  };

  return (
    <div className="auth-screen">
      <div className="auth-container">
        {/* Left Column: White Card Box */}
        <div className="auth-card">
          <div className="auth-brand">
            <img src="/Images/logo.png" alt="CrackProof Logo" className="auth-logo" />
            <p className="auth-tagline">Practice. Understand. Improve.</p>
          </div>

          <h1 className="auth-title">Welcome Back</h1>
          <p className="auth-subtitle">Sign in to continue your interview journey</p>

          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label htmlFor="loginEmail">Email</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                <input
                  id="loginEmail"
                  className="inp"
                  type="email"
                  placeholder="you@example.com"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="loginPw">Password</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  id="loginPw"
                  className="inp"
                  type="password"
                  placeholder="Your password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && <p className="formError">{error}</p>}

            <button type="submit" className="btn-signin" disabled={loading}>
              {loading ? "Signing In..." : "Sign In"}
            </button>
          </form>

          <div className="auth-divider">
            <span>or</span>
          </div>

          <button type="button" className="btn-guest" onClick={onGuestLogin}>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            Continue as Guest
          </button>

          <p className="auth-footer">
            Don't have an account?{" "}
            <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToSignup(email); }}>
              Sign up
            </a>
          </p>
        </div>

        {/* Right Column: Illustrated Graphic */}
        <div className="auth-illustration">
          <img src="/Images/landing_pg.png" alt="A better you for a brighter career" />
        </div>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: SignupScreen
   ------------------------------------------------------------------------------
   Hooks: [useState] for name, email, password, loading, errors
   Props: onSignup, onSwitchToLogin, initialEmail
   ============================================================================== */
function SignupScreen({ onSignup, onSwitchToLogin, initialEmail = "" }) {
  // [HOOK: useState]
  const [name, setName] = useState("");
  const [email, setEmail] = useState(initialEmail);
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (!name.trim()) {
      setError("Please enter your full name.");
      return;
    }
    if (!email.trim() || !password) {
      setError("Please fill in all fields.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }

    setError("");
    setLoading(true);
    const err = await onSignup(name.trim(), email.trim(), password);
    setLoading(false);
    if (err) setError(err);
  };

  return (
    <div className="auth-screen">
      <div className="auth-container">
        {/* Left Column: White Card Box */}
        <div className="auth-card">
          <div className="auth-brand">
            <img src="/Images/logo.png" alt="CrackProof Logo" className="auth-logo" />
            <p className="auth-tagline">Practice. Understand. Improve.</p>
          </div>

          <h1 className="auth-title">Create Account</h1>
          <p className="auth-subtitle">Sign up to save your interviews and track progress</p>

          <form onSubmit={handleSubmit}>
            {/* Full Name Field */}
            <div className="auth-field">
              <label htmlFor="suName">Full Name</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <input
                  id="suName"
                  className="inp"
                  type="text"
                  placeholder="John Doe"
                  autoComplete="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="suEmail">Email</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                <input
                  id="suEmail"
                  className="inp"
                  type="email"
                  placeholder="you@example.com"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="suPassword">Password</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  id="suPassword"
                  className="inp"
                  type="password"
                  placeholder="At least 6 characters"
                  autoComplete="new-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && <p className="formError">{error}</p>}

            <button type="submit" className="btn-signin" disabled={loading}>
              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          <p className="auth-footer">
            Already have an account?{" "}
            <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToLogin(email); }}>
              Sign in
            </a>
          </p>
        </div>

        {/* Right Column: Illustrated Graphic */}
        <div className="auth-illustration">
          <img src="/Images/landing_pg.png" alt="A better you for a brighter career" />
        </div>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: DashboardScreen
   ------------------------------------------------------------------------------
   Props: user, isGuest, history, onStartInterview, onOpenPastReport
   Image: Uses Images/mountain.png on the right side
   Name: Displays personalized greeting with user's actual name
   ============================================================================== */
function DashboardScreen({ user, isGuest, history, onStartInterview, onOpenPastReport }) {
  const displayName = isGuest
    ? "Guest"
    : user?.name || (user?.email ? user.email.split("@")[0] : "Candidate");

  return (
    <div className="wrap">
      {/* Hero Row: Left Greeting, Right Mountain Banner */}
      <div className="hero-row">
        <div>
          <h1 style={{ fontSize: "1.85rem" }}>
            {isGuest ? "Welcome to CrackProof!" : `Good to see you, ${displayName}!`}
          </h1>
          <p className="muted" style={{ marginTop: "6px" }}>
            Ready to practice a core CS technical interview?
          </p>
          {isGuest && (
            <p className="formError" style={{ marginTop: "14px" }}>
              You are practicing as a guest. Your sessions will not be saved on the server.
            </p>
          )}
          <button
            className="btn btn-primary"
            style={{ marginTop: "22px", padding: "13px 26px" }}
            onClick={onStartInterview}
          >
            Start an Interview&nbsp; →
          </button>
        </div>

        {/* Right Side Mountain Card (Replaced old plain text metric box) */}
        <div className="hero-card-right">
          <img
            src="/Images/mountain.png"
            alt="Small conversations today. Bigger opportunities tomorrow."
            className="hero-mountain-img"
          />
        </div>
      </div>

      {/* Past Interviews Section */}
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between", marginBottom: "12px" }}>
        <h2 style={{ fontSize: "1.12rem" }}>Your Recent Interviews</h2>
        <span className="small muted">Evaluated against textbook standards</span>
      </div>

      <div className="card" style={{ overflow: "hidden", marginBottom: "40px" }}>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Topic</th>
              <th>Questions</th>
            </tr>
          </thead>
          <tbody>
            {isGuest ? (
              <tr>
                <td colSpan="3" className="muted small" style={{ padding: "26px", textAlign: "center" }}>
                  Guest sessions are not stored. Sign up to track your progress over time.
                </td>
              </tr>
            ) : !history || history.length === 0 ? (
              <tr>
                <td colSpan="3" className="muted small" style={{ padding: "26px", textAlign: "center" }}>
                  No past interviews yet. Pick a topic above to begin!
                </td>
              </tr>
            ) : (
              history.map((row) => {
                const dateStr = row.created_at ? row.created_at.slice(0, 10) : "Recent";
                return (
                  <tr
                    key={row.id}
                    className="histRow"
                    onClick={() => onOpenPastReport(row.id)}
                    style={{ cursor: "pointer" }}
                  >
                    <td>{dateStr}</td>
                    <td><b>{row.topic}</b></td>
                    <td>{row.questions_answered || 0} answered</td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: TopicsScreen
   ------------------------------------------------------------------------------
/* ==============================================================================
   PROPS & CHILD COMPONENT: TopicsScreen
   ------------------------------------------------------------------------------
   EXACT MATCH FOR mockup/icons.png:
   - Top-left: Back arrow button (←)
   - Center: Title & Subtitle
   - Top-right: Handwritten script "Same topics. New you."
   - 2x3 Grid of centered white cards with image icons:
     1. Object Oriented Programming -> Images/cube.png
     2. Java                        -> Images/java.png
     3. DBMS                        -> Images/database.png
     4. Operating Systems           -> Images/gear.png
     5. Computer Networks           -> Images/network.png
     6. Data Structures & Algorithms-> Images/network.png
   ============================================================================== */
const TOPIC_LIST = [
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

// Helper to compute real, dynamic questions answered for a topic
function getTopicAnsweredCount(historyCounts = {}, topicName = "", displayName = "") {
  if (!historyCounts || typeof historyCounts !== "object") return 0;

  // 1. Direct key matches
  if (typeof historyCounts[topicName] === "number") return historyCounts[topicName];
  if (typeof historyCounts[displayName] === "number") return historyCounts[displayName];

  // 2. Fuzzy match across topic variations in history
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

function TopicsScreen({ onSelectTopic, onBack, historyCounts = {} }) {
  return (
    <div className="topic-page-frame">
      {/* Top Header Row with Back Arrow, Centered Title, and Right Handwritten Script */}
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
          <h1 className="topic-header-title">Choose a Topic</h1>
          <p className="topic-header-subtitle">
            Select a subject to start your interview
          </p>
        </div>

        <div className="topic-header-script">
          Same topics.<br />
          New you.
        </div>
      </div>

      {/* 2x3 Grid of Topic Cards */}
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
              <img
                src={t.icon}
                alt={t.displayName}
                className="topic-card-icon"
              />
              <div className="topic-card-title-row">
                <span className="topic-card-title">{t.displayName}</span>
                <span className="topic-card-chev">&gt;</span>
              </div>
              <div className="topic-card-count">
                {countText}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: ProgressScreen
   ------------------------------------------------------------------------------
   Dedicated Progress page matching navbar "Progress" tab.
   Uses Images/progress.png ("Progress over perfection")
   Features:
   - Header with Back arrow
   - Illustrated Hero banner with progress.png
   - 4 Metric KPI Cards: Total Questions, Interviews, Subjects Active, Readiness
   - Subject Mastery & Curriculum progress bars for all 6 subjects
   - Clickable past interview history archive
   ============================================================================== */
function ProgressScreen({ user, isGuest, history = [], historyCounts = {}, onStartInterview, onSelectTopic, onOpenPastReport, onBack }) {
  const totalQuestions = history.reduce((acc, r) => acc + (r.questions_answered || 0), 0);
  const totalInterviews = history.length;
  const activeTopicsCount = TOPIC_LIST.filter(t => getTopicAnsweredCount(historyCounts, t.name, t.displayName) > 0).length;
  const latestReadiness = history.length > 0 ? formatReadiness(history[0].readiness) : null;

  return (
    <div className="wrap" style={{ paddingTop: "24px", paddingBottom: "50px" }}>
      {/* Top Header Row with Back Button */}
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
          <span className="eyebrow">Candidate Mastery</span>
          <h1 style={{ fontSize: "1.75rem", margin: "2px 0 0" }}>Interview Progress & Analytics</h1>
        </div>
      </div>

      {/* Hero Banner with progress.png */}
      <div className="hero-row" style={{ marginBottom: "28px" }}>
        <div>
          <span className="eyebrow" style={{ color: "var(--green)" }}>Progress Over Perfection</span>
          <h2 style={{ fontSize: "1.6rem", marginTop: "6px" }}>
            Every interview step builds permanent technical confidence.
          </h2>
          <p className="muted" style={{ marginTop: "8px", lineHeight: "1.5" }}>
            Review your real-time grounded evaluations across all 6 computer science core subjects. Each session measures technical correctness, reasoning depth, and edge-case mastery.
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
            src="/Images/progress.png"
            alt="Progress over perfection."
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
          <span className="small muted">Interviews Completed</span>
          <div style={{ fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" }}>
            {totalInterviews}
          </div>
          <span className="small muted">
            {totalInterviews > 0 ? `${totalInterviews} batch${totalInterviews === 1 ? "" : "es"} evaluated` : "0 sessions finished"}
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

      {/* Subject Mastery Breakdown */}
      <div style={{ marginBottom: "34px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "14px" }}>
          <h2 style={{ fontSize: "1.25rem" }}>Subject Mastery & Curriculum Coverage</h2>
          <span className="small muted">6 Core Technical Domains</span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(310px, 1fr))", gap: "16px" }}>
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

                {/* Progress bar */}
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
                  <span className="small muted" style={{ fontSize: "0.78rem" }}>{pct}% mastery</span>
                  <span className="small muted" style={{ fontSize: "0.78rem" }}>{answered} / {pool} benchmark questions</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: HistoryScreen
   ------------------------------------------------------------------------------
   Matches mockup/HISTORY.png:
   - Header with bird logo, "History", Subtitle: "Choose a subject to view your interview history."
   - Quote box on right: "Review. Reflect. Improve. That's how you go further." with sprout plant
   - Candidate avatar
   - 6 subject cards with icons, title, "View your past questions and answers", dynamic attempts count, chevron
   ============================================================================== */
function HistoryScreen({ user, isGuest, onSelectSubject, onBack }) {
  const [topics, setTopics] = useState(() =>
    TOPIC_LIST.map(t => ({
      name: t.name,
      display_name: t.displayName,
      icon: t.icon,
      subtitle: "View your past questions and answers",
      attempts: 0
    }))
  );
  const [loading, setLoading] = useState(false);

  const displayName = isGuest
    ? "Guest"
    : user?.name || (user?.email ? user.email.split("@")[0] : "Candidate");
  const avatarInitial = (displayName[0] || "A").toUpperCase();

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      const guestHistory = isGuest ? JSON.parse(localStorage.getItem("crackproof_guest_history") || "[]") : [];
      const guestIds = guestHistory.map(g => g.interview_id).filter(Boolean).join(",");
      const url = `/api/history/topics${guestIds ? `?guest_ids=${encodeURIComponent(guestIds)}` : ""}`;
      const res = await apiRequest(url);
      if (active) {
        if (res && res.ok && res.topics) {
          setTopics(res.topics);
        } else {
          setTopics(TOPIC_LIST.map(t => ({
            name: t.name,
            display_name: t.displayName,
            icon: t.icon,
            subtitle: "View your past questions and answers",
            attempts: 0
          })));
        }
        setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [isGuest]);

  return (
    <div className="history-overview-wrap">
      {/* Top Header Row matching mockup/HISTORY.png */}
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

      {/* 2x3 Grid of Subject History Cards */}
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

/* ==============================================================================
   PROPS & CHILD COMPONENT: SubjectHistoryScreen
   ------------------------------------------------------------------------------
   Matches mockup/SUB_Hist.png:
   - Left sidebar with Logo, Home, Interviews, Progress, History (active green pill), Settings
   - Bottom sidebar footer: Mountain image + "Consistent Practice Creates Confident You."
   - Main content:
     - Back to All Subjects
     - Subject icon + Title + Subtitle
     - Filter dropdown on right (All Results, Correct, Partial, Needs Work)
     - Question cards: question text, date/time, status badge, score, chevron
     - Empty state if 0 questions
   ============================================================================== */
function SubjectHistoryScreen({ subject, questions = [], loading, onSelectQuestion, onBack, onNavigate, onStartInterview }) {
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
      {/* Left Sidebar matching mockup/SUB_Hist.png */}
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

        {/* Sidebar Footer with Mountain Image */}
        <div className="sub-hist-sidebar-footer">
          <div className="sub-hist-footer-quote">
            Consistent<br />Practice<br />Creates<br />Confident You.
          </div>
          <img src="/Images/mountain.png" alt="Mountain summit flag" className="sub-hist-footer-img" />
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="sub-hist-main">
        {/* Back Link */}
        <button type="button" className="sub-hist-back-btn" onClick={onBack}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Back to All Subjects
        </button>

        {/* Header Title Row */}
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

        {/* Question Cards List */}
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

/* ==============================================================================
   PROPS & CHILD COMPONENT: QuestionPreviewScreen
   ------------------------------------------------------------------------------
   Matches mockup/q_sub_full_preview.png:
   - Left Sidebar (same as SUB_Hist.png)
   - Top action row: Back to {Subject} History, < Previous, Next >
   - Question header: Bold title, date/time, score, verdict badge
   - "Your Answer" card: Candidate transcript
   - "Evaluation Summary" card: 5 interactive tabs (What You Got Right, What's Missing, Misconceptions, Depth Evidence, Reasoning)
   ============================================================================== */
function QuestionPreviewScreen({ subject, questions = [], currentIndex = 0, onBack, onNavigateIndex, onNavigate }) {
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
  const reasoning = ev.reasoning || "Evaluation compiled from authoritative textbook references.";

  return (
    <div className="sub-hist-container">
      {/* Left Sidebar matching mockup/q_sub_full_preview.png */}
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
        {/* Navigation row with Back on left and Prev/Next on right */}
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

        {/* Question Title Header */}
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

        {/* Your Answer Card */}
        <div className="preview-card">
          <h2 className="preview-card-title">Your Answer</h2>
          <div className="preview-answer-body">
            {q.transcript ? q.transcript : <span className="muted" style={{ fontStyle: "italic" }}>No spoken or written transcript recorded for this question.</span>}
          </div>
        </div>

        {/* Evaluation Summary Card */}
        <div className="preview-card">
          <h2 className="preview-card-title">Evaluation Summary</h2>

          {/* 5 Tabs matching mockup/q_sub_full_preview.png */}
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

          {/* Tab Content */}
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

/* ==============================================================================
   PROPS & CHILD COMPONENT: InterviewTopBar
   ------------------------------------------------------------------------------
   Matches topbar in mockup/recording.png + Back arrow on top-left
   ============================================================================== */
function InterviewTopBar({ topic, questionNumber, substep, onBack, onStopInterview }) {
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

/* ==============================================================================
   PROPS & CHILD COMPONENT: InterviewTimeline (Left Column Stepper)
   ------------------------------------------------------------------------------
   Matches 5-step vertical stepper in mockup/recording.png:
   1 Question (Active green circle #155E3E)
   2 Your Answer
   3 Evaluation
   4 Next Question
   5 Complete
   ============================================================================== */
const TIMELINE_STEPS = [
  { step: 1, label: "Question" },
  { step: 2, label: "Your Answer" },
  { step: 3, label: "Evaluation" },
  { step: 4, label: "Next Question" },
  { step: 5, label: "Complete" }
];

function InterviewTimeline({ currentStep }) {
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

/* ==============================================================================
   PROPS & CHILD COMPONENT: WaveformCluster
   ------------------------------------------------------------------------------
   Green vertical audio sound bars matching waveform in mockup/recording.png
   ============================================================================== */
function WaveformCluster({ isRecording, side = "left" }) {
  // Graduated heights peaking near center button
  const baseHeights = [8, 12, 16, 22, 18, 26, 32, 28, 38, 42, 34, 46, 38, 48];
  const heights = side === "left" ? baseHeights : [...baseHeights].reverse();

  return (
    <div className={`waveform-cluster ${isRecording ? "is-recording" : ""}`}>
      {heights.map((h, i) => {
        const opacity = 0.4 + (i / heights.length) * 0.6;
        return (
          <i
            key={i}
            style={{
              height: isRecording ? `${h}px` : `${Math.max(6, Math.floor(h * 0.35))}px`,
              opacity: isRecording ? opacity : 0.45,
              background: isRecording ? "#257853" : "#98A2B3"
            }}
          />
        );
      })}
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: SpeakNaturallyCard (Right Column)
   ------------------------------------------------------------------------------
   Matches right green card in mockup/recording.png:
   - Green mic badge
   - Equalizer signal bars
   - "Speak naturally" title & description
   ============================================================================== */
function SpeakNaturallyCard({ isRecording }) {
  return (
    <div className="iv-info-card">
      <div className="iv-info-header">
        <div className="iv-info-mic-badge">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="23" />
            <line x1="8" y1="23" x2="16" y2="23" />
          </svg>
        </div>
        <div className="iv-info-eq-bars">
          <span style={{ height: isRecording ? "12px" : "6px", transition: "height 0.2s" }} />
          <span style={{ height: isRecording ? "18px" : "10px", transition: "height 0.2s" }} />
          <span style={{ height: isRecording ? "24px" : "16px", transition: "height 0.2s" }} />
          <span style={{ height: isRecording ? "22px" : "20px", transition: "height 0.2s" }} />
          <span style={{ height: isRecording ? "16px" : "14px", transition: "height 0.2s" }} />
          <span style={{ height: isRecording ? "10px" : "8px", transition: "height 0.2s" }} />
        </div>
      </div>

      <h4 className="iv-info-title">Speak naturally</h4>
      <p className="iv-info-desc">
        Make sure the mic is picking up your voice. You can re-record if needed.
      </p>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: QuestionRecordingView
   ------------------------------------------------------------------------------
   EXACT 1-TO-1 MATCH FOR mockup/recording.png:
   - Header with Logo, Breadcrumb, Stop Interview
   - 3-Column Layout:
     1. Left 5-step timeline (Step 1 active)
     2. Center stacked cards:
        - Question Card
        - Voice Box with "Recording... 00:24", Waveform + Red Stop Button
     3. Right "Speak naturally" Info Card
   ============================================================================== */
function QuestionRecordingView({
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
        {/* Top Header Bar */}
        <InterviewTopBar
          topic={topic}
          questionNumber={questionNumber}
          onBack={onBack}
          onStopInterview={onStopInterview}
        />

        {/* 3-Column Grid */}
        <div className="iv-body-grid">
          {/* Left Column: Vertical Timeline */}
          <InterviewTimeline currentStep={1} />

          {/* Center Column: Question Card + Voice Box */}
          <div>
            {/* Question Card (Box 1) */}
            <div className="iv-question-card">
              <h2 className="iv-question-title">
                {questionText || "Preparing your question..."}
              </h2>
            </div>

            {/* Voice Recording Box (Box 2) */}
            <div className="iv-voice-box">
              <div className="iv-voice-status">
                {loading ? (
                  <span className="idle-text" style={{ color: "var(--green)" }}>
                    Transcribing answer with Whisper...
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

              {/* Waveform + Center Button */}
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
                  ? "Transcribing with local Whisper..."
                  : isRecording
                  ? "Click to stop recording"
                  : "Click microphone to start speaking"}
              </div>
            </div>
          </div>

          {/* Right Column: Speak Naturally Card */}
          <SpeakNaturallyCard isRecording={isRecording} />
        </div>
      </div>
    </div>
  );
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: EvaluationStageView (Step 3: "Evaluation")
   ------------------------------------------------------------------------------
   Faithfully implements mockup/Evaluation1.png and mockup/Evaluation2.png:
   - Evaluation1: "Your Transcript" active with Edit button, "Transcript looks good!" banner, "Listen to Audio" button, and "Continue ->" button.
   - Evaluation2: "Evaluation" active with "What You Got Right", "What's Missing", "Misconceptions", "Depth Evidence", "Reasoning" tabs, green checkmarks, "View Source" links, and the bottom "Good start!" banner with sprout illustration.
   - Seamless transition when clicking "Evaluation" on the right of "Your Transcript" or clicking "Continue ->".
   ============================================================================== */
function EvaluationStageView({
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

    let srcUrl = null;
    if (audioBlob) {
      srcUrl = URL.createObjectURL(audioBlob);
    } else if (audioPath && audioPath !== "browser") {
      srcUrl = "/" + audioPath.replace(/^\//, "");
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
    };
  }, []);

  // Handle transition from Evaluation1 -> Evaluation2
  const handleGoToEvaluation = useCallback(async () => {
    if (evaluation) {
      setStage("evaluation");
      return;
    }
    if (onSubmitEvaluation) {
      await onSubmitEvaluation();
      setStage("evaluation");
    }
  }, [evaluation, onSubmitEvaluation]);

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
      const match = evaluation.citations.find(c => c.claim && claimText && c.claim.toLowerCase().includes(claimText.slice(0, 20).toLowerCase()));
      if (match && evaluation.sources) {
        source = evaluation.sources.find(s => s.number === match.source_number);
      }
    }

    if (!source && evaluation?.sources && evaluation.sources.length > 0) {
      source = evaluation.sources[0];
    }

    setActiveSource({
      title: source?.title || `${topic} Authoritative Textbook Standard`,
      section: source?.section || "Core Technical Curriculum Benchmark",
      url: source?.url || null,
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
                          {transcript || "Polymorphism means one interface and multiple implementations. For example, we can have a parent class Animal and child classes like Dog and Cat, and both can have their own implementation of the sound method. We can use a parent reference to call the method and the correct implementation will be invoked."}
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
                        <span>Transcript looks good!</span>
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
                        >
                          View Final Report →
                        </button>
                      ) : (
                        <button
                          type="button"
                          className="btn btn-primary"
                          style={{ padding: "12px 30px" }}
                          onClick={onNextQuestion}
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
                <span className="eyebrow" style={{ color: "var(--green)" }}>Authoritative Reference Benchmark</span>
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
                  This technical answer point was benchmarked against the verified syllabus reference standard.
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
function TranscriptReviewView(props) {
  return <EvaluationStageView {...props} initialStage="transcript" />;
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: EvaluationResultView (Step 3: "Evaluation Result")
   ------------------------------------------------------------------------------
   Renders EvaluationStageView configured for displaying detailed evaluation results.
   ============================================================================== */
function EvaluationResultView(props) {
  return <EvaluationStageView {...props} initialStage="evaluation" />;
}

/* ==============================================================================
   PROPS & CHILD COMPONENT: FinalReportView
   ------------------------------------------------------------------------------
   Props: report, onRestartTopic, onChooseNewTopic, onReturnDashboard
   ============================================================================== */
function FinalReportView({ report, onRestartTopic, onChooseNewTopic, onReturnDashboard }) {
  const readinessVal = report?.readiness || report?.metrics?.overall_readiness || report?.assessment?.readiness_verdict || "DEVELOPING";
  const readiness = formatReadiness(readinessVal);
  const profile = report?.dimension_profile || report?.depth_profile || {};
  const summary = report?.summary || report?.assessment?.summary || "Comprehensive summary generated from grounded textbook evaluations.";
  const questionsCount = report?.questions_answered || report?.metrics?.questions_answered || 5;

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
        <span className="eyebrow">Interview Complete</span>
        <h1 style={{ fontSize: "1.75rem", marginTop: "6px" }}>Candidate Evaluation Report</h1>
        <p className="small muted" style={{ marginTop: "4px" }}>
          {report?.topic || "Technical Interview"} · {questionsCount} questions evaluated
        </p>
      </div>

      {/* Overall Card */}
      <div className="card readiness" style={{ padding: "26px", marginBottom: "20px" }}>
        <h3>Overall Candidate Readiness</h3>
        <div style={{ margin: "14px 0" }}>
          <span className={`pill ${readiness.pill}`} style={{ fontSize: "1rem", padding: "8px 18px" }}>
            {readiness.text}
          </span>
        </div>
        <p className="small muted" style={{ lineHeight: 1.5 }}>
          {summary}
        </p>
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
                  numScore = Math.round(((demonstrated * 1.0 + partial * 0.5) / tested) * 10);
                  displayScore = `${numScore}/10 (${tested} tested)`;
                  pct = Math.min(100, Math.round((numScore / 10) * 100));
                } else {
                  displayScore = "Not Tested";
                  pct = 0;
                }
              } else {
                displayScore = "Demonstrated";
                pct = 70;
              }
            } else {
              displayScore = String(score);
              pct = 50;
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
function App() {
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

  // [HOOK: useCallback] Navigation Handler
  const navigate = useCallback((targetScreen) => {
    setRoute(targetScreen);
    window.scrollTo(0, 0);
  }, []);

  // [HOOK: useCallback] Fetch History (persists guest history in localStorage, DB for registered users)
  const loadHistory = useCallback(async () => {
    if (isGuest) {
      try {
        const guestHist = JSON.parse(localStorage.getItem("crackproof_guest_history") || "[]");
        setHistory(Array.isArray(guestHist) ? guestHist : []);
      } catch (e) {
        setHistory([]);
      }
      return;
    }
    const res = await apiRequest("/api/history");
    if (res.ok && res.interviews) {
      setHistory(res.interviews);
    }
  }, [isGuest]);

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
  const handleGuestLogin = useCallback(() => {
    setUser(null);
    setIsGuest(true);
    navigate("dash");
  }, [navigate]);

  // [HOOK: useCallback] Logout Handler
  const handleLogout = useCallback(async () => {
    await apiRequest("/api/logout", {});
    setUser(null);
    setIsGuest(false);
    dispatch({ type: "RESET" });
    navigate("login");
  }, [navigate]);

  // [HOOK: useCallback] History selection handlers
  const handleSelectHistorySubject = useCallback(async (subjectName) => {
    setSelectedHistorySubject(subjectName);
    setHistoryLoading(true);
    navigate("history_subject");
    const guestHistory = isGuest ? JSON.parse(localStorage.getItem("crackproof_guest_history") || "[]") : [];
    const guestIds = guestHistory.map(g => g.interview_id).filter(Boolean).join(",");
    const url = `/api/history/subject/${encodeURIComponent(subjectName)}${guestIds ? `?guest_ids=${encodeURIComponent(guestIds)}` : ""}`;
    const res = await apiRequest(url);
    setHistoryLoading(false);
    if (res && res.ok) {
      setHistorySubjectQuestions(res.questions || []);
    } else {
      setHistorySubjectQuestions([]);
    }
  }, [navigate, isGuest]);

  const handleSelectHistoryQuestion = useCallback((index) => {
    setSelectedQuestionIndex(index);
    navigate("history_question");
  }, [navigate]);

  // [HOOK: useCallback] Start Interview Topic (Immediate feedback, prevents blank screen)
  const handleStartTopic = useCallback(async (topic) => {
    dispatch({ type: "START_LOADING", payload: { topic } });
    navigate("interview");
    const res = await apiRequest("/api/start", { topic });
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
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      // Auto-detect supported audio recording mimeType across Chrome, Safari, Firefox
      let mimeType = "audio/webm";
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
        // Stop all hardware tracks only after recording completes
        try {
          if (recorder.stream) {
            recorder.stream.getTracks().forEach((track) => track.stop());
          }
        } catch (e) {}

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

        try {
          const res = await fetch("/api/transcribe", { method: "POST", body: formData });
          const data = await res.json();
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
          alert("Transcription server connection error. Please try again.");
          dispatch({ type: "RECORDING_FAILED" });
        }
      };

      // Timeslice of 500ms guarantees chunks stream in smoothly
      recorder.start(500);
      dispatch({ type: "START_RECORDING" });

      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      timerIntervalRef.current = setInterval(() => {
        dispatch({ type: "TICK_TIMER" });
      }, 1000);
    } catch (e) {
      alert("Microphone permission is required to record your technical interview. Please allow microphone access in your browser.");
    }
  }, [interview.interviewId, interview.questionNumber]);

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
    dispatch({ type: "START_EVALUATION" });
    const res = await apiRequest("/api/evaluate", {
      interview_id: interview.interviewId,
      transcript: interview.transcript,
      audio_path: interview.audioPath
    });

    if (res.ok) {
      dispatch({
        type: "SET_EVALUATION",
        payload: {
          evaluation: res.evaluation,
          batchDone: res.batch_complete
        }
      });
    } else {
      alert(res.message || "Evaluation error.");
    }
  }, [interview.interviewId, interview.transcript, interview.audioPath]);

  // [HOOK: useCallback] Next Question Handler
  const handleNextQuestion = useCallback(async () => {
    const res = await apiRequest("/api/next", { interview_id: interview.interviewId });
    if (res.ok) {
      dispatch({
        type: "SET_NEXT_QUESTION",
        payload: {
          questionNumber: res.question_number,
          questionText: res.question
        }
      });
    }
  }, [interview.interviewId]);

  // [HOOK: useCallback] Back from Interview - cleans up audio tracks, resets state, and returns to topics
  const handleBackFromInterview = useCallback(() => {
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
    }
    if (mediaRecorderRef.current) {
      try {
        if (mediaRecorderRef.current.stream) {
          mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
        }
      } catch (e) {}
      try {
        if (mediaRecorderRef.current.state !== "inactive") {
          mediaRecorderRef.current.stop();
        }
      } catch (e) {}
    }
    dispatch({ type: "RESET" });
    navigate("topics");
  }, [navigate]);

  // [HOOK: useCallback] Stop Interview Button - immediate halt, 0ms lag if 0 questions, overlay if finalizing
  const handleStopInterview = useCallback(async () => {
    // 1. Immediately stop audio hardware tracks and clear timers
    if (timerIntervalRef.current) {
      clearInterval(timerIntervalRef.current);
    }
    if (mediaRecorderRef.current) {
      try {
        if (mediaRecorderRef.current.stream) {
          mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
        }
      } catch (e) {}
      try {
        if (mediaRecorderRef.current.state !== "inactive") {
          mediaRecorderRef.current.stop();
        }
      } catch (e) {}
    }

    // 2. If zero completed questions (e.g. on Question 1 before submitting answer), exit instantly with 0ms delay!
    const hasCompletedAnswers = interview.questionNumber > 1 || interview.status === "REVIEW" || interview.status === "EVALUATION";
    if (!interview.interviewId || !hasCompletedAnswers) {
      dispatch({ type: "RESET" });
      navigate("topics");
      return;
    }

    // 3. If >= 1 question answered, show instant stopping overlay and finalize report
    setIsStopping(true);
    try {
      const res = await apiRequest("/api/report", { interview_id: interview.interviewId });
      setIsStopping(false);
      if (res && res.ok) {
        if (isGuest && interview.interviewId) {
          try {
            const prev = JSON.parse(localStorage.getItem("crackproof_guest_history") || "[]");
            prev.unshift({
              interview_id: interview.interviewId,
              topic: interview.topic || "Java",
              questions_answered: res.questions_answered || interview.questionNumber || 1,
              readiness: res?.readiness || "DEVELOPING",
              created_at: new Date().toISOString()
            });
            localStorage.setItem("crackproof_guest_history", JSON.stringify(prev));
          } catch (e) {}
        }
        loadHistory();
        dispatch({ type: "SET_REPORT", payload: res });
        navigate("report");
      } else {
        dispatch({ type: "RESET" });
        navigate("topics");
      }
    } catch (err) {
      setIsStopping(false);
      dispatch({ type: "RESET" });
      navigate("topics");
    }
  }, [interview.interviewId, interview.topic, interview.questionNumber, interview.status, isGuest, loadHistory, navigate]);

  // [HOOK: useCallback] Open Report
  const handleFinishReport = useCallback(async () => {
    const res = await apiRequest("/api/report", { interview_id: interview.interviewId });
    if (res && res.ok) {
      if (isGuest && interview.interviewId) {
        try {
          const prev = JSON.parse(localStorage.getItem("crackproof_guest_history") || "[]");
          prev.unshift({
            interview_id: interview.interviewId,
            topic: interview.topic || "Java",
            questions_answered: res.questions_answered || interview.questionNumber || 1,
            readiness: res?.readiness || "DEVELOPING",
            created_at: new Date().toISOString()
          });
          localStorage.setItem("crackproof_guest_history", JSON.stringify(prev));
        } catch (e) {}
      }
      loadHistory();
      dispatch({ type: "SET_REPORT", payload: res });
      navigate("report");
    } else {
      dispatch({ type: "RESET" });
      navigate("topics");
    }
  }, [interview.interviewId, interview.topic, interview.questionNumber, isGuest, loadHistory, navigate]);

  // [HOOK: useCallback] Open Past Report from Dashboard History
  const handleOpenPastReport = useCallback(async (id) => {
    const res = await apiRequest("/api/report", { interview_id: id });
    if (res.ok) {
      dispatch({ type: "SET_REPORT", payload: res });
      navigate("report");
    }
  }, [navigate]);

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, []);

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
    <div>
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
          onOpenPastReport={handleOpenPastReport}
        />
      )}

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
