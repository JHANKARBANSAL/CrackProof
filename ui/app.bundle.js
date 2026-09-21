(() => {
  // ui/src/api/client.js
  async function apiRequest(path, data = null) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 18e4);
    const options = { method: data ? "POST" : "GET" };
    options.signal = controller.signal;
    if (data) {
      options.headers = { "Content-Type": "application/json" };
      options.body = JSON.stringify(data);
    }
    try {
      const res = await fetch(path, options);
      const body = await res.json();
      if (!body || typeof body !== "object" || Array.isArray(body)) throw new Error("Invalid response");
      return res.ok ? body : { ...body, ok: false };
    } catch (err) {
      return {
        ok: false,
        message: err.name === "AbortError" ? "The request took too long. Please try again." : "Could not reach the server. Please check your connection and try again."
      };
    } finally {
      clearTimeout(timeout);
    }
  }
  function formatReadiness(val) {
    if (val === "STRONG" || val === "READY") return { text: "Strong", pill: "pill-g" };
    if (val === "DEVELOPING" || val === "ALMOST_READY") return { text: "Developing", pill: "pill-a" };
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

  // ui/src/state/interviewReducer.js
  var initialInterviewState = {
    status: "IDLE",
    // 'IDLE' | 'LOADING' | 'QUESTION' | 'RECORDING' | 'REVIEW' | 'EVALUATION' | 'REPORT'
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

  // ui/src/components/Icon.jsx
  var React = window.React;
  function Icon({ name, size = 20, className = "" }) {
    return /* @__PURE__ */ React.createElement("img", { className: `ui-icon ${className}`, src: `/Images/icons/${name}.svg`, alt: "", "aria-hidden": "true", width: size, height: size });
  }

  // ui/src/components/WorkspaceNav.jsx
  var React2 = window.React;
  var links = [
    ["dash", "Overview", "layout-dashboard"],
    ["topics", "Knowledge practice", "book-open"],
    ["panel", "AI interview panel", "audio-lines"],
    ["profile", "My profile", "contact-round"],
    ["progress", "My progress", "chart-no-axes-combined"],
    ["history", "Practice history", "history"]
  ];
  function WorkspaceNav({ user, isGuest, activeRoute, onNavigate, onLogout }) {
    const name = isGuest ? "Guest" : user?.name || user?.email?.split("@")[0] || "Candidate";
    return /* @__PURE__ */ React2.createElement(React2.Fragment, null, /* @__PURE__ */ React2.createElement("aside", { className: "workspace-sidebar" }, /* @__PURE__ */ React2.createElement("button", { className: "workspace-brand", onClick: () => onNavigate("dash"), "aria-label": "CrackProof home" }, /* @__PURE__ */ React2.createElement("img", { src: "/Images/logo.png", alt: "CrackProof" }), /* @__PURE__ */ React2.createElement("span", null, "INTERVIEW STUDIO")), /* @__PURE__ */ React2.createElement("span", { className: "sidebar-caption" }, "YOUR WORKSPACE"), /* @__PURE__ */ React2.createElement("nav", { "aria-label": "Main navigation" }, links.map(([route, label, icon]) => /* @__PURE__ */ React2.createElement("button", { key: route, "aria-current": activeRoute === route ? "page" : void 0, className: activeRoute === route ? "active" : "", onClick: () => onNavigate(route) }, /* @__PURE__ */ React2.createElement(Icon, { name: icon }), /* @__PURE__ */ React2.createElement("span", null, label), route === "panel" && /* @__PURE__ */ React2.createElement("span", { className: "nav-new" }, "AI")))), /* @__PURE__ */ React2.createElement("div", { className: "sidebar-tip" }, /* @__PURE__ */ React2.createElement(Icon, { name: "sparkles", size: 22 }), /* @__PURE__ */ React2.createElement("strong", null, "A little practice.", /* @__PURE__ */ React2.createElement("br", null), "A lot more confidence."), /* @__PURE__ */ React2.createElement("p", null, "Bring your experience. Find your next step."), /* @__PURE__ */ React2.createElement("button", { onClick: () => onNavigate("profile") }, "Build your profile ", /* @__PURE__ */ React2.createElement(Icon, { name: "arrow-up-right", size: 16 }))), /* @__PURE__ */ React2.createElement("div", { className: "sidebar-account" }, /* @__PURE__ */ React2.createElement("div", { className: "avatar" }, name[0].toUpperCase()), /* @__PURE__ */ React2.createElement("div", null, /* @__PURE__ */ React2.createElement("strong", null, name), /* @__PURE__ */ React2.createElement("small", null, isGuest ? "Guest workspace" : "Personal workspace")), /* @__PURE__ */ React2.createElement("button", { onClick: onLogout, title: "Sign out", "aria-label": "Sign out" }, /* @__PURE__ */ React2.createElement(Icon, { name: "log-out", size: 18 })))), /* @__PURE__ */ React2.createElement("header", { className: "workspace-topbar" }, /* @__PURE__ */ React2.createElement("div", null, /* @__PURE__ */ React2.createElement("span", { className: "muted" }, "Workspace"), /* @__PURE__ */ React2.createElement("span", { className: "topbar-slash" }, "/"), /* @__PURE__ */ React2.createElement("strong", null, links.find((item) => item[0] === activeRoute)?.[1] || "Practice report")), /* @__PURE__ */ React2.createElement("span", { className: "workspace-mode" }, /* @__PURE__ */ React2.createElement("span", null), isGuest ? "Guest mode" : "Your practice space")));
  }

  // ui/src/screens/auth/LoginScreen.jsx
  var React3 = window.React;
  var { useState } = React3;
  function LoginScreen({ onLogin, onSwitchToSignup, onGuestLogin }) {
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
    return /* @__PURE__ */ React3.createElement("div", { className: "auth-screen" }, /* @__PURE__ */ React3.createElement("div", { className: "auth-container" }, /* @__PURE__ */ React3.createElement("div", { className: "auth-card" }, /* @__PURE__ */ React3.createElement("div", { className: "auth-brand" }, /* @__PURE__ */ React3.createElement("img", { src: "/Images/logo.png", alt: "CrackProof Logo", className: "auth-logo" }), /* @__PURE__ */ React3.createElement("p", { className: "auth-tagline" }, "Practice. Understand. Improve.")), /* @__PURE__ */ React3.createElement("h1", { className: "auth-title" }, "Your next chapter", /* @__PURE__ */ React3.createElement("br", null), "starts here."), /* @__PURE__ */ React3.createElement("p", { className: "auth-subtitle" }, "Sign in to your interview workspace."), /* @__PURE__ */ React3.createElement("form", { onSubmit: handleSubmit }, /* @__PURE__ */ React3.createElement("div", { className: "auth-field" }, /* @__PURE__ */ React3.createElement("label", { htmlFor: "loginEmail" }, "Email"), /* @__PURE__ */ React3.createElement("div", { className: "input-wrap" }, /* @__PURE__ */ React3.createElement("svg", { className: "input-icon", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React3.createElement("path", { d: "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" }), /* @__PURE__ */ React3.createElement("polyline", { points: "22,6 12,13 2,6" })), /* @__PURE__ */ React3.createElement(
      "input",
      {
        id: "loginEmail",
        className: "inp",
        type: "email",
        placeholder: "you@example.com",
        autoComplete: "email",
        value: email,
        onChange: (e) => setEmail(e.target.value)
      }
    ))), /* @__PURE__ */ React3.createElement("div", { className: "auth-field" }, /* @__PURE__ */ React3.createElement("label", { htmlFor: "loginPw" }, "Password"), /* @__PURE__ */ React3.createElement("div", { className: "input-wrap" }, /* @__PURE__ */ React3.createElement("svg", { className: "input-icon", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React3.createElement("rect", { x: "3", y: "11", width: "18", height: "11", rx: "2", ry: "2" }), /* @__PURE__ */ React3.createElement("path", { d: "M7 11V7a5 5 0 0 1 10 0v4" })), /* @__PURE__ */ React3.createElement(
      "input",
      {
        id: "loginPw",
        className: "inp",
        type: "password",
        placeholder: "Your password",
        autoComplete: "current-password",
        value: password,
        onChange: (e) => setPassword(e.target.value)
      }
    ))), error && /* @__PURE__ */ React3.createElement("p", { className: "formError" }, error), /* @__PURE__ */ React3.createElement("button", { type: "submit", className: "btn-signin", disabled: loading }, loading ? "Signing In..." : "Sign In")), /* @__PURE__ */ React3.createElement("div", { className: "auth-divider" }, /* @__PURE__ */ React3.createElement("span", null, "or")), /* @__PURE__ */ React3.createElement("button", { type: "button", className: "btn-guest", onClick: onGuestLogin }, /* @__PURE__ */ React3.createElement("svg", { width: "17", height: "17", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React3.createElement("path", { d: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" }), /* @__PURE__ */ React3.createElement("circle", { cx: "12", cy: "7", r: "4" })), "Continue as Guest"), /* @__PURE__ */ React3.createElement("p", { className: "auth-footer" }, "Don't have an account?", " ", /* @__PURE__ */ React3.createElement("a", { href: "#", onClick: (e) => {
      e.preventDefault();
      onSwitchToSignup(email);
    } }, "Sign up"))), /* @__PURE__ */ React3.createElement("div", { className: "auth-illustration" }, /* @__PURE__ */ React3.createElement("span", { className: "eyebrow" }, "PRACTICE FOR WHAT'S NEXT"), /* @__PURE__ */ React3.createElement("h2", null, "Good preparation.", /* @__PURE__ */ React3.createElement("br", null), "A different kind of confidence."), /* @__PURE__ */ React3.createElement("img", { src: "/Images/interview-desk.png", alt: "A laptop and conversation tools for interview preparation" }), /* @__PURE__ */ React3.createElement("p", null, "Core concepts. Your own story. A panel that challenges you."))));
  }

  // ui/src/screens/auth/SignupScreen.jsx
  var React4 = window.React;
  var { useState: useState2 } = React4;
  function SignupScreen({ onSignup, onSwitchToLogin, initialEmail = "" }) {
    const [name, setName] = useState2("");
    const [email, setEmail] = useState2(initialEmail);
    const [password, setPassword] = useState2("");
    const [loading, setLoading] = useState2(false);
    const [error, setError] = useState2("");
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
    return /* @__PURE__ */ React4.createElement("div", { className: "auth-screen" }, /* @__PURE__ */ React4.createElement("div", { className: "auth-container" }, /* @__PURE__ */ React4.createElement("div", { className: "auth-card" }, /* @__PURE__ */ React4.createElement("div", { className: "auth-brand" }, /* @__PURE__ */ React4.createElement("img", { src: "/Images/logo.png", alt: "CrackProof Logo", className: "auth-logo" }), /* @__PURE__ */ React4.createElement("p", { className: "auth-tagline" }, "Practice. Understand. Improve.")), /* @__PURE__ */ React4.createElement("h1", { className: "auth-title" }, "Create Account"), /* @__PURE__ */ React4.createElement("p", { className: "auth-subtitle" }, "Join CrackProof to save and track your progress"), /* @__PURE__ */ React4.createElement("form", { onSubmit: handleSubmit }, /* @__PURE__ */ React4.createElement("div", { className: "auth-field" }, /* @__PURE__ */ React4.createElement("label", { htmlFor: "signupName" }, "Full Name"), /* @__PURE__ */ React4.createElement("div", { className: "input-wrap" }, /* @__PURE__ */ React4.createElement("svg", { className: "input-icon", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React4.createElement("path", { d: "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" }), /* @__PURE__ */ React4.createElement("circle", { cx: "12", cy: "7", r: "4" })), /* @__PURE__ */ React4.createElement(
      "input",
      {
        id: "signupName",
        className: "inp",
        type: "text",
        placeholder: "Your Name",
        autoComplete: "name",
        value: name,
        onChange: (e) => setName(e.target.value)
      }
    ))), /* @__PURE__ */ React4.createElement("div", { className: "auth-field" }, /* @__PURE__ */ React4.createElement("label", { htmlFor: "signupEmail" }, "Email"), /* @__PURE__ */ React4.createElement("div", { className: "input-wrap" }, /* @__PURE__ */ React4.createElement("svg", { className: "input-icon", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React4.createElement("path", { d: "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" }), /* @__PURE__ */ React4.createElement("polyline", { points: "22,6 12,13 2,6" })), /* @__PURE__ */ React4.createElement(
      "input",
      {
        id: "signupEmail",
        className: "inp",
        type: "email",
        placeholder: "you@example.com",
        autoComplete: "email",
        value: email,
        onChange: (e) => setEmail(e.target.value)
      }
    ))), /* @__PURE__ */ React4.createElement("div", { className: "auth-field" }, /* @__PURE__ */ React4.createElement("label", { htmlFor: "signupPw" }, "Password"), /* @__PURE__ */ React4.createElement("div", { className: "input-wrap" }, /* @__PURE__ */ React4.createElement("svg", { className: "input-icon", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React4.createElement("rect", { x: "3", y: "11", width: "18", height: "11", rx: "2", ry: "2" }), /* @__PURE__ */ React4.createElement("path", { d: "M7 11V7a5 5 0 0 1 10 0v4" })), /* @__PURE__ */ React4.createElement(
      "input",
      {
        id: "signupPw",
        className: "inp",
        type: "password",
        placeholder: "At least 6 characters",
        autoComplete: "new-password",
        value: password,
        onChange: (e) => setPassword(e.target.value)
      }
    ))), error && /* @__PURE__ */ React4.createElement("p", { className: "formError" }, error), /* @__PURE__ */ React4.createElement("button", { type: "submit", className: "btn-signin", disabled: loading }, loading ? "Creating Account..." : "Sign Up")), /* @__PURE__ */ React4.createElement("p", { className: "auth-footer" }, "Already have an account?", " ", /* @__PURE__ */ React4.createElement("a", { href: "#", onClick: (e) => {
      e.preventDefault();
      onSwitchToLogin();
    } }, "Sign in"))), /* @__PURE__ */ React4.createElement("div", { className: "auth-illustration" }, /* @__PURE__ */ React4.createElement("span", { className: "eyebrow" }, "YOUR NEXT CHAPTER STARTS HERE"), /* @__PURE__ */ React4.createElement("h2", null, "Turn practice into", /* @__PURE__ */ React4.createElement("br", null), "your next opportunity."), /* @__PURE__ */ React4.createElement("img", { src: "/Images/interview-desk.png", alt: "An illustrated interview workspace with a laptop and a confidence checkmark" }), /* @__PURE__ */ React4.createElement("p", null, "Build your profile. Practice your skills. Find your voice."))));
  }

  // ui/src/screens/dashboard/DashboardScreen.jsx
  var React5 = window.React;
  function DashboardScreen({ user, isGuest, history = [], onStartInterview, onOpenPastReport, onSetupInterview, onOpenPanel }) {
    const name = isGuest ? "there" : user?.name?.split(" ")[0] || "there";
    const answers = history.reduce((sum, item) => sum + (item.questions_answered || 0), 0);
    const subjects = new Set(history.map((item) => item.topic)).size;
    return /* @__PURE__ */ React5.createElement("main", { className: "wrap overview-page" }, /* @__PURE__ */ React5.createElement("div", { className: "page-intro" }, /* @__PURE__ */ React5.createElement("div", null, /* @__PURE__ */ React5.createElement("span", { className: "eyebrow" }, "YOUR NEXT CHAPTER"), /* @__PURE__ */ React5.createElement("h1", null, "Let's make you interview-ready."), /* @__PURE__ */ React5.createElement("p", { className: "muted" }, "Hey ", name, ", one good practice session can change your next conversation.")), /* @__PURE__ */ React5.createElement("button", { className: "btn btn-secondary", onClick: onSetupInterview }, /* @__PURE__ */ React5.createElement(Icon, { name: "contact-round", size: 17 }), " My profile")), /* @__PURE__ */ React5.createElement("section", { className: "studio-hero" }, /* @__PURE__ */ React5.createElement("div", { className: "studio-hero-copy" }, /* @__PURE__ */ React5.createElement("span", { className: "hero-kicker" }, /* @__PURE__ */ React5.createElement(Icon, { name: "sparkles", size: 16 }), " YOUR SPACE TO GET BETTER"), /* @__PURE__ */ React5.createElement("h2", null, "Big ambitions.", /* @__PURE__ */ React5.createElement("br", null), "Better preparation."), /* @__PURE__ */ React5.createElement("p", null, "Find the gaps. Tell your story. Walk into your next interview with more confidence."), /* @__PURE__ */ React5.createElement("button", { className: "btn btn-lime", onClick: onStartInterview }, "Start practicing ", /* @__PURE__ */ React5.createElement(Icon, { name: "arrow-up-right", size: 19 })), /* @__PURE__ */ React5.createElement("span", { className: "hero-footnote" }, "Your pace. Your progress.")), /* @__PURE__ */ React5.createElement("div", { className: "studio-hero-art" }, /* @__PURE__ */ React5.createElement("img", { src: "/Images/interview-desk.png", alt: "A sculptural laptop and conversation tools on a desk" }), /* @__PURE__ */ React5.createElement("span", { className: "art-caption" }, /* @__PURE__ */ React5.createElement(Icon, { name: "check-check", size: 17 }), " Practice with purpose"))), /* @__PURE__ */ React5.createElement("div", { className: "overview-stats" }, [["message-circle", answers, "Questions practiced", "Knowledge practice"], ["book-open", subjects, "Subjects explored", "Across your saved interviews"], ["history", history.length, "Interview sessions", "With evaluated answers"]].map(([icon, count, label, hint]) => /* @__PURE__ */ React5.createElement("div", { className: "stat-tile", key: label }, /* @__PURE__ */ React5.createElement("span", { className: "stat-icon" }, /* @__PURE__ */ React5.createElement(Icon, { name: icon })), /* @__PURE__ */ React5.createElement("div", null, /* @__PURE__ */ React5.createElement("span", { className: "stat-value" }, count), /* @__PURE__ */ React5.createElement("strong", null, label), /* @__PURE__ */ React5.createElement("small", null, hint))))), /* @__PURE__ */ React5.createElement("div", { className: "section-title" }, /* @__PURE__ */ React5.createElement("div", null, /* @__PURE__ */ React5.createElement("span", { className: "eyebrow" }, "TWO WAYS TO PREPARE"), /* @__PURE__ */ React5.createElement("h2", null, "What would you like to work on?")), /* @__PURE__ */ React5.createElement("span", { className: "small muted" }, "Different skills. One goal.")), /* @__PURE__ */ React5.createElement("div", { className: "practice-modes" }, /* @__PURE__ */ React5.createElement("section", { className: "practice-mode knowledge-mode" }, /* @__PURE__ */ React5.createElement("div", { className: "mode-heading" }, /* @__PURE__ */ React5.createElement("span", { className: "mode-icon" }, /* @__PURE__ */ React5.createElement(Icon, { name: "book-open", size: 24 })), /* @__PURE__ */ React5.createElement("span", { className: "mode-label" }, "BUILD YOUR FOUNDATION")), /* @__PURE__ */ React5.createElement("h3", null, "Know it. Explain it."), /* @__PURE__ */ React5.createElement("p", null, "Practice core CS concepts and understand the reasoning behind every evaluation."), /* @__PURE__ */ React5.createElement("div", { className: "mode-tags" }, /* @__PURE__ */ React5.createElement("span", null, "6 CS subjects"), /* @__PURE__ */ React5.createElement("span", null, "Source-backed feedback")), /* @__PURE__ */ React5.createElement("button", { onClick: onStartInterview }, "Explore knowledge practice ", /* @__PURE__ */ React5.createElement(Icon, { name: "arrow-right", size: 19 }))), /* @__PURE__ */ React5.createElement("section", { className: "practice-mode persona-mode" }, /* @__PURE__ */ React5.createElement("div", { className: "mode-heading" }, /* @__PURE__ */ React5.createElement("span", { className: "mode-icon" }, /* @__PURE__ */ React5.createElement(Icon, { name: "audio-lines", size: 24 })), /* @__PURE__ */ React5.createElement("span", { className: "mode-label" }, "PUT YOURSELF IN THE ROOM")), /* @__PURE__ */ React5.createElement("h3", null, "Your story. Meet the panel."), /* @__PURE__ */ React5.createElement("p", null, "Discuss your skills and projects with technical, project and hiring interviewer personas."), /* @__PURE__ */ React5.createElement("div", { className: "mode-tags" }, /* @__PURE__ */ React5.createElement("span", null, "Resume-aware"), /* @__PURE__ */ React5.createElement("span", null, "Voice or text")), /* @__PURE__ */ React5.createElement("button", { onClick: onOpenPanel }, "Meet your AI panel ", /* @__PURE__ */ React5.createElement(Icon, { name: "arrow-right", size: 19 })))), /* @__PURE__ */ React5.createElement("div", { className: "overview-bottom" }, /* @__PURE__ */ React5.createElement("section", { className: "recent-sessions" }, /* @__PURE__ */ React5.createElement("div", { className: "section-title" }, /* @__PURE__ */ React5.createElement("h2", null, "Pick up your progress"), /* @__PURE__ */ React5.createElement("span", { className: "small muted" }, "Knowledge practice")), !history.length ? /* @__PURE__ */ React5.createElement("div", { className: "empty-studio" }, /* @__PURE__ */ React5.createElement("span", { className: "empty-studio-icon" }, /* @__PURE__ */ React5.createElement(Icon, { name: "history", size: 30 })), /* @__PURE__ */ React5.createElement("h3", null, "Your first session is a fresh start."), /* @__PURE__ */ React5.createElement("p", null, "Your questions, feedback and next steps will appear here."), /* @__PURE__ */ React5.createElement("button", { className: "btn btn-secondary", onClick: onStartInterview }, "Start your first interview ", /* @__PURE__ */ React5.createElement(Icon, { name: "arrow-right", size: 16 }))) : /* @__PURE__ */ React5.createElement("div", { className: "recent-list" }, history.slice(0, 4).map((row) => /* @__PURE__ */ React5.createElement("button", { key: row.interview_id, onClick: () => onOpenPastReport(row.interview_id) }, /* @__PURE__ */ React5.createElement("span", { className: "stat-icon" }, /* @__PURE__ */ React5.createElement(Icon, { name: "book-open" })), /* @__PURE__ */ React5.createElement("span", null, /* @__PURE__ */ React5.createElement("strong", null, row.topic), /* @__PURE__ */ React5.createElement("small", null, row.created_at?.slice(0, 10), " \xB7 ", row.questions_answered || 0, " answers")), /* @__PURE__ */ React5.createElement(Icon, { name: "arrow-up-right", size: 18 }))))), /* @__PURE__ */ React5.createElement("aside", { className: "prep-path" }, /* @__PURE__ */ React5.createElement("span", { className: "eyebrow" }, "A SIMPLE WAY FORWARD"), /* @__PURE__ */ React5.createElement("h2", null, "Your preparation path"), [["01", "Make it personal", "Set your role and add your experience.", onSetupInterview], ["02", "Strengthen the basics", "Practice concepts and close the gaps.", onStartInterview], ["03", "Bring it all together", "Put your answers in front of the panel.", onOpenPanel]].map(([number, title, detail, action]) => /* @__PURE__ */ React5.createElement("button", { key: number, onClick: action }, /* @__PURE__ */ React5.createElement("span", null, number), /* @__PURE__ */ React5.createElement("div", null, /* @__PURE__ */ React5.createElement("strong", null, title), /* @__PURE__ */ React5.createElement("small", null, detail)), /* @__PURE__ */ React5.createElement(Icon, { name: "chevron-right", size: 16 }))))), isGuest && /* @__PURE__ */ React5.createElement("p", { className: "guest-footnote" }, /* @__PURE__ */ React5.createElement(Icon, { name: "shield-check", size: 16 }), " You're in a guest workspace. Your saved practice is linked to this browser session."));
  }

  // ui/src/components/RolePicker.jsx
  var React6 = window.React;
  var { useState: useState3, useId, useRef, useEffect } = React6;
  var TARGET_ROLES = ["Software Engineer", "Frontend Developer", "Backend Developer", "Full Stack Developer", "Java Developer", "Python Developer", "Mobile App Developer", "Data Analyst", "Data Engineer", "Data Scientist", "Machine Learning Engineer", "AI Engineer", "DevOps Engineer", "Cloud Engineer", "QA / Test Engineer", "Cybersecurity Analyst", "Product Manager", "UI / UX Designer"];
  function RolePicker({ value, onChange }) {
    const [open, setOpen] = useState3(false);
    const [active, setActive] = useState3(-1);
    const [showAll, setShowAll] = useState3(false);
    const id = useId();
    const pickerRef = useRef(null);
    useEffect(() => {
      if (open && active >= 0) pickerRef.current?.querySelectorAll('[role="option"]')[active]?.scrollIntoView({ block: "nearest" });
    }, [active, open]);
    const matches = TARGET_ROLES.filter((role) => showAll || role.toLowerCase().includes(value.trim().toLowerCase()));
    const custom = value.trim() && !TARGET_ROLES.some((role) => role.toLowerCase() === value.trim().toLowerCase());
    const options = [...matches, ...custom ? [value.trim()] : []];
    function choose(role) {
      onChange(role);
      setOpen(false);
      setActive(-1);
    }
    return /* @__PURE__ */ React6.createElement("div", { className: "role-picker", ref: pickerRef, onBlur: (event) => {
      if (!event.currentTarget.contains(event.relatedTarget)) setOpen(false);
    } }, /* @__PURE__ */ React6.createElement("label", { htmlFor: id }, "Target role ", /* @__PURE__ */ React6.createElement("span", { className: "required-mark" }, "*")), /* @__PURE__ */ React6.createElement("div", { className: "role-input" }, /* @__PURE__ */ React6.createElement(Icon, { name: "briefcase-business" }), /* @__PURE__ */ React6.createElement("input", { id, value, required: true, maxLength: 120, pattern: ".*\\S.*", placeholder: "Search or enter your target role", role: "combobox", "aria-autocomplete": "list", "aria-expanded": open, "aria-controls": `${id}-options`, "aria-activedescendant": open && active >= 0 ? `${id}-${active}` : void 0, autoComplete: "off", onFocus: () => setOpen(true), onChange: (event) => {
      onChange(event.target.value);
      setShowAll(false);
      setOpen(true);
      setActive(-1);
    }, onKeyDown: (event) => {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        setOpen(true);
        setActive((index) => event.key === "ArrowDown" ? Math.min(index + 1, options.length - 1) : Math.max(index - 1, 0));
      }
      if (event.key === "Enter" && open) {
        event.preventDefault();
        if (options[active >= 0 ? active : 0]) choose(options[active >= 0 ? active : 0]);
      }
      if (event.key === "Escape") {
        event.preventDefault();
        setOpen(false);
      }
    } }), /* @__PURE__ */ React6.createElement("button", { type: "button", "aria-label": "Show target roles", "aria-expanded": open, onClick: () => {
      setShowAll(true);
      setOpen(!open);
      setActive(-1);
    } }, /* @__PURE__ */ React6.createElement(Icon, { name: "chevron-down", size: 18 }))), open && /* @__PURE__ */ React6.createElement("div", { className: "role-options", id: `${id}-options`, role: "listbox", "aria-label": "Target roles" }, /* @__PURE__ */ React6.createElement("div", { className: "role-options-label", role: "presentation" }, value && !showAll ? "MATCHING ROLES" : "POPULAR PLACEMENT ROLES"), options.map((role, index) => /* @__PURE__ */ React6.createElement("div", { role: "option", id: `${id}-${index}`, key: role, "aria-selected": index === active, onMouseDown: (event) => event.preventDefault(), onClick: () => choose(role), className: index === active ? "selected" : "" }, /* @__PURE__ */ React6.createElement("span", null, role), custom && index === options.length - 1 ? /* @__PURE__ */ React6.createElement("small", null, "Custom role") : /* @__PURE__ */ React6.createElement(Icon, { name: "arrow-up-right", size: 15 })))), /* @__PURE__ */ React6.createElement("p", { className: "field-hint" }, "Choose a role or type your own. Your interview will adapt to this goal."));
  }

  // ui/src/screens/dashboard/ResumeSetupScreen.jsx
  var React7 = window.React;
  var { useEffect: useEffect2, useRef: useRef2, useState: useState4 } = React7;
  var emptyProfile = {
    target_role: "",
    experience_level: "Fresher",
    job_description: "",
    skills: [],
    projects: [],
    education: "",
    work_summary: ""
  };
  function ResumeSetupScreen({ isGuest, onPractice, onPanel }) {
    const [profile, setProfile] = useState4(emptyProfile);
    const [skillsText, setSkillsText] = useState4("");
    const [step, setStep] = useState4(0);
    const [loading, setLoading] = useState4(true);
    const [loadFailed, setLoadFailed] = useState4(false);
    const [busy, setBusy] = useState4(false);
    const [error, setError] = useState4("");
    const [notice, setNotice] = useState4("");
    const [file, setFile] = useState4(null);
    const [extracted, setExtracted] = useState4(null);
    const [saved, setSaved] = useState4(false);
    const [jdReview, setJdReview] = useState4(null);
    const [reviewingJD, setReviewingJD] = useState4(false);
    const uploadController = useRef2(null);
    const mounted = useRef2(true);
    const busyRef = useRef2(false);
    useEffect2(() => {
      mounted.current = true;
      loadProfile();
      return () => {
        mounted.current = false;
        uploadController.current?.abort();
      };
    }, []);
    async function loadProfile() {
      setLoading(true);
      const result = await apiRequest("/api/profile");
      if (!mounted.current) return;
      setLoadFailed(!result.ok);
      setError(result.ok ? "" : result.message);
      if (result.ok && result.profile) {
        setProfile(result.profile);
        setSkillsText(result.profile.skills.join(", "));
        setNotice("Your saved setup is ready to review or update.");
      }
      setLoading(false);
    }
    function update(field, value) {
      setProfile((previous) => ({ ...previous, [field]: value }));
      setSaved(false);
      if (field === "target_role" || field === "job_description") setJdReview(null);
    }
    async function checkDescription() {
      if (busyRef.current) return;
      busyRef.current = true;
      setBusy(true);
      setReviewingJD(true);
      setError("");
      const result = await apiRequest("/api/profile/job-description", { target_role: profile.target_role, job_description: profile.job_description });
      busyRef.current = false;
      if (!mounted.current) return;
      setBusy(false);
      setReviewingJD(false);
      if (result.ok) setJdReview(result.review);
      else setError(result.message);
    }
    async function analyzeResume() {
      if (!file || busyRef.current) return;
      if (file.size > 5 * 1024 * 1024) {
        setError("Please select a PDF smaller than 5 MB.");
        return;
      }
      busyRef.current = true;
      setBusy(true);
      setError("");
      setExtracted(null);
      const controller = new AbortController();
      uploadController.current = controller;
      const timeout = setTimeout(() => controller.abort(), 18e4);
      try {
        const body = new FormData();
        body.append("resume", file);
        const response = await fetch("/api/resume/parse", { method: "POST", body, signal: controller.signal });
        if (response.status === 413) throw new Error("Please select a smaller PDF.");
        const result = await response.json();
        if (!response.ok || !result.ok) throw new Error(result.message || "Could not analyze this resume.");
        if (mounted.current) setExtracted(result.details);
      } catch (error2) {
        if (mounted.current) setError(error2.name === "AbortError" ? "Analysis timed out. Retry or enter details manually." : error2.message);
      } finally {
        clearTimeout(timeout);
        uploadController.current = null;
        busyRef.current = false;
        if (mounted.current) setBusy(false);
      }
    }
    function applyExtracted() {
      setProfile((previous) => ({ ...previous, ...extracted }));
      setSkillsText(extracted.skills.join(", "));
      setExtracted(null);
      setSaved(false);
      setNotice("Resume details added to the form. Check and correct them before saving.");
    }
    function next(event) {
      event.preventDefault();
      setError("");
      if (step === 1) {
        const skills = [...new Set(skillsText.split(",").map((value) => value.trim()).filter(Boolean))];
        if (!skills.length || skills.length > 30 || skills.some((value) => value.length > 120)) {
          setError("Enter 1\u201330 skills, separated by commas. Keep each skill under 120 characters.");
          return;
        }
        update("skills", skills);
      }
      setStep(step + 1);
      window.scrollTo(0, 0);
    }
    async function save() {
      if (busyRef.current) return;
      busyRef.current = true;
      setBusy(true);
      setError("");
      const result = await apiRequest("/api/profile", profile);
      busyRef.current = false;
      if (!mounted.current) return;
      setBusy(false);
      if (!result.ok) {
        setError(result.message);
        return;
      }
      setNotice("");
      setSaved(true);
      setProfile(result.profile);
      setSkillsText(result.profile.skills.join(", "));
    }
    if (loading) return /* @__PURE__ */ React7.createElement("div", { className: "wrap", role: "status" }, "Loading your interview setup\u2026");
    if (loadFailed) return /* @__PURE__ */ React7.createElement("div", { className: "wrap" }, /* @__PURE__ */ React7.createElement("p", { role: "alert" }, error), /* @__PURE__ */ React7.createElement("button", { className: "btn btn-primary", onClick: loadProfile }, "Retry loading setup"));
    return /* @__PURE__ */ React7.createElement("main", { className: "wrap setup-page" }, /* @__PURE__ */ React7.createElement("div", { className: "setup-heading" }, /* @__PURE__ */ React7.createElement("span", { className: "eyebrow" }, "MAKE IT PERSONAL"), /* @__PURE__ */ React7.createElement("h1", null, "Your ambition. Your interview."), /* @__PURE__ */ React7.createElement("p", { className: "muted" }, "A little context helps us ask the right questions.")), /* @__PURE__ */ React7.createElement("ol", { className: "setup-steps", "aria-label": "Setup progress" }, ["Your goal", "Resume & skills", "Review & save"].map((label, index) => /* @__PURE__ */ React7.createElement("li", { key: label, "aria-current": step === index ? "step" : void 0, className: step === index ? "active" : "" }, /* @__PURE__ */ React7.createElement("span", null, index + 1), label))), error && /* @__PURE__ */ React7.createElement("p", { className: "formError", role: "alert" }, error), notice && /* @__PURE__ */ React7.createElement("p", { className: "setup-notice", role: "status" }, notice), /* @__PURE__ */ React7.createElement("div", { className: "profile-layout" }, /* @__PURE__ */ React7.createElement("form", { onSubmit: next, className: "card setup-card" }, /* @__PURE__ */ React7.createElement("fieldset", { disabled: busy, className: "setup-fields" }, step === 0 && /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("div", { className: "form-section-heading" }, /* @__PURE__ */ React7.createElement("span", { className: "section-icon" }, /* @__PURE__ */ React7.createElement(Icon, { name: "target" })), /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement("h2", null, "Set your direction"), /* @__PURE__ */ React7.createElement("p", { className: "muted" }, "Tell us where you want to go."))), /* @__PURE__ */ React7.createElement(RolePicker, { value: profile.target_role, onChange: (value) => update("target_role", value) }), /* @__PURE__ */ React7.createElement("label", null, "Experience ", /* @__PURE__ */ React7.createElement("select", { className: "inp", value: profile.experience_level, onChange: (event) => update("experience_level", event.target.value) }, ["Fresher", "0\u20132 years", "3\u20135 years", "5+ years"].map((level) => /* @__PURE__ */ React7.createElement("option", { key: level }, level)))), /* @__PURE__ */ React7.createElement("div", { className: "jd-block" }, /* @__PURE__ */ React7.createElement("label", { htmlFor: "job-description" }, "Have a specific job in mind? ", /* @__PURE__ */ React7.createElement("span", { className: "optional-tag" }, "OPTIONAL")), /* @__PURE__ */ React7.createElement("p", { className: "field-hint" }, "Paste its description to focus your panel on the actual responsibilities and skills."), /* @__PURE__ */ React7.createElement("textarea", { id: "job-description", className: "inp", rows: 5, maxLength: 8e3, value: profile.job_description, onChange: (event) => update("job_description", event.target.value), placeholder: "Paste responsibilities, required skills and experience from the job posting\u2026" }), /* @__PURE__ */ React7.createElement("div", { className: "jd-action-row" }, /* @__PURE__ */ React7.createElement("button", { className: "btn btn-secondary", type: "button", disabled: !profile.target_role.trim() || !profile.job_description.trim() || busy, onClick: checkDescription }, /* @__PURE__ */ React7.createElement(Icon, { name: "sparkles", size: 16 }), reviewingJD ? "Reviewing description\u2026" : "Check job description"), /* @__PURE__ */ React7.createElement("span", { className: "field-hint" }, profile.job_description.length.toLocaleString(), " / 8,000")), /* @__PURE__ */ React7.createElement("p", { className: "field-hint" }, "AI checks relevance and detail\u2014not job authenticity or your chances of selection. Checking sends this text to the configured AI provider."), jdReview && /* @__PURE__ */ React7.createElement("section", { className: `jd-review ${jdReview.assessment === "useful" ? "jd-useful" : "jd-advice"}`, "aria-label": "Job description review", "aria-live": "polite" }, /* @__PURE__ */ React7.createElement("strong", null, /* @__PURE__ */ React7.createElement(Icon, { name: jdReview.assessment === "useful" ? "circle-check" : "circle-alert", size: 18 }), { useful: "Useful for your interview", needs_detail: "A little more detail would help", role_mismatch: "This may be a different role", not_a_job_description: "This doesn't look like a job description" }[jdReview.assessment]), /* @__PURE__ */ React7.createElement("p", null, jdReview.summary), !!jdReview.relevant_skills.length && /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement("h3", null, "Skills mentioned"), /* @__PURE__ */ React7.createElement("div", { className: "skill-tags" }, jdReview.relevant_skills.map((skill) => /* @__PURE__ */ React7.createElement("span", { key: skill }, skill)))), !!jdReview.focus_areas.length && /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement("h3", null, "Suggested interview focus"), /* @__PURE__ */ React7.createElement("ul", null, jdReview.focus_areas.map((area) => /* @__PURE__ */ React7.createElement("li", { key: area }, area)))), !!jdReview.missing_details.length && /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement("h3", null, "Worth adding"), /* @__PURE__ */ React7.createElement("ul", null, jdReview.missing_details.map((detail) => /* @__PURE__ */ React7.createElement("li", { key: detail }, detail)))), !!jdReview.evidence.length && /* @__PURE__ */ React7.createElement("details", null, /* @__PURE__ */ React7.createElement("summary", null, "Why this feedback?"), jdReview.evidence.map((quote) => /* @__PURE__ */ React7.createElement("blockquote", { key: quote }, quote))), jdReview.assessment !== "useful" && /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn", onClick: () => update("job_description", "") }, "Continue without this description")))), step === 1 && /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("div", { className: "form-section-heading" }, /* @__PURE__ */ React7.createElement("span", { className: "section-icon" }, /* @__PURE__ */ React7.createElement(Icon, { name: "file-text" })), /* @__PURE__ */ React7.createElement("h2", null, "Your experience, in your words")), /* @__PURE__ */ React7.createElement("p", { className: "muted" }, "Upload a resume to fill the form, or enter everything below yourself."), /* @__PURE__ */ React7.createElement("div", { className: "setup-upload" }, /* @__PURE__ */ React7.createElement("label", null, "Resume PDF ", /* @__PURE__ */ React7.createElement("input", { type: "file", accept: ".pdf,application/pdf", onChange: (event) => {
      setFile(event.target.files[0] || null);
      setExtracted(null);
      setError("");
    } })), /* @__PURE__ */ React7.createElement("p", { className: "small muted" }, "Text PDFs only \xB7 up to 5 MB \xB7 up to 10 pages"), /* @__PURE__ */ React7.createElement("p", { className: "small muted" }, "Analyze sends extracted resume text to the configured AI provider. The app does not keep your original PDF or raw text. Only details you review and save are stored."), /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-secondary", disabled: !file || busy, onClick: analyzeResume }, busy ? "Analyzing resume\u2026" : "Analyze resume")), extracted && /* @__PURE__ */ React7.createElement("section", { className: "setup-extraction", "aria-label": "Extracted resume preview" }, /* @__PURE__ */ React7.createElement("h3", null, "Resume preview"), /* @__PURE__ */ React7.createElement("p", { className: "small muted" }, "AI can make mistakes. Using these details replaces the skills, projects, education and work fields below."), /* @__PURE__ */ React7.createElement(Details, { profile: extracted }), /* @__PURE__ */ React7.createElement("div", { className: "setup-actions" }, /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-secondary", onClick: applyExtracted }, "Use these details"), /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn", onClick: () => setExtracted(null) }, "Discard extraction"))), /* @__PURE__ */ React7.createElement("label", null, "Skills ", /* @__PURE__ */ React7.createElement("textarea", { className: "inp", required: true, rows: 3, value: skillsText, onChange: (event) => {
      setSkillsText(event.target.value);
      setSaved(false);
    }, placeholder: "Python, SQL, React" }), /* @__PURE__ */ React7.createElement("span", { className: "small muted" }, "Separate skills with commas. Listed skills are self-reported, not verified proficiency.")), /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement("h3", null, "Projects ", /* @__PURE__ */ React7.createElement("span", { className: "small muted" }, "(optional, up to 8)")), profile.projects.map((project, index) => /* @__PURE__ */ React7.createElement("div", { className: "setup-project", key: index }, /* @__PURE__ */ React7.createElement("label", null, "Project ", index + 1, " title", /* @__PURE__ */ React7.createElement("input", { className: "inp", required: true, maxLength: 120, value: project.title, onChange: (event) => update("projects", profile.projects.map((item, i) => i === index ? { ...item, title: event.target.value } : item)) })), /* @__PURE__ */ React7.createElement("label", null, "Your contribution & technologies", /* @__PURE__ */ React7.createElement("textarea", { className: "inp", rows: 3, maxLength: 2e3, value: project.description, onChange: (event) => update("projects", profile.projects.map((item, i) => i === index ? { ...item, description: event.target.value } : item)) })), /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn", onClick: () => update("projects", profile.projects.filter((_, i) => i !== index)) }, "Remove project ", index + 1))), /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-secondary", disabled: profile.projects.length >= 8, onClick: () => update("projects", [...profile.projects, { title: "", description: "" }]) }, "+ Add project")), /* @__PURE__ */ React7.createElement("label", null, "Education ", /* @__PURE__ */ React7.createElement("span", { className: "muted" }, "(optional)"), /* @__PURE__ */ React7.createElement("textarea", { className: "inp", rows: 2, maxLength: 2e3, value: profile.education, onChange: (event) => update("education", event.target.value) })), /* @__PURE__ */ React7.createElement("label", null, "Work / internship experience ", /* @__PURE__ */ React7.createElement("span", { className: "muted" }, "(optional)"), /* @__PURE__ */ React7.createElement("textarea", { className: "inp", rows: 3, maxLength: 3e3, value: profile.work_summary, onChange: (event) => update("work_summary", event.target.value) }))), step === 2 && /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("h2", null, saved ? "Your setup is saved" : "Ready to save your setup?"), /* @__PURE__ */ React7.createElement("p", { className: "muted" }, "Review your details. You can return here to update them."), /* @__PURE__ */ React7.createElement("dl", { className: "setup-summary" }, /* @__PURE__ */ React7.createElement("dt", null, "Target role"), /* @__PURE__ */ React7.createElement("dd", null, profile.target_role), /* @__PURE__ */ React7.createElement("dt", null, "Experience"), /* @__PURE__ */ React7.createElement("dd", null, profile.experience_level), profile.job_description && /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("dt", null, "Job description"), /* @__PURE__ */ React7.createElement("dd", null, profile.job_description))), /* @__PURE__ */ React7.createElement(Details, { profile }), /* @__PURE__ */ React7.createElement("p", { className: "setup-notice" }, "Save your profile, then meet the Technical Interviewer, Project Reviewer and Hiring Manager in the AI Panel. You choose when to start."), /* @__PURE__ */ React7.createElement("p", { className: "small muted" }, isGuest ? "Guest setup is linked to this browser session. Signing in uses a separate account profile." : "Your confirmed profile is saved with your account."), saved && /* @__PURE__ */ React7.createElement("p", { role: "status", className: "setup-success" }, "Saved successfully. Your profile is ready for the AI Panel.")), /* @__PURE__ */ React7.createElement("div", { className: "setup-actions" }, step > 0 && /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-secondary", onClick: () => {
      setStep(step - 1);
      setError("");
      setNotice("");
    } }, "Back"), step < 2 ? /* @__PURE__ */ React7.createElement("button", { className: "btn btn-primary", type: "submit" }, step === 0 ? "Continue to resume & skills" : "Review setup", " \u2192") : /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-primary", onClick: save, disabled: saved || busy }, busy ? "Saving\u2026" : saved ? "Setup saved" : "Confirm & save setup"), saved && /* @__PURE__ */ React7.createElement(React7.Fragment, null, /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn btn-secondary", onClick: onPanel }, "Meet the AI Panel \u2192"), /* @__PURE__ */ React7.createElement("button", { type: "button", className: "btn", onClick: onPractice }, "Practice core CS")))))), /* @__PURE__ */ React7.createElement("aside", { className: "profile-companion" }, /* @__PURE__ */ React7.createElement("div", { className: "companion-art" }, /* @__PURE__ */ React7.createElement("img", { src: "/Images/interview-desk.png", alt: "" })), /* @__PURE__ */ React7.createElement("span", { className: "eyebrow" }, "YOUR INTERVIEW BLUEPRINT"), /* @__PURE__ */ React7.createElement("h2", null, profile.target_role || "Made around you."), /* @__PURE__ */ React7.createElement("p", null, profile.target_role ? `${profile.experience_level} \xB7 Personalized practice` : "Your goals, skills and projects shape the conversation."), /* @__PURE__ */ React7.createElement("div", { className: "companion-lines" }, /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement(Icon, { name: "briefcase-business" }), /* @__PURE__ */ React7.createElement("span", null, /* @__PURE__ */ React7.createElement("strong", null, "A clear direction"), /* @__PURE__ */ React7.createElement("small", null, profile.target_role || "Start with your target role"))), /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement(Icon, { name: "file-text" }), /* @__PURE__ */ React7.createElement("span", null, /* @__PURE__ */ React7.createElement("strong", null, "Your own experience"), /* @__PURE__ */ React7.createElement("small", null, "Resume upload or manual entry"))), /* @__PURE__ */ React7.createElement("div", null, /* @__PURE__ */ React7.createElement(Icon, { name: "audio-lines" }), /* @__PURE__ */ React7.createElement("span", null, /* @__PURE__ */ React7.createElement("strong", null, "Three perspectives"), /* @__PURE__ */ React7.createElement("small", null, "Technical, project and hiring personas")))), /* @__PURE__ */ React7.createElement("p", { className: "companion-note" }, /* @__PURE__ */ React7.createElement(Icon, { name: "shield-check", size: 18 }), "You review every detail before saving."))));
  }
  function Details({ profile }) {
    return /* @__PURE__ */ React7.createElement("dl", { className: "setup-summary" }, /* @__PURE__ */ React7.createElement("dt", null, "Skills"), /* @__PURE__ */ React7.createElement("dd", null, profile.skills.length ? profile.skills.join(", ") : "None added"), /* @__PURE__ */ React7.createElement("dt", null, "Projects"), /* @__PURE__ */ React7.createElement("dd", null, profile.projects.length ? profile.projects.map((project, index) => /* @__PURE__ */ React7.createElement("div", { key: index }, /* @__PURE__ */ React7.createElement("strong", null, project.title), /* @__PURE__ */ React7.createElement("p", null, project.description))) : "None added"), /* @__PURE__ */ React7.createElement("dt", null, "Education"), /* @__PURE__ */ React7.createElement("dd", null, profile.education || "Not added"), /* @__PURE__ */ React7.createElement("dt", null, "Work experience"), /* @__PURE__ */ React7.createElement("dd", null, profile.work_summary || "Not added"));
  }

  // ui/src/hooks/usePanelVoice.js
  var { useState: useState5, useRef: useRef3, useEffect: useEffect3 } = window.React;
  function usePanelVoice(panelId, questionNumber, onTranscript, onError) {
    const [phase, setPhase] = useState5("idle");
    const [seconds, setSeconds] = useState5(0);
    const recorderRef = useRef3(null);
    const controllerRef = useRef3(null);
    const timerRef = useRef3(null);
    const versionRef = useRef3(0);
    const activeRef = useRef3(false);
    function cancel() {
      versionRef.current++;
      activeRef.current = false;
      clearInterval(timerRef.current);
      controllerRef.current?.abort();
      const recorder = recorderRef.current;
      if (recorder) {
        recorder.onstop = null;
        recorder.onerror = null;
        try {
          if (recorder.state !== "inactive") recorder.stop();
        } finally {
          recorder.stream.getTracks().forEach((track) => track.stop());
        }
      }
      recorderRef.current = null;
    }
    useEffect3(() => {
      setPhase("idle");
      setSeconds(0);
      return cancel;
    }, [panelId, questionNumber]);
    function stop() {
      clearInterval(timerRef.current);
      const recorder = recorderRef.current;
      if (recorder?.state === "recording") {
        setPhase("transcribing");
        recorder.stop();
      }
    }
    async function start() {
      if (activeRef.current) return;
      activeRef.current = true;
      const version = ++versionRef.current;
      setPhase("requesting");
      let stream;
      try {
        if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) throw new Error("Voice recording is unavailable in this browser. You can type your answer.");
        window.speechSynthesis?.cancel();
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        if (version !== versionRef.current) {
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
        const mime = ["audio/webm", "audio/mp4", "audio/ogg"].find((type) => MediaRecorder.isTypeSupported?.(type));
        const recorder = new MediaRecorder(stream, mime ? { mimeType: mime } : void 0);
        recorderRef.current = recorder;
        const chunks = [];
        recorder.ondataavailable = (event) => {
          if (event.data.size) chunks.push(event.data);
        };
        recorder.onerror = () => {
          cancel();
          setPhase("idle");
          onError("Recording failed. Retry or type your answer.");
        };
        recorder.onstop = async () => {
          clearInterval(timerRef.current);
          stream.getTracks().forEach((track) => track.stop());
          if (version !== versionRef.current) return;
          setPhase("transcribing");
          const actualMime = recorder.mimeType || mime || "audio/webm";
          const extension = actualMime.includes("mp4") ? "mp4" : actualMime.includes("ogg") ? "ogg" : "webm";
          const blob = new Blob(chunks, { type: actualMime });
          const controller = new AbortController();
          controllerRef.current = controller;
          const timeout = setTimeout(() => controller.abort(), 18e4);
          try {
            if (!blob.size) throw new Error("Recording was empty. Please try again.");
            const body = new FormData();
            body.append("audio", blob, `answer.${extension}`);
            body.append("question_number", questionNumber);
            const response = await fetch(`/api/panels/${panelId}/transcribe`, { method: "POST", body, signal: controller.signal });
            if (response.status === 413) throw new Error("Recording is too large. Please record a shorter answer.");
            const result = await response.json();
            if (!response.ok || !result.ok) throw new Error(result.message || "Transcription failed.");
            if (version === versionRef.current) onTranscript(result.transcript);
          } catch (error) {
            if (version === versionRef.current) onError(error.name === "AbortError" ? "Transcription timed out. Retry or type your answer." : error.message);
          } finally {
            clearTimeout(timeout);
            if (version === versionRef.current) {
              activeRef.current = false;
              setPhase("idle");
            }
          }
        };
        recorder.start(500);
        setSeconds(0);
        setPhase("recording");
        let elapsed = 0;
        timerRef.current = setInterval(() => {
          elapsed++;
          setSeconds(elapsed);
          if (elapsed >= 120) stop();
        }, 1e3);
      } catch (error) {
        stream?.getTracks().forEach((track) => track.stop());
        if (version === versionRef.current) {
          activeRef.current = false;
          setPhase("idle");
          onError(error.name === "NotAllowedError" ? "Microphone permission was denied. You can type your answer or enable the microphone and retry." : error.message);
        }
      }
    }
    return { phase, seconds, start, stop };
  }

  // ui/src/screens/interview/PanelScreen.jsx
  var React8 = window.React;
  var { useEffect: useEffect4, useRef: useRef4, useState: useState6 } = React8;
  function PanelScreen({ onSetup, isGuest }) {
    const [lobby, setLobby] = useState6(null);
    const [session, setSession] = useState6(null);
    const [busy, setBusy] = useState6(false);
    const [error, setError] = useState6("");
    const [draft, setDraft] = useState6("");
    const [heard, setHeard] = useState6("");
    const [unsent, setUnsent] = useState6("");
    const [speaking, setSpeaking] = useState6(false);
    const alive = useRef4(true);
    const busyRef = useRef4(false);
    const startToken = useRef4(null);
    const voice = usePanelVoice(session?.id, session?.current?.number, setHeard, setError);
    const voiceBusy = voice.phase !== "idle";
    const personas = lobby?.personas || [];
    const personaName = (id) => personas.find((persona) => persona.id === id)?.name || id;
    useEffect4(() => {
      alive.current = true;
      loadLobby();
      return () => {
        alive.current = false;
        window.speechSynthesis?.cancel();
      };
    }, []);
    useEffect4(() => {
      window.speechSynthesis?.cancel();
      setSpeaking(false);
      setHeard("");
    }, [session?.id, session?.current?.number]);
    async function loadLobby() {
      const result = await apiRequest("/api/panels");
      if (!alive.current) return;
      if (result.ok) setLobby(result);
      else setError(result.message);
    }
    async function advance(state) {
      if (state.status === "completed" || state.current) return;
      const result = await apiRequest(`/api/panels/${state.id}/advance`, {});
      if (!alive.current) return;
      if (result.session) setSession(result.session);
      if (!result.ok) setError(result.message);
    }
    async function perform(action) {
      if (busyRef.current || voiceBusy) return;
      busyRef.current = true;
      setBusy(true);
      setError("");
      window.speechSynthesis?.cancel();
      setSpeaking(false);
      try {
        await action();
      } catch {
        if (alive.current) setError("Something went wrong. Reopen your saved panel to continue.");
      } finally {
        busyRef.current = false;
        if (alive.current) setBusy(false);
      }
    }
    function start() {
      perform(async () => {
        startToken.current ||= crypto.randomUUID();
        const result = await apiRequest("/api/panels/start", { request_id: startToken.current });
        if (!alive.current) return;
        if (!result.ok) {
          setError(result.message);
          return;
        }
        startToken.current = null;
        setSession(result.session);
        setDraft("");
        setUnsent("");
        await advance(result.session);
      });
    }
    function open(id) {
      perform(async () => {
        const result = await apiRequest(`/api/panels/${id}`);
        if (!alive.current) return;
        if (!result.ok) {
          setError(result.message);
          return;
        }
        setSession(result.session);
        setDraft("");
        setUnsent("");
        await advance(result.session);
      });
    }
    function submit(event) {
      event.preventDefault();
      if (!draft.trim() || !session.current) return;
      perform(async () => {
        const result = await apiRequest(`/api/panels/${session.id}/answer`, { question_number: session.current.number, answer: draft });
        if (!alive.current) return;
        if (result.session) setSession(result.session);
        if (!result.ok) {
          if (result.session && result.session.current?.number !== session.current.number) {
            setUnsent(draft);
            setDraft("");
          }
          setError(result.message);
          return;
        }
        setDraft("");
        setHeard("");
        await advance(result.session);
      });
    }
    function finish() {
      perform(async () => {
        const result = await apiRequest(`/api/panels/${session.id}/finish`, {});
        if (!alive.current) return;
        if (result.session) setSession(result.session);
        if (!result.ok) {
          setError(result.message);
          return;
        }
        setDraft("");
        await advance(result.session);
      });
    }
    function speak() {
      if (!window.speechSynthesis || !window.SpeechSynthesisUtterance) {
        setError("Read-aloud is unavailable in this browser. The question is shown below.");
        return;
      }
      window.speechSynthesis.cancel();
      if (speaking) {
        setSpeaking(false);
        return;
      }
      const speech = new SpeechSynthesisUtterance(session.current.question);
      speech.lang = "en-US";
      speech.onend = () => {
        if (alive.current) setSpeaking(false);
      };
      speech.onerror = (event) => {
        if (!alive.current) return;
        setSpeaking(false);
        if (!["canceled", "interrupted"].includes(event.error)) setError("Question audio could not play. You can read the question and continue.");
      };
      setSpeaking(true);
      window.speechSynthesis.speak(speech);
    }
    const active = session?.current;
    return /* @__PURE__ */ React8.createElement("main", { className: "wrap panel-page" }, /* @__PURE__ */ React8.createElement("div", { className: "panel-heading" }, /* @__PURE__ */ React8.createElement("div", null, /* @__PURE__ */ React8.createElement("span", { className: "eyebrow" }, "THE INTERVIEW ROOM"), /* @__PURE__ */ React8.createElement("h1", null, session ? session.profile.target_role : "A real conversation. More perspectives."), /* @__PURE__ */ React8.createElement("p", { className: "muted" }, "Practice telling your story\u2014with questions built around you.")), session && /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy || voiceBusy, onClick: () => {
      window.speechSynthesis?.cancel();
      setSpeaking(false);
      setSession(null);
      setDraft("");
      setError("");
      loadLobby();
    } }, "Back to panel sessions")), error && /* @__PURE__ */ React8.createElement("p", { className: "formError", role: "alert" }, error), unsent && session && /* @__PURE__ */ React8.createElement("details", { className: "card panel-transcript" }, /* @__PURE__ */ React8.createElement("summary", null, "Previous draft was not submitted"), /* @__PURE__ */ React8.createElement("p", { className: "panel-answer" }, unsent), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "Another request had already changed that question. This draft was not added to the new question.")), !lobby && /* @__PURE__ */ React8.createElement("p", { role: "status" }, error ? /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", onClick: loadLobby }, "Retry loading panel") : "Loading panel\u2026"), lobby && /* @__PURE__ */ React8.createElement(React8.Fragment, null, !session && /* @__PURE__ */ React8.createElement("section", { className: "panel-welcome" }, /* @__PURE__ */ React8.createElement("div", null, /* @__PURE__ */ React8.createElement("span", { className: "pill pill-g" }, "PERSONALIZED AI PRACTICE"), /* @__PURE__ */ React8.createElement("h2", null, "Three interviewers.", /* @__PURE__ */ React8.createElement("br", null), "One stronger you."), /* @__PURE__ */ React8.createElement("p", null, "Your skills, projects and ambitions set the agenda. Get comfortable with the conversation before the real thing."), /* @__PURE__ */ React8.createElement("div", { className: "panel-format" }, /* @__PURE__ */ React8.createElement("span", null, /* @__PURE__ */ React8.createElement(Icon, { name: "users", size: 17 }), " 3 AI personas"), /* @__PURE__ */ React8.createElement("span", null, /* @__PURE__ */ React8.createElement(Icon, { name: "message-circle", size: 17 }), " 6 questions"), /* @__PURE__ */ React8.createElement("span", null, /* @__PURE__ */ React8.createElement(Icon, { name: "mic", size: 17 }), " Voice or text"))), /* @__PURE__ */ React8.createElement("img", { src: "/Images/interview-panel.png", alt: "Illustrated fictional AI interview panel" })), /* @__PURE__ */ React8.createElement("div", { className: "panel-personas" }, personas.map((persona, index) => /* @__PURE__ */ React8.createElement("section", { key: persona.id, className: `card panel-persona ${active?.persona === persona.id ? "panel-active" : ""}` }, /* @__PURE__ */ React8.createElement("span", { className: "panel-avatar", "aria-hidden": "true" }, /* @__PURE__ */ React8.createElement(Icon, { name: ["code-xml", "layers", "users"][index], size: 24 })), /* @__PURE__ */ React8.createElement("h2", null, persona.name), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, persona.focus), /* @__PURE__ */ React8.createElement("span", { className: "panel-role-status" }, active?.persona === persona.id ? "Current interviewer" : `Questions ${index * 2 + 1}\u2013${index * 2 + 2}`)))), !session ? /* @__PURE__ */ React8.createElement(React8.Fragment, null, /* @__PURE__ */ React8.createElement("section", { className: "card panel-card" }, /* @__PURE__ */ React8.createElement("h2", null, "Your panel briefing"), lobby.profile ? /* @__PURE__ */ React8.createElement(React8.Fragment, null, /* @__PURE__ */ React8.createElement("p", null, /* @__PURE__ */ React8.createElement("strong", null, lobby.profile.target_role), " \xB7 ", lobby.profile.experience_level), /* @__PURE__ */ React8.createElement("p", { className: "muted" }, "Focus skills: ", lobby.profile.skills.join(", "))) : /* @__PURE__ */ React8.createElement("p", null, "Save your target role and skills before starting. A resume is optional."), /* @__PURE__ */ React8.createElement("p", { className: "muted" }, "Six questions, one at a time. Type an answer or record in English, review the transcript, then submit. Read-aloud uses your browser voice. This version uses turn-by-turn audio."), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "Your profile and submitted answers are sent to the configured AI provider. Recordings are sent for transcription and removed from the app server afterward. Submitted answers and feedback are saved ", isGuest ? "for this guest browser session" : "with your account", ". Unsaved drafts are lost when you leave."), /* @__PURE__ */ React8.createElement("div", { className: "setup-actions" }, /* @__PURE__ */ React8.createElement("button", { className: "btn btn-primary", disabled: !lobby.profile || busy, onClick: start }, busy ? "Preparing your panel\u2026" : "Start panel interview"), /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy, onClick: onSetup }, lobby.profile ? "Edit my profile" : "Set up my profile"))), /* @__PURE__ */ React8.createElement("section", { className: "panel-history" }, /* @__PURE__ */ React8.createElement("h2", null, "Your panel sessions"), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "Your latest 20 sessions. Reopen to resume or read feedback."), !lobby.sessions.length ? /* @__PURE__ */ React8.createElement("p", { className: "muted" }, "Your first panel conversation starts here.") : lobby.sessions.map((item) => /* @__PURE__ */ React8.createElement("button", { disabled: busy, className: "card panel-history-row", key: item.id, onClick: () => open(item.id) }, /* @__PURE__ */ React8.createElement("span", null, /* @__PURE__ */ React8.createElement("strong", null, item.target_role), /* @__PURE__ */ React8.createElement("br", null), /* @__PURE__ */ React8.createElement("span", { className: "small muted" }, new Date(item.created_at).toLocaleDateString(), " \xB7 ", item.answered, " answers")), /* @__PURE__ */ React8.createElement("span", null, item.status === "completed" ? "View feedback" : "Resume", " \u2192"))))) : /* @__PURE__ */ React8.createElement(React8.Fragment, null, /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, session.turns.length, " of ", lobby.total_turns, " answers saved \xB7 This session uses the profile saved when it started."), session.turns.length > 0 && /* @__PURE__ */ React8.createElement("details", { className: "card panel-transcript" }, /* @__PURE__ */ React8.createElement("summary", null, "Conversation so far \xB7 ", session.turns.length, " answers"), session.turns.map((turn) => /* @__PURE__ */ React8.createElement("article", { key: turn.number }, /* @__PURE__ */ React8.createElement("h3", null, turn.number, ". ", personaName(turn.persona)), /* @__PURE__ */ React8.createElement("p", null, turn.question), /* @__PURE__ */ React8.createElement("p", { className: "panel-answer" }, /* @__PURE__ */ React8.createElement("strong", null, "You:"), " ", turn.answer)))), active && /* @__PURE__ */ React8.createElement("section", { className: "card panel-card" }, /* @__PURE__ */ React8.createElement("span", { className: "pill pill-g" }, personaName(active.persona), " \xB7 Question ", active.number, " / ", lobby.total_turns), /* @__PURE__ */ React8.createElement("h2", { className: "panel-question" }, active.question), /* @__PURE__ */ React8.createElement("div", { className: "setup-actions" }, /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy || voiceBusy, onClick: speak }, speaking ? "Stop reading" : "Read question aloud"), /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy || ["requesting", "transcribing"].includes(voice.phase), onClick: () => {
      setError("");
      setSpeaking(false);
      voice.phase === "recording" ? voice.stop() : voice.start();
    } }, voice.phase === "recording" ? `Stop recording \xB7 ${voice.seconds}s` : voice.phase === "requesting" ? "Waiting for microphone\u2026" : voice.phase === "transcribing" ? "Transcribing\u2026" : "Record answer")), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "Recording stops after 2 minutes. You can always type instead."), heard && /* @__PURE__ */ React8.createElement("div", { className: "panel-heard" }, /* @__PURE__ */ React8.createElement("h3", null, "Review your transcript"), /* @__PURE__ */ React8.createElement("p", null, heard), /* @__PURE__ */ React8.createElement("div", { className: "setup-actions" }, /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy || voiceBusy, onClick: () => {
      setDraft((previous) => previous ? previous + "\n" + heard : heard);
      setHeard("");
    } }, "Add to my answer"), /* @__PURE__ */ React8.createElement("button", { className: "btn", disabled: busy || voiceBusy, onClick: () => setHeard("") }, "Discard transcript"))), /* @__PURE__ */ React8.createElement("form", { onSubmit: submit }, /* @__PURE__ */ React8.createElement("label", { className: "panel-answer-label" }, "Your answer", /* @__PURE__ */ React8.createElement("textarea", { className: "inp", rows: 6, maxLength: 6e3, required: true, value: draft, disabled: busy || voiceBusy, onChange: (event) => setDraft(event.target.value), placeholder: "Explain your approach, reasoning and an example." })), /* @__PURE__ */ React8.createElement("div", { className: "setup-actions" }, /* @__PURE__ */ React8.createElement("button", { className: "btn btn-primary", disabled: busy || voiceBusy || !draft.trim() }, busy ? "Preparing next step\u2026" : "Submit answer \u2192")))), !active && session.status !== "completed" && /* @__PURE__ */ React8.createElement("section", { className: "card panel-card", "aria-live": "polite" }, /* @__PURE__ */ React8.createElement("h2", null, session.status === "report_pending" ? "Your feedback" : "Next panel question"), /* @__PURE__ */ React8.createElement("p", { className: "muted" }, busy ? "The AI panel is preparing your next step\u2026" : "Your submitted answers are saved. Continue when ready."), /* @__PURE__ */ React8.createElement("button", { className: "btn btn-primary", disabled: busy, onClick: () => perform(() => advance(session)) }, session.status === "report_pending" ? "Generate feedback" : "Prepare next question")), session.status === "active" && session.turns.length > 0 && /* @__PURE__ */ React8.createElement("div", { className: "panel-finish" }, /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "Finishing early uses submitted answers only. Submit or clear any draft first."), /* @__PURE__ */ React8.createElement("button", { className: "btn btn-secondary", disabled: busy || voiceBusy || !!draft.trim() || !!heard, onClick: finish }, "Finish now & get feedback")), session.report && /* @__PURE__ */ React8.createElement("section", { className: "card panel-card" }, /* @__PURE__ */ React8.createElement("span", { className: "pill pill-g" }, "PANEL FEEDBACK"), /* @__PURE__ */ React8.createElement("h2", null, "Your practice takeaways"), /* @__PURE__ */ React8.createElement("p", null, session.report.summary), /* @__PURE__ */ React8.createElement("p", { className: "small muted" }, "AI coaching based on ", session.turns.length, " submitted answers; this is not a hiring decision or a verified knowledge score.", session.turns.length < lobby.total_turns ? " This was a shortened session with limited evidence." : ""), session.report.feedback.map((item) => /* @__PURE__ */ React8.createElement("article", { className: "panel-feedback", key: item.question_number }, /* @__PURE__ */ React8.createElement("h3", null, "Question ", item.question_number, " \xB7 ", personaName(session.turns[item.question_number - 1]?.persona)), /* @__PURE__ */ React8.createElement("dl", { className: "setup-summary" }, /* @__PURE__ */ React8.createElement("dt", null, "What came through"), /* @__PURE__ */ React8.createElement("dd", null, item.strength), /* @__PURE__ */ React8.createElement("dt", null, "What to improve"), /* @__PURE__ */ React8.createElement("dd", null, item.improvement), /* @__PURE__ */ React8.createElement("dt", null, "Practice next"), /* @__PURE__ */ React8.createElement("dd", null, item.practice_task))))))));
  }

  // ui/src/screens/dashboard/TopicsScreen.jsx
  var React9 = window.React;
  var TOPIC_LIST = [
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
  function getTopicAnsweredCount(historyCounts = {}, topicName = "", displayName = "") {
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
  function TopicsScreen({ onSelectTopic, onBack, historyCounts = {} }) {
    return /* @__PURE__ */ React9.createElement("div", { className: "topic-page-frame" }, /* @__PURE__ */ React9.createElement("div", { className: "topic-header-row" }, /* @__PURE__ */ React9.createElement(
      "button",
      {
        className: "btn-back-arrow",
        onClick: onBack,
        title: "Back to Dashboard",
        "aria-label": "Back"
      },
      /* @__PURE__ */ React9.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React9.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React9.createElement("polyline", { points: "12 19 5 12 12 5" }))
    ), /* @__PURE__ */ React9.createElement("div", { className: "topic-header-center" }, /* @__PURE__ */ React9.createElement("span", { className: "eyebrow" }, "KNOWLEDGE PRACTICE"), /* @__PURE__ */ React9.createElement("h1", { className: "topic-header-title" }, "Make your fundamentals stronger."), /* @__PURE__ */ React9.createElement("p", { className: "topic-header-subtitle" }, "Choose a subject. Explain your thinking. Get feedback with sources.")), /* @__PURE__ */ React9.createElement("div", { className: "topic-header-script" }, "6 subjects.", /* @__PURE__ */ React9.createElement("br", null), "Your next breakthrough.")), /* @__PURE__ */ React9.createElement("div", { className: "topic-grid" }, TOPIC_LIST.map((t) => {
      const answered = getTopicAnsweredCount(historyCounts, t.name, t.displayName);
      const countText = answered > 0 ? `${answered} question${answered === 1 ? "" : "s"} answered` : "0 questions answered";
      return /* @__PURE__ */ React9.createElement(
        "button",
        {
          key: t.name,
          type: "button",
          className: "topic-card",
          onClick: () => onSelectTopic(t.name)
        },
        /* @__PURE__ */ React9.createElement("span", { className: "topic-symbol" }, /* @__PURE__ */ React9.createElement(Icon, { name: { OOP: "layers", Java: "braces", DBMS: "database", OS: "cpu", "Computer Networks": "network", DSA: "route" }[t.name], size: 30 })),
        /* @__PURE__ */ React9.createElement("div", { className: "topic-card-title-row" }, /* @__PURE__ */ React9.createElement("span", { className: "topic-card-title" }, t.displayName), /* @__PURE__ */ React9.createElement("span", { className: "topic-card-chev" }, ">")),
        /* @__PURE__ */ React9.createElement("div", { className: "topic-card-count" }, /* @__PURE__ */ React9.createElement("p", { className: "topic-detail" }, { OOP: "Objects, design principles and clean abstractions.", Java: "Language fundamentals and practical reasoning.", DBMS: "Queries, data models and reliable transactions.", OS: "Processes, memory and what happens underneath.", "Computer Networks": "Protocols, connections and the web in motion.", DSA: "Problem solving, complexity and trade-offs." }[t.name]), countText)
      );
    })));
  }

  // ui/src/screens/dashboard/ProgressScreen.jsx
  var React10 = window.React;
  function ProgressScreen({ user, isGuest, history = [], historyCounts = {}, onStartInterview, onSelectTopic, onOpenPastReport, onBack }) {
    const totalQuestions = history.reduce((acc, r) => acc + (r.questions_answered || 0), 0);
    const totalInterviews = history.length;
    const activeTopicsCount = TOPIC_LIST.filter((t) => getTopicAnsweredCount(historyCounts, t.name, t.displayName) > 0).length;
    const latestReadiness = history.length > 0 ? formatReadiness(history[0].readiness) : null;
    return /* @__PURE__ */ React10.createElement("div", { className: "wrap", style: { paddingTop: "24px", paddingBottom: "50px" } }, /* @__PURE__ */ React10.createElement("div", { style: { display: "flex", alignItems: "center", gap: "14px", marginBottom: "22px" } }, /* @__PURE__ */ React10.createElement(
      "button",
      {
        type: "button",
        className: "btn-back-arrow",
        onClick: onBack,
        title: "Back to Dashboard",
        "aria-label": "Back to Dashboard"
      },
      /* @__PURE__ */ React10.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React10.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React10.createElement("polyline", { points: "12 19 5 12 12 5" }))
    ), /* @__PURE__ */ React10.createElement("div", null, /* @__PURE__ */ React10.createElement("span", { className: "eyebrow" }, "YOUR PRACTICE, IN PERSPECTIVE"), /* @__PURE__ */ React10.createElement("h1", { style: { fontSize: "1.75rem", margin: "2px 0 0" } }, "Interview Progress & Analytics"))), /* @__PURE__ */ React10.createElement("div", { className: "hero-row", style: { marginBottom: "28px" } }, /* @__PURE__ */ React10.createElement("div", null, /* @__PURE__ */ React10.createElement("span", { className: "eyebrow", style: { color: "var(--green)" } }, "Progress Over Perfection"), /* @__PURE__ */ React10.createElement("h2", { style: { fontSize: "1.6rem", marginTop: "6px" } }, "See how far your practice has taken you."), /* @__PURE__ */ React10.createElement("p", { className: "muted", style: { marginTop: "8px", lineHeight: "1.5" } }, "Review your real-time grounded evaluations across all 6 computer science core subjects."), /* @__PURE__ */ React10.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-primary",
        style: { marginTop: "18px", padding: "12px 24px" },
        onClick: onStartInterview
      },
      "Practice Next Interview \u2192"
    )), /* @__PURE__ */ React10.createElement("div", { className: "hero-card-right" }, /* @__PURE__ */ React10.createElement(
      "img",
      {
        src: "/Images/interview-desk.png",
        alt: "Your interview preparation workspace",
        className: "progress-hero-img"
      }
    ))), /* @__PURE__ */ React10.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "16px", marginBottom: "32px" } }, /* @__PURE__ */ React10.createElement("div", { className: "card", style: { padding: "20px" } }, /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, "Total Questions Practiced"), /* @__PURE__ */ React10.createElement("div", { style: { fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" } }, totalQuestions), /* @__PURE__ */ React10.createElement("span", { className: "small muted", style: { color: "var(--green)", fontWeight: 600 } }, totalQuestions > 0 ? "Real evaluation evidence" : "Ready for question 1")), /* @__PURE__ */ React10.createElement("div", { className: "card", style: { padding: "20px" } }, /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, "Interviews Practiced"), /* @__PURE__ */ React10.createElement("div", { style: { fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" } }, totalInterviews), /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, totalInterviews > 0 ? `${totalInterviews} session${totalInterviews === 1 ? "" : "s"} with evaluated answers` : "No evaluated sessions yet")), /* @__PURE__ */ React10.createElement("div", { className: "card", style: { padding: "20px" } }, /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, "Subjects Practiced"), /* @__PURE__ */ React10.createElement("div", { style: { fontSize: "2rem", fontWeight: "700", color: "var(--ink)", marginTop: "6px" } }, activeTopicsCount, " / 6"), /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, 6 - activeTopicsCount > 0 ? `${6 - activeTopicsCount} subjects remaining` : "All subjects covered!")), /* @__PURE__ */ React10.createElement("div", { className: "card", style: { padding: "20px" } }, /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, "Latest Readiness Verdict"), /* @__PURE__ */ React10.createElement("div", { style: { marginTop: "10px" } }, latestReadiness ? /* @__PURE__ */ React10.createElement("span", { className: `pill ${latestReadiness.pill}`, style: { fontSize: "0.92rem", padding: "6px 14px" } }, latestReadiness.text) : /* @__PURE__ */ React10.createElement("span", { className: "pill pill-muted", style: { fontSize: "0.92rem", padding: "6px 14px" } }, "Not Evaluated Yet")), /* @__PURE__ */ React10.createElement("span", { className: "small muted", style: { display: "block", marginTop: "8px" } }, "Textbook grounded benchmark"))), /* @__PURE__ */ React10.createElement("div", { style: { marginBottom: "34px" } }, /* @__PURE__ */ React10.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "14px" } }, /* @__PURE__ */ React10.createElement("h2", { style: { fontSize: "1.25rem" } }, "Subject Practice Progress"), /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, "6 Core Technical Domains")), /* @__PURE__ */ React10.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 310px), 1fr))", gap: "16px" } }, TOPIC_LIST.map((t) => {
      const answered = getTopicAnsweredCount(historyCounts, t.name, t.displayName);
      const pool = t.totalPool || 8;
      const pct = Math.min(100, Math.round(answered / pool * 100));
      return /* @__PURE__ */ React10.createElement("div", { key: t.name, className: "card", style: { padding: "18px 20px" } }, /* @__PURE__ */ React10.createElement("div", { style: { display: "flex", alignItems: "center", gap: "14px", marginBottom: "12px" } }, /* @__PURE__ */ React10.createElement("img", { src: t.icon, alt: t.displayName, style: { width: "42px", height: "42px", objectFit: "contain" } }), /* @__PURE__ */ React10.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React10.createElement("div", { style: { fontWeight: 600, fontSize: "1rem", color: "var(--ink)" } }, t.displayName), /* @__PURE__ */ React10.createElement("span", { className: "small muted" }, answered, " questions answered")), /* @__PURE__ */ React10.createElement(
        "button",
        {
          type: "button",
          className: "btn btn-secondary small",
          onClick: () => onSelectTopic(t.name),
          style: { padding: "6px 12px", fontSize: "0.82rem" }
        },
        "Practice \u2192"
      )), /* @__PURE__ */ React10.createElement("div", { style: { height: "6px", width: "100%", background: "#EAECF0", borderRadius: "999px", overflow: "hidden" } }, /* @__PURE__ */ React10.createElement(
        "div",
        {
          style: {
            height: "100%",
            width: `${pct}%`,
            background: pct > 0 ? "var(--green)" : "transparent",
            borderRadius: "999px",
            transition: "width 0.4s ease"
          }
        }
      )), /* @__PURE__ */ React10.createElement("div", { style: { display: "flex", justifyContent: "space-between", marginTop: "6px" } }, /* @__PURE__ */ React10.createElement("span", { className: "small muted", style: { fontSize: "0.78rem" } }, pct, "% of practice goal"), /* @__PURE__ */ React10.createElement("span", { className: "small muted", style: { fontSize: "0.78rem" } }, answered, " / ", pool, " answers")));
    }))));
  }

  // ui/src/screens/history/HistoryScreen.jsx
  var React11 = window.React;
  var { useState: useState7, useEffect: useEffect5 } = React11;
  function HistoryScreen({ user, isGuest, historyCounts = {}, onSelectSubject, onBack }) {
    const [topics, setTopics] = useState7(
      () => TOPIC_LIST.map((t) => ({
        name: t.name,
        display_name: t.displayName,
        icon: t.icon,
        subtitle: "View your past questions and answers",
        attempts: getTopicAnsweredCount(historyCounts, t.name, t.displayName) || 0
      }))
    );
    const displayName = isGuest ? "Guest" : user?.name || (user?.email ? user.email.split("@")[0] : "Candidate");
    const avatarInitial = (displayName[0] || "A").toUpperCase();
    useEffect5(() => {
      let active = true;
      async function load() {
        const res = await apiRequest("/api/history/topics");
        if (active && res && res.ok && res.topics) {
          setTopics(res.topics);
        }
      }
      load();
      return () => {
        active = false;
      };
    }, [isGuest]);
    return /* @__PURE__ */ React11.createElement("div", { className: "history-overview-wrap" }, /* @__PURE__ */ React11.createElement("div", { className: "history-top-header" }, /* @__PURE__ */ React11.createElement("div", { className: "history-brand-col" }, /* @__PURE__ */ React11.createElement("img", { src: "/Images/logo.png", alt: "CrackProof", className: "history-header-logo" }), /* @__PURE__ */ React11.createElement("div", null, /* @__PURE__ */ React11.createElement("h1", { className: "history-header-title" }, "History"), /* @__PURE__ */ React11.createElement("p", { className: "history-header-subtitle" }, "Choose a subject to view your interview history."))), /* @__PURE__ */ React11.createElement("div", { className: "history-header-right" }, /* @__PURE__ */ React11.createElement("div", { className: "history-quote-box" }, /* @__PURE__ */ React11.createElement("span", { className: "history-quote-text" }, '"Review. Reflect. Improve.', /* @__PURE__ */ React11.createElement("br", null), `That's how you go further."`), /* @__PURE__ */ React11.createElement("svg", { className: "history-quote-plant", viewBox: "0 0 24 24", fill: "none", stroke: "#166534", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React11.createElement("path", { d: "M12 22v-9" }), /* @__PURE__ */ React11.createElement("path", { d: "M12 13c-3-3-6-2-8 1 0-4 4-7 8-7 4 0 8 3 8 7-2-3-5-4-8-1z" }))), /* @__PURE__ */ React11.createElement("div", { className: "history-avatar-badge", title: displayName }, avatarInitial))), /* @__PURE__ */ React11.createElement("div", { className: "history-grid-6" }, topics.map((t) => /* @__PURE__ */ React11.createElement(
      "button",
      {
        key: t.name,
        type: "button",
        className: "history-subject-card",
        onClick: () => onSelectSubject(t.name)
      },
      /* @__PURE__ */ React11.createElement("div", { className: "history-card-left" }, /* @__PURE__ */ React11.createElement("img", { src: t.icon, alt: t.display_name, className: "history-card-icon" }), /* @__PURE__ */ React11.createElement("div", { className: "history-card-details" }, /* @__PURE__ */ React11.createElement("h3", { className: "history-card-name" }, t.display_name), /* @__PURE__ */ React11.createElement("p", { className: "history-card-desc" }, "View your past questions and answers"), /* @__PURE__ */ React11.createElement("span", { className: "history-badge-attempts" }, t.attempts || 0, " attempt", (t.attempts || 0) === 1 ? "" : "s"))),
      /* @__PURE__ */ React11.createElement("span", { className: "history-card-chevron" }, /* @__PURE__ */ React11.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.4", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React11.createElement("polyline", { points: "9 18 15 12 9 6" })))
    ))));
  }

  // ui/src/screens/history/SubjectHistoryScreen.jsx
  var React12 = window.React;
  var { useState: useState8, useMemo } = React12;
  function SubjectHistoryScreen({ subject, questions = [], loading, onSelectQuestion, onBack, onNavigate, onStartInterview }) {
    const [filter, setFilter] = useState8("ALL");
    const topicObj = TOPIC_LIST.find((t) => t.name.toLowerCase() === subject.toLowerCase() || t.displayName.toLowerCase() === subject.toLowerCase()) || {
      name: subject,
      displayName: subject,
      icon: "/Images/java.png"
    };
    const filteredQuestions = useMemo(() => {
      if (filter === "CORRECT") return questions.filter((q) => q.verdict === "CORRECT");
      if (filter === "PARTIAL") return questions.filter((q) => q.verdict === "PARTIAL");
      if (filter === "NEEDS_WORK") return questions.filter((q) => q.verdict === "NEEDS_WORK");
      return questions;
    }, [questions, filter]);
    return /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-container" }, /* @__PURE__ */ React12.createElement("aside", { className: "sub-hist-sidebar" }, /* @__PURE__ */ React12.createElement("div", null, /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-brand", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React12.createElement("img", { src: "/Images/logo.png", alt: "CrackProof", className: "sub-hist-brand-img" }), /* @__PURE__ */ React12.createElement("span", { className: "sub-hist-brand-name" }, "CrackProof")), /* @__PURE__ */ React12.createElement("nav", { className: "sub-hist-nav-menu" }, /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("path", { d: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" }), /* @__PURE__ */ React12.createElement("polyline", { points: "9 22 9 12 15 12 15 22" })), "Home"), /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("topics") }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("rect", { x: "2", y: "3", width: "20", height: "14", rx: "2", ry: "2" }), /* @__PURE__ */ React12.createElement("line", { x1: "8", y1: "21", x2: "16", y2: "21" }), /* @__PURE__ */ React12.createElement("line", { x1: "12", y1: "17", x2: "12", y2: "21" })), "Interviews"), /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("progress") }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("line", { x1: "18", y1: "20", x2: "18", y2: "10" }), /* @__PURE__ */ React12.createElement("line", { x1: "12", y1: "20", x2: "12", y2: "4" }), /* @__PURE__ */ React12.createElement("line", { x1: "6", y1: "20", x2: "6", y2: "14" })), "Progress"), /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-nav-item active", onClick: () => onNavigate("history") }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React12.createElement("polyline", { points: "12 6 12 12 16 14" })), "History"), /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("circle", { cx: "12", cy: "12", r: "3" }), /* @__PURE__ */ React12.createElement("path", { d: "M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" })), "Settings"))), /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-sidebar-footer" }, /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-footer-quote" }, "Consistent", /* @__PURE__ */ React12.createElement("br", null), "Practice", /* @__PURE__ */ React12.createElement("br", null), "Creates", /* @__PURE__ */ React12.createElement("br", null), "Confident You."), /* @__PURE__ */ React12.createElement("img", { src: "/Images/mountain.png", alt: "Mountain summit flag", className: "sub-hist-footer-img" }))), /* @__PURE__ */ React12.createElement("main", { className: "sub-hist-main" }, /* @__PURE__ */ React12.createElement("button", { type: "button", className: "sub-hist-back-btn", onClick: onBack }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React12.createElement("polyline", { points: "12 19 5 12 12 5" })), "Back to All Subjects"), /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-title-row" }, /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-heading-group" }, /* @__PURE__ */ React12.createElement("img", { src: topicObj.icon, alt: topicObj.displayName, className: "sub-hist-subject-icon" }), /* @__PURE__ */ React12.createElement("div", null, /* @__PURE__ */ React12.createElement("h1", { className: "sub-hist-subject-title" }, topicObj.displayName, " \u2013 History"), /* @__PURE__ */ React12.createElement("p", { className: "sub-hist-subject-sub" }, "Your past ", topicObj.displayName, " interview questions and answers."))), /* @__PURE__ */ React12.createElement(
      "select",
      {
        className: "sub-hist-filter-select",
        value: filter,
        onChange: (e) => setFilter(e.target.value)
      },
      /* @__PURE__ */ React12.createElement("option", { value: "ALL" }, "All Results (", questions.length, ")"),
      /* @__PURE__ */ React12.createElement("option", { value: "CORRECT" }, "Correct (", questions.filter((q) => q.verdict === "CORRECT").length, ")"),
      /* @__PURE__ */ React12.createElement("option", { value: "PARTIAL" }, "Partial (", questions.filter((q) => q.verdict === "PARTIAL").length, ")"),
      /* @__PURE__ */ React12.createElement("option", { value: "NEEDS_WORK" }, "Needs Work (", questions.filter((q) => q.verdict === "NEEDS_WORK").length, ")")
    )), loading ? /* @__PURE__ */ React12.createElement("div", { style: { textAlign: "center", padding: "60px 20px", color: "#667085" } }, /* @__PURE__ */ React12.createElement("p", null, "Loading questions history...")) : filteredQuestions.length === 0 ? /* @__PURE__ */ React12.createElement("div", { className: "preview-card", style: { textAlign: "center", padding: "48px 24px" } }, /* @__PURE__ */ React12.createElement("h3", { style: { fontSize: "1.2rem", fontWeight: 700, color: "#101828", marginBottom: "8px" } }, "No ", filter !== "ALL" ? filter.toLowerCase().replace("_", " ") : "", " questions recorded yet"), /* @__PURE__ */ React12.createElement("p", { style: { color: "#667085", maxWidth: "460px", margin: "0 auto 20px" } }, "Practice technical interview questions in ", topicObj.displayName, " to generate real-time AI evaluations and grounded evidence."), /* @__PURE__ */ React12.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-primary",
        style: { padding: "10px 22px" },
        onClick: () => onStartInterview(topicObj.name)
      },
      "Start ",
      topicObj.displayName,
      " Interview \u2192"
    )) : /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-list" }, filteredQuestions.map((q, idx) => {
      const verdictClass = q.verdict === "CORRECT" ? "correct" : q.verdict === "PARTIAL" ? "partial" : "needswork";
      const verdictLabel = q.verdict === "CORRECT" ? "CORRECT" : q.verdict === "PARTIAL" ? "PARTIAL" : "NEEDS WORK";
      return /* @__PURE__ */ React12.createElement(
        "div",
        {
          key: q.id || idx,
          className: "sub-hist-q-card",
          onClick: () => onSelectQuestion(questions.findIndex((item) => item.id === q.id))
        },
        /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-q-left" }, /* @__PURE__ */ React12.createElement("h3", { className: "sub-hist-q-text" }, q.question), /* @__PURE__ */ React12.createElement("p", { className: "sub-hist-q-time" }, q.timestamp)),
        /* @__PURE__ */ React12.createElement("div", { className: "sub-hist-q-right" }, /* @__PURE__ */ React12.createElement("span", { className: `badge-status ${verdictClass}` }, q.verdict === "CORRECT" && /* @__PURE__ */ React12.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("polyline", { points: "20 6 9 17 4 12" })), q.verdict === "PARTIAL" && /* @__PURE__ */ React12.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React12.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "12" }), /* @__PURE__ */ React12.createElement("line", { x1: "12", y1: "16", x2: "12.01", y2: "16" })), q.verdict === "NEEDS_WORK" && /* @__PURE__ */ React12.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("line", { x1: "12", y1: "19", x2: "12", y2: "5" }), /* @__PURE__ */ React12.createElement("polyline", { points: "5 12 12 5 19 12" })), verdictLabel), /* @__PURE__ */ React12.createElement("span", { className: "sub-hist-score" }, "Score: ", q.score_display || `${q.score}/10`), /* @__PURE__ */ React12.createElement("span", { className: "sub-hist-chev" }, /* @__PURE__ */ React12.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.4", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React12.createElement("polyline", { points: "9 18 15 12 9 6" }))))
      );
    }))));
  }

  // ui/src/screens/history/QuestionPreviewScreen.jsx
  var React13 = window.React;
  var { useState: useState9 } = React13;
  function QuestionPreviewScreen({ subject, questions = [], currentIndex = 0, onBack, onNavigateIndex, onNavigate }) {
    const [activeTab, setActiveTab] = useState9("right");
    const q = questions[currentIndex] || {};
    const ev = q.evaluation || {};
    const topicObj = TOPIC_LIST.find((t) => t.name.toLowerCase() === subject.toLowerCase() || t.displayName.toLowerCase() === subject.toLowerCase()) || {
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
    return /* @__PURE__ */ React13.createElement("div", { className: "sub-hist-container" }, /* @__PURE__ */ React13.createElement("aside", { className: "sub-hist-sidebar" }, /* @__PURE__ */ React13.createElement("div", null, /* @__PURE__ */ React13.createElement("div", { className: "sub-hist-brand", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React13.createElement("img", { src: "/Images/logo.png", alt: "CrackProof", className: "sub-hist-brand-img" }), /* @__PURE__ */ React13.createElement("span", { className: "sub-hist-brand-name" }, "CrackProof")), /* @__PURE__ */ React13.createElement("nav", { className: "sub-hist-nav-menu" }, /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("path", { d: "M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" }), /* @__PURE__ */ React13.createElement("polyline", { points: "9 22 9 12 15 12 15 22" })), "Home"), /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("topics") }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("rect", { x: "2", y: "3", width: "20", height: "14", rx: "2", ry: "2" }), /* @__PURE__ */ React13.createElement("line", { x1: "8", y1: "21", x2: "16", y2: "21" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "17", x2: "12", y2: "21" })), "Interviews"), /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("progress") }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("line", { x1: "18", y1: "20", x2: "18", y2: "10" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "20", x2: "12", y2: "4" }), /* @__PURE__ */ React13.createElement("line", { x1: "6", y1: "20", x2: "6", y2: "14" })), "Progress"), /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-nav-item active", onClick: () => onNavigate("history") }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React13.createElement("polyline", { points: "12 6 12 12 16 14" })), "History"), /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-nav-item", onClick: () => onNavigate("dash") }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "3" }), /* @__PURE__ */ React13.createElement("path", { d: "M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" })), "Settings"))), /* @__PURE__ */ React13.createElement("div", { className: "sub-hist-sidebar-footer" }, /* @__PURE__ */ React13.createElement("div", { className: "sub-hist-footer-quote" }, "Consistent", /* @__PURE__ */ React13.createElement("br", null), "Practice", /* @__PURE__ */ React13.createElement("br", null), "Creates", /* @__PURE__ */ React13.createElement("br", null), "Confident You."), /* @__PURE__ */ React13.createElement("img", { src: "/Images/mountain.png", alt: "Mountain summit flag", className: "sub-hist-footer-img" }))), /* @__PURE__ */ React13.createElement("main", { className: "sub-hist-main" }, /* @__PURE__ */ React13.createElement("div", { className: "preview-actions-bar" }, /* @__PURE__ */ React13.createElement("button", { type: "button", className: "sub-hist-back-btn", onClick: onBack, style: { margin: 0 } }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React13.createElement("polyline", { points: "12 19 5 12 12 5" })), "Back to ", topicObj.displayName, " History"), /* @__PURE__ */ React13.createElement("div", { className: "preview-prev-next" }, /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: "preview-pn-btn",
        disabled: !hasPrev,
        onClick: () => onNavigateIndex(currentIndex - 1)
      },
      "< Previous"
    ), /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: "preview-pn-btn",
        disabled: !hasNext,
        onClick: () => onNavigateIndex(currentIndex + 1)
      },
      "Next >"
    ))), /* @__PURE__ */ React13.createElement("div", { className: "preview-main-q-header" }, /* @__PURE__ */ React13.createElement("div", null, /* @__PURE__ */ React13.createElement("h1", { className: "preview-main-q-title" }, q.question || "Interview Question"), /* @__PURE__ */ React13.createElement("p", { className: "preview-main-q-time" }, q.timestamp)), /* @__PURE__ */ React13.createElement("div", { className: "preview-main-q-meta" }, /* @__PURE__ */ React13.createElement("span", { className: `badge-status ${verdictClass}` }, q.verdict === "CORRECT" && /* @__PURE__ */ React13.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("polyline", { points: "20 6 9 17 4 12" })), q.verdict === "PARTIAL" && /* @__PURE__ */ React13.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "12" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "16", x2: "12.01", y2: "16" })), q.verdict === "NEEDS_WORK" && /* @__PURE__ */ React13.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "19", x2: "12", y2: "5" }), /* @__PURE__ */ React13.createElement("polyline", { points: "5 12 12 5 19 12" })), verdictLabel), /* @__PURE__ */ React13.createElement("span", { className: "preview-main-score" }, "Score: ", q.score_display || `${q.score}/10`))), /* @__PURE__ */ React13.createElement("div", { className: "preview-card" }, /* @__PURE__ */ React13.createElement("h2", { className: "preview-card-title" }, "Your Answer"), /* @__PURE__ */ React13.createElement("div", { className: "preview-answer-body" }, q.transcript ? q.transcript : /* @__PURE__ */ React13.createElement("span", { className: "muted", style: { fontStyle: "italic" } }, "No spoken or written transcript recorded for this question."))), /* @__PURE__ */ React13.createElement("div", { className: "preview-card" }, /* @__PURE__ */ React13.createElement("h2", { className: "preview-card-title" }, "Evaluation Summary"), /* @__PURE__ */ React13.createElement("div", { className: "preview-tabs-row" }, /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: `preview-tab-btn ${activeTab === "right" ? "active" : ""}`,
        onClick: () => setActiveTab("right")
      },
      "What You Got Right (",
      correctPoints.length,
      ")"
    ), /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: `preview-tab-btn ${activeTab === "missing" ? "active" : ""}`,
        onClick: () => setActiveTab("missing")
      },
      "What's Missing (",
      missingPoints.length,
      ")"
    ), /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: `preview-tab-btn ${activeTab === "misconceptions" ? "active" : ""}`,
        onClick: () => setActiveTab("misconceptions")
      },
      "Misconceptions (",
      misconceptions.length,
      ")"
    ), /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: `preview-tab-btn ${activeTab === "evidence" ? "active" : ""}`,
        onClick: () => setActiveTab("evidence")
      },
      "Depth Evidence (",
      evidenceList.length,
      ")"
    ), /* @__PURE__ */ React13.createElement(
      "button",
      {
        type: "button",
        className: `preview-tab-btn ${activeTab === "reasoning" ? "active" : ""}`,
        onClick: () => setActiveTab("reasoning")
      },
      "Reasoning"
    )), /* @__PURE__ */ React13.createElement("div", null, activeTab === "right" && (correctPoints.length === 0 ? /* @__PURE__ */ React13.createElement("p", { className: "muted", style: { fontStyle: "italic", margin: 0 } }, "No correct technical points demonstrated in this attempt.") : /* @__PURE__ */ React13.createElement("ul", { className: "preview-bullet-list" }, correctPoints.map((pt, i) => /* @__PURE__ */ React13.createElement("li", { key: i, className: "preview-bullet-item" }, /* @__PURE__ */ React13.createElement("span", { className: "preview-bullet-icon", style: { color: "#12B76A" } }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.5", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React13.createElement("polyline", { points: "16 9 10 15 7 12" }))), /* @__PURE__ */ React13.createElement("span", null, pt))))), activeTab === "missing" && (missingPoints.length === 0 ? /* @__PURE__ */ React13.createElement("p", { className: "muted", style: { fontStyle: "italic", margin: 0 } }, "None! All foundational core concepts were satisfactorily covered.") : /* @__PURE__ */ React13.createElement("ul", { className: "preview-bullet-list" }, missingPoints.map((pt, i) => /* @__PURE__ */ React13.createElement("li", { key: i, className: "preview-bullet-item" }, /* @__PURE__ */ React13.createElement("span", { className: "preview-bullet-icon", style: { color: "#F79009" } }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "12" }), /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "16", x2: "12.01", y2: "16" }))), /* @__PURE__ */ React13.createElement("span", null, pt))))), activeTab === "misconceptions" && (misconceptions.length === 0 ? /* @__PURE__ */ React13.createElement("p", { className: "muted", style: { fontStyle: "italic", margin: 0 } }, "No conceptual misconceptions or fallacies were detected in your response.") : /* @__PURE__ */ React13.createElement("ul", { className: "preview-bullet-list" }, misconceptions.map((pt, i) => /* @__PURE__ */ React13.createElement("li", { key: i, className: "preview-bullet-item" }, /* @__PURE__ */ React13.createElement("span", { className: "preview-bullet-icon", style: { color: "#D92D20" } }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), /* @__PURE__ */ React13.createElement("line", { x1: "15", y1: "9", x2: "9", y2: "15" }), /* @__PURE__ */ React13.createElement("line", { x1: "9", y1: "9", x2: "15", y2: "15" }))), /* @__PURE__ */ React13.createElement("span", null, typeof pt === "string" ? pt : pt.misconception || JSON.stringify(pt)))))), activeTab === "evidence" && (evidenceList.length === 0 ? /* @__PURE__ */ React13.createElement("p", { className: "muted", style: { fontStyle: "italic", margin: 0 } }, "No structured depth dimension evidence recorded.") : /* @__PURE__ */ React13.createElement("ul", { className: "preview-bullet-list" }, evidenceList.map((evItem, i) => {
      const isDem = evItem.status === "DEMONSTRATED";
      const isPart = evItem.status === "PARTIALLY_DEMONSTRATED";
      const iconColor = isDem ? "#12B76A" : isPart ? "#F79009" : "#98A2B3";
      return /* @__PURE__ */ React13.createElement("li", { key: i, className: "preview-bullet-item" }, /* @__PURE__ */ React13.createElement("span", { className: "preview-bullet-icon", style: { color: iconColor } }, /* @__PURE__ */ React13.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React13.createElement("circle", { cx: "12", cy: "12", r: "10" }), isDem ? /* @__PURE__ */ React13.createElement("polyline", { points: "16 9 10 15 7 12" }) : /* @__PURE__ */ React13.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "12" }))), /* @__PURE__ */ React13.createElement("div", null, /* @__PURE__ */ React13.createElement("strong", { style: { color: "#101828" } }, evItem.evidence_type, ": "), /* @__PURE__ */ React13.createElement("span", { style: { color: "#475467" } }, evItem.evidence_from_answer || evItem.status)));
    }))), activeTab === "reasoning" && /* @__PURE__ */ React13.createElement("div", { style: { lineHeight: 1.65, color: "#344054", fontSize: "0.95rem" } }, reasoning)))));
  }

  // ui/src/components/WaveformCluster.jsx
  var React14 = window.React;
  function WaveformCluster({ isRecording, side = "left" }) {
    const baseHeights = [8, 12, 16, 22, 18, 26, 32, 28, 38, 42, 34, 46, 38, 48];
    const heights = side === "left" ? baseHeights : [...baseHeights].reverse();
    return /* @__PURE__ */ React14.createElement("div", { className: `waveform-cluster ${isRecording ? "is-recording" : ""}` }, heights.map((h, i) => {
      const opacity = 0.4 + i / heights.length * 0.6;
      return /* @__PURE__ */ React14.createElement(
        "i",
        {
          key: i,
          style: {
            height: isRecording ? `${h}px` : `${Math.max(6, Math.floor(h * 0.35))}px`,
            opacity: isRecording ? opacity : 0.45,
            background: isRecording ? "#257853" : "#98A2B3"
          }
        }
      );
    }));
  }

  // ui/src/components/SpeakNaturallyCard.jsx
  var React15 = window.React;
  function SpeakNaturallyCard({ isRecording }) {
    return /* @__PURE__ */ React15.createElement("div", { className: "iv-info-card" }, /* @__PURE__ */ React15.createElement("div", { className: "iv-info-header" }, /* @__PURE__ */ React15.createElement("div", { className: "iv-info-mic-badge" }, /* @__PURE__ */ React15.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React15.createElement("path", { d: "M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" }), /* @__PURE__ */ React15.createElement("path", { d: "M19 10v2a7 7 0 0 1-14 0v-2" }), /* @__PURE__ */ React15.createElement("line", { x1: "12", y1: "19", x2: "12", y2: "23" }), /* @__PURE__ */ React15.createElement("line", { x1: "8", y1: "23", x2: "16", y2: "23" }))), /* @__PURE__ */ React15.createElement("div", { className: "iv-info-eq-bars" }, /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "12px" : "6px", transition: "height 0.2s" } }), /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "18px" : "10px", transition: "height 0.2s" } }), /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "24px" : "16px", transition: "height 0.2s" } }), /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "22px" : "20px", transition: "height 0.2s" } }), /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "16px" : "14px", transition: "height 0.2s" } }), /* @__PURE__ */ React15.createElement("span", { style: { height: isRecording ? "10px" : "8px", transition: "height 0.2s" } }))), /* @__PURE__ */ React15.createElement("h4", { className: "iv-info-title" }, "Speak naturally"), /* @__PURE__ */ React15.createElement("p", { className: "iv-info-desc" }, "Make sure the mic is picking up your voice. You can re-record if needed."));
  }

  // ui/src/screens/interview/QuestionRecordingView.jsx
  var React16 = window.React;
  function InterviewTopBar({ topic, questionNumber, substep, onBack, onStopInterview }) {
    return /* @__PURE__ */ React16.createElement("div", { className: "iv-topbar" }, /* @__PURE__ */ React16.createElement("div", { className: "iv-brand-wrap" }, /* @__PURE__ */ React16.createElement(
      "button",
      {
        type: "button",
        className: "btn-back-arrow",
        onClick: onBack,
        title: "Back to Topics",
        "aria-label": "Back to Topics",
        style: { width: "34px", height: "34px", flexShrink: 0 }
      },
      /* @__PURE__ */ React16.createElement("svg", { width: "16", height: "16", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React16.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React16.createElement("polyline", { points: "12 19 5 12 12 5" }))
    ), /* @__PURE__ */ React16.createElement(
      "img",
      {
        src: "/Images/logo.png",
        alt: "CrackProof Logo",
        className: "iv-logo",
        onClick: onBack,
        style: { cursor: "pointer" }
      }
    ), /* @__PURE__ */ React16.createElement("div", { className: "iv-breadcrumb" }, /* @__PURE__ */ React16.createElement("b", null, topic), /* @__PURE__ */ React16.createElement("span", { className: "iv-sep" }, ">"), /* @__PURE__ */ React16.createElement("span", null, "Question ", questionNumber, " of 5"), substep && /* @__PURE__ */ React16.createElement(React16.Fragment, null, /* @__PURE__ */ React16.createElement("span", { className: "iv-sep" }, ">"), /* @__PURE__ */ React16.createElement("span", null, substep)))), /* @__PURE__ */ React16.createElement("button", { type: "button", className: "btn-stop-interview", onClick: onStopInterview }, "Stop Interview"));
  }
  var TIMELINE_STEPS = [
    { step: 1, label: "Question" },
    { step: 2, label: "Your Answer" },
    { step: 3, label: "Evaluation" },
    { step: 4, label: "Next Question" },
    { step: 5, label: "Complete" }
  ];
  function InterviewTimeline({ currentStep }) {
    return /* @__PURE__ */ React16.createElement("div", { className: "iv-timeline" }, TIMELINE_STEPS.map((item, idx) => {
      const isDone = item.step < currentStep;
      const isActive = item.step === currentStep;
      const isLast = idx === TIMELINE_STEPS.length - 1;
      return /* @__PURE__ */ React16.createElement(
        "div",
        {
          key: item.step,
          className: `iv-step-item ${isActive ? "active" : ""} ${isDone ? "done" : ""}`
        },
        !isLast && /* @__PURE__ */ React16.createElement("div", { className: "iv-step-line" }),
        /* @__PURE__ */ React16.createElement("div", { className: "iv-step-circle" }, item.step),
        /* @__PURE__ */ React16.createElement("span", { className: "iv-step-label" }, item.label)
      );
    }));
  }
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
    return /* @__PURE__ */ React16.createElement("div", { className: "iv-page-wrap" }, /* @__PURE__ */ React16.createElement("div", { className: "iv-card-frame" }, /* @__PURE__ */ React16.createElement(
      InterviewTopBar,
      {
        topic,
        questionNumber,
        onBack,
        onStopInterview
      }
    ), /* @__PURE__ */ React16.createElement("div", { className: "iv-body-grid" }, /* @__PURE__ */ React16.createElement(InterviewTimeline, { currentStep: 1 }), /* @__PURE__ */ React16.createElement("div", null, /* @__PURE__ */ React16.createElement("div", { className: "iv-question-card" }, /* @__PURE__ */ React16.createElement("h2", { className: "iv-question-title" }, questionText || "Preparing your question...")), /* @__PURE__ */ React16.createElement("div", { className: "iv-voice-box" }, /* @__PURE__ */ React16.createElement("div", { className: "iv-voice-status" }, loading ? /* @__PURE__ */ React16.createElement("span", { className: "idle-text", style: { color: "var(--green)" } }, "Preparing your transcript...") : isRecording ? /* @__PURE__ */ React16.createElement("div", null, /* @__PURE__ */ React16.createElement("span", { className: "recording-text" }, "Recording..."), /* @__PURE__ */ React16.createElement("span", { className: "recording-timer" }, formatTime(recSeconds))) : /* @__PURE__ */ React16.createElement("span", { className: "idle-text" }, "Click microphone to record your answer")), /* @__PURE__ */ React16.createElement("div", { className: "iv-rec-center-row" }, /* @__PURE__ */ React16.createElement(WaveformCluster, { isRecording, side: "left" }), /* @__PURE__ */ React16.createElement(
      "button",
      {
        className: `btn-record-main ${isRecording ? "is-recording" : "is-idle"}`,
        onClick: isRecording ? onStopRecord : onStartRecord,
        disabled: loading,
        title: isRecording ? "Click to stop recording" : "Click to start recording"
      },
      isRecording ? /* @__PURE__ */ React16.createElement("span", { className: "stop-square" }) : /* @__PURE__ */ React16.createElement("svg", { width: "28", height: "28", viewBox: "0 0 24 24", fill: "none", stroke: "#FFFFFF", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React16.createElement("path", { d: "M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" }), /* @__PURE__ */ React16.createElement("path", { d: "M19 10v2a7 7 0 0 1-14 0v-2" }), /* @__PURE__ */ React16.createElement("line", { x1: "12", y1: "19", x2: "12", y2: "23" }), /* @__PURE__ */ React16.createElement("line", { x1: "8", y1: "23", x2: "16", y2: "23" }))
    ), /* @__PURE__ */ React16.createElement(WaveformCluster, { isRecording, side: "right" })), /* @__PURE__ */ React16.createElement("div", { className: "iv-voice-subtext" }, loading ? "Please wait while your answer is transcribed." : isRecording ? "Click to stop recording" : "Click microphone to start speaking"))), /* @__PURE__ */ React16.createElement(SpeakNaturallyCard, { isRecording }))));
  }

  // ui/src/screens/interview/EvaluationStageView.jsx
  var React17 = window.React;
  var { useState: useState10, useEffect: useEffect6, useRef: useRef5, useCallback } = React17;
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
    initialStage = "transcript",
    // "transcript" for Evaluation1.png, "evaluation" for Evaluation2.png
    onUpdateTranscript,
    onSubmitEvaluation,
    onNextQuestion,
    onFinish,
    onBack,
    onStopInterview,
    onRetry
  }) {
    const [stage, setStage] = useState10(evaluation ? initialStage || "evaluation" : "transcript");
    const [isEditing, setIsEditing] = useState10(false);
    const [isPlayingAudio, setIsPlayingAudio] = useState10(false);
    const [evalTab, setEvalTab] = useState10("right");
    const [activeSource, setActiveSource] = useState10(null);
    const audioInstanceRef = useRef5(null);
    const audioUrlRef = useRef5(null);
    useEffect6(() => {
      if (evaluation && initialStage === "evaluation") {
        setStage("evaluation");
      } else if (initialStage === "transcript" && !evaluation) {
        setStage("transcript");
      }
    }, [evaluation, initialStage]);
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
    useEffect6(() => {
      return () => {
        if (audioInstanceRef.current) {
          audioInstanceRef.current.pause();
        }
        if (audioUrlRef.current) URL.revokeObjectURL(audioUrlRef.current);
        audioInstanceRef.current = null;
        audioUrlRef.current = null;
      };
    }, [audioBlob]);
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
        const match = evaluation.citations.find((c) => c.claim && claimText && c.claim.trim().toLowerCase() === claimText.trim().toLowerCase());
        if (match && evaluation.sources) {
          source = evaluation.sources.find((s) => s.number === match.source_number);
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
    let bannerTitle = "Good start!";
    let bannerSubtitle = "You have the core idea. Let's look at what's missing to make it complete.";
    if (evaluation?.verdict === "CORRECT") {
      bannerTitle = "Great work!";
      bannerSubtitle = "You demonstrated solid technical understanding and covered essential core principles.";
    } else if (evaluation?.verdict === "INCORRECT") {
      bannerTitle = "Needs more practice!";
      bannerSubtitle = "Let's review the authoritative textbook references to build firm technical grounding.";
    }
    return /* @__PURE__ */ React17.createElement("div", { className: "iv-page-wrap" }, /* @__PURE__ */ React17.createElement("div", { className: "iv-card-frame" }, /* @__PURE__ */ React17.createElement(
      InterviewTopBar,
      {
        topic,
        questionNumber,
        substep: "Evaluation",
        onBack,
        onStopInterview
      }
    ), /* @__PURE__ */ React17.createElement("div", { className: "iv-body-grid" }, /* @__PURE__ */ React17.createElement(InterviewTimeline, { currentStep: 3 }), /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("div", { className: "eval-card-main" }, stage === "transcript" && /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("div", { className: "eval-top-tabs" }, /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval-top-tab active",
        onClick: () => setStage("transcript")
      },
      "Your Transcript"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval-top-tab",
        onClick: handleGoToEvaluation,
        disabled: loading || !evaluation && !transcript?.trim(),
        title: "View Technical Evaluation"
      },
      "Evaluation ",
      loading ? "(Evaluating...)" : ""
    )), /* @__PURE__ */ React17.createElement("div", { className: "eval-card-body" }, /* @__PURE__ */ React17.createElement("div", { className: "eval1-transcript-card" }, /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval1-edit-btn",
        onClick: () => setIsEditing(!isEditing),
        disabled: loading || !onUpdateTranscript
      },
      /* @__PURE__ */ React17.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React17.createElement("path", { d: "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" })),
      /* @__PURE__ */ React17.createElement("span", null, isEditing ? "Done" : "Edit")
    ), isEditing ? /* @__PURE__ */ React17.createElement(
      "textarea",
      {
        className: "inp",
        rows: 5,
        style: {
          width: "100%",
          padding: "14px",
          fontSize: "0.98rem",
          lineHeight: 1.6,
          resize: "vertical",
          marginTop: "24px",
          fontFamily: "inherit"
        },
        value: transcript,
        onChange: (e) => onUpdateTranscript(e.target.value),
        placeholder: "Type or edit your answer transcript..."
      }
    ) : /* @__PURE__ */ React17.createElement("p", { className: "eval1-transcript-text" }, transcript || "No transcript available. Please record your answer.")), /* @__PURE__ */ React17.createElement("div", { className: "eval1-status-banner" }, /* @__PURE__ */ React17.createElement("div", { className: "eval1-status-left" }, /* @__PURE__ */ React17.createElement("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React17.createElement("circle", { cx: "12", cy: "12", r: "10", fill: "#12B76A" }), /* @__PURE__ */ React17.createElement("path", { d: "M8 12.5L10.5 15L16 9.5", stroke: "#FFFFFF", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" })), /* @__PURE__ */ React17.createElement("span", null, "Review the transcript before evaluating.")), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval1-btn-listen",
        onClick: handleTogglePlayAudio
      },
      isPlayingAudio ? /* @__PURE__ */ React17.createElement(React17.Fragment, null, /* @__PURE__ */ React17.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "currentColor" }, /* @__PURE__ */ React17.createElement("rect", { x: "6", y: "4", width: "4", height: "16" }), /* @__PURE__ */ React17.createElement("rect", { x: "14", y: "4", width: "4", height: "16" })), "Pause Audio") : /* @__PURE__ */ React17.createElement(React17.Fragment, null, /* @__PURE__ */ React17.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "currentColor" }, /* @__PURE__ */ React17.createElement("polygon", { points: "5 3 19 12 5 21 5 3" })), "Listen to Audio")
    )), /* @__PURE__ */ React17.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "24px" } }, onRetry ? /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-ghost",
        style: { display: "inline-flex", alignItems: "center", gap: "6px" },
        onClick: onRetry,
        title: "Re-record your answer to this question"
      },
      /* @__PURE__ */ React17.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2" }, /* @__PURE__ */ React17.createElement("path", { d: "M1 4v6h6" }), /* @__PURE__ */ React17.createElement("path", { d: "M3.51 15a9 9 0 1 0 2.13-9.36L1 10" })),
      "Re-record Answer"
    ) : /* @__PURE__ */ React17.createElement("div", null), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval1-btn-continue",
        onClick: handleGoToEvaluation,
        disabled: loading || !transcript?.trim()
      },
      loading ? "Evaluating Answer..." : "Continue \u2192"
    )))), stage === "evaluation" && /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("div", { className: "eval-top-tabs" }, /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval-top-tab",
        onClick: () => setStage("transcript"),
        title: "Back to Your Transcript",
        style: { color: "#667085", marginRight: "6px" }
      },
      "\u2190 Your Transcript"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: `eval-top-tab ${evalTab === "right" ? "active" : ""}`,
        onClick: () => setEvalTab("right")
      },
      "What You Got Right"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: `eval-top-tab ${evalTab === "missing" ? "active" : ""}`,
        onClick: () => setEvalTab("missing")
      },
      "What's Missing"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: `eval-top-tab ${evalTab === "misconceptions" ? "active" : ""}`,
        onClick: () => setEvalTab("misconceptions")
      },
      "Misconceptions"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: `eval-top-tab ${evalTab === "depth" ? "active" : ""}`,
        onClick: () => setEvalTab("depth")
      },
      "Depth Evidence"
    ), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: `eval-top-tab ${evalTab === "reasoning" ? "active" : ""}`,
        onClick: () => setEvalTab("reasoning")
      },
      "Reasoning"
    )), /* @__PURE__ */ React17.createElement("div", { className: "eval-card-body" }, /* @__PURE__ */ React17.createElement("div", { style: { minHeight: "150px" } }, evalTab === "right" && /* @__PURE__ */ React17.createElement("div", null, !evaluation?.correct_points || evaluation.correct_points.length === 0 ? /* @__PURE__ */ React17.createElement("p", { className: "small muted", style: { padding: "18px 0" } }, "No core points were accurately identified in this response.") : evaluation.correct_points.map((point, idx) => {
      const text = typeof point === "string" ? point : point?.text || point?.claim || JSON.stringify(point);
      return /* @__PURE__ */ React17.createElement("div", { key: idx, className: "eval2-item-row" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-item-left" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-check-circle" }, /* @__PURE__ */ React17.createElement("svg", { width: "13", height: "13", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React17.createElement("path", { d: "M7 12.5L10.5 16L17 9", stroke: "#FFFFFF", strokeWidth: "2.8", strokeLinecap: "round", strokeLinejoin: "round" }))), /* @__PURE__ */ React17.createElement("p", { className: "eval2-item-text" }, text)), /* @__PURE__ */ React17.createElement(
        "button",
        {
          type: "button",
          className: "eval2-view-source",
          onClick: () => handleViewSource(point, "right")
        },
        "View Source"
      ));
    })), evalTab === "missing" && /* @__PURE__ */ React17.createElement("div", null, !evaluation?.missing_core_concepts || evaluation.missing_core_concepts.length === 0 ? /* @__PURE__ */ React17.createElement("p", { className: "small muted", style: { padding: "18px 0" } }, "No essential concepts were missed for this question.") : evaluation.missing_core_concepts.map((item, idx) => {
      const text = typeof item === "string" ? item : item?.text || item?.claim || item?.concept || JSON.stringify(item);
      return /* @__PURE__ */ React17.createElement("div", { key: idx, className: "eval2-item-row" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-item-left" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-check-circle", style: { background: "#F79009" } }, /* @__PURE__ */ React17.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React17.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "13", stroke: "#FFFFFF", strokeWidth: "2.8", strokeLinecap: "round" }), /* @__PURE__ */ React17.createElement("circle", { cx: "12", cy: "17", r: "1.5", fill: "#FFFFFF" }))), /* @__PURE__ */ React17.createElement("p", { className: "eval2-item-text" }, text)), /* @__PURE__ */ React17.createElement(
        "button",
        {
          type: "button",
          className: "eval2-view-source",
          onClick: () => handleViewSource(item, "missing")
        },
        "View Source"
      ));
    })), evalTab === "misconceptions" && /* @__PURE__ */ React17.createElement("div", null, !evaluation?.misconceptions || evaluation.misconceptions.length === 0 ? /* @__PURE__ */ React17.createElement("p", { className: "small muted", style: { padding: "18px 0" } }, "No factual misconceptions were detected in your explanation.") : evaluation.misconceptions.map((item, idx) => {
      const text = typeof item === "string" ? item : item?.text || item?.claim || JSON.stringify(item);
      return /* @__PURE__ */ React17.createElement("div", { key: idx, className: "eval2-item-row" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-item-left" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-check-circle", style: { background: "#F04438" } }, /* @__PURE__ */ React17.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React17.createElement("line", { x1: "18", y1: "6", x2: "6", y2: "18", stroke: "#FFFFFF", strokeWidth: "2.8", strokeLinecap: "round" }), /* @__PURE__ */ React17.createElement("line", { x1: "6", y1: "6", x2: "18", y2: "18", stroke: "#FFFFFF", strokeWidth: "2.8", strokeLinecap: "round" }))), /* @__PURE__ */ React17.createElement("p", { className: "eval2-item-text" }, text)), /* @__PURE__ */ React17.createElement(
        "button",
        {
          type: "button",
          className: "eval2-view-source",
          onClick: () => handleViewSource(item, "misconceptions")
        },
        "View Source"
      ));
    })), evalTab === "depth" && /* @__PURE__ */ React17.createElement("div", null, !evaluation?.deeper_concepts_to_probe || evaluation.deeper_concepts_to_probe.length === 0 ? /* @__PURE__ */ React17.createElement("p", { className: "small muted", style: { padding: "18px 0" } }, "Core depth dimensions were assessed according to syllabus standard.") : evaluation.deeper_concepts_to_probe.map((item, idx) => {
      const text = typeof item === "string" ? item : item?.text || item?.concept || JSON.stringify(item);
      return /* @__PURE__ */ React17.createElement("div", { key: idx, className: "eval2-item-row" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-item-left" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-check-circle", style: { background: "#2E90FA" } }, "\u2726"), /* @__PURE__ */ React17.createElement("p", { className: "eval2-item-text" }, text)), /* @__PURE__ */ React17.createElement(
        "button",
        {
          type: "button",
          className: "eval2-view-source",
          onClick: () => handleViewSource(item, "depth")
        },
        "View Source"
      ));
    })), evalTab === "reasoning" && /* @__PURE__ */ React17.createElement("div", null, evaluation?.reasoning && /* @__PURE__ */ React17.createElement("div", { style: { background: "#F9FAFB", border: "1px solid #EAECF0", borderRadius: "10px", padding: "16px 20px", marginBottom: "16px" } }, /* @__PURE__ */ React17.createElement("div", { style: { fontWeight: 700, fontSize: "0.92rem", color: "#101828", marginBottom: "6px" } }, "Technical Evaluator Analysis:"), /* @__PURE__ */ React17.createElement("p", { className: "small", style: { lineHeight: 1.6, color: "#344054", margin: 0 } }, evaluation.reasoning)), Array.isArray(evaluation?.citations) && evaluation.citations.length > 0 && /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("div", { style: { fontWeight: 600, fontSize: "0.88rem", color: "#101828", marginBottom: "8px" } }, "Authoritative Textbook Citations:"), evaluation.citations.map((c, idx) => /* @__PURE__ */ React17.createElement("div", { key: idx, className: "eval2-item-row", style: { padding: "10px 0" } }, /* @__PURE__ */ React17.createElement("span", { className: "small", style: { color: "#344054", flex: 1 } }, '"', typeof c === "string" ? c : c.claim || JSON.stringify(c), '"'), /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "eval2-view-source",
        onClick: () => handleViewSource(c, "citations")
      },
      "[Source ",
      c.source_number || idx + 1,
      "]"
    )))))), /* @__PURE__ */ React17.createElement("div", { className: "eval2-bottom-banner" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-banner-left" }, /* @__PURE__ */ React17.createElement("div", { className: "eval2-big-check" }, /* @__PURE__ */ React17.createElement("svg", { width: "24", height: "24", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React17.createElement("path", { d: "M7 12.5L10.5 16L17 9", stroke: "#FFFFFF", strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }))), /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("div", { className: "eval2-banner-title" }, bannerTitle), /* @__PURE__ */ React17.createElement("p", { className: "eval2-banner-sub" }, bannerSubtitle))), /* @__PURE__ */ React17.createElement("div", { className: "eval2-banner-right" }, /* @__PURE__ */ React17.createElement("svg", { width: "74", height: "74", viewBox: "0 0 100 100", fill: "none", xmlns: "http://www.w3.org/2000/svg" }, /* @__PURE__ */ React17.createElement("ellipse", { cx: "50", cy: "85", rx: "32", ry: "6", fill: "#88A090", opacity: "0.4" }), /* @__PURE__ */ React17.createElement("path", { d: "M50 85V44", stroke: "#257853", strokeWidth: "4.5", strokeLinecap: "round" }), /* @__PURE__ */ React17.createElement("path", { d: "M50 64C50 64 26 62 18 46C16 41 20 36 28 38C38 41 48 53 50 64Z", fill: "#58A87D" }), /* @__PURE__ */ React17.createElement("path", { d: "M50 58C50 58 74 56 82 40C84 35 80 30 72 32C62 35 52 47 50 58Z", fill: "#75C296" }), /* @__PURE__ */ React17.createElement("circle", { cx: "50", cy: "34", r: "4.5", fill: "#58A87D" })))), /* @__PURE__ */ React17.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "24px" } }, /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-ghost",
        onClick: () => setStage("transcript"),
        style: { display: "inline-flex", alignItems: "center", gap: "6px" }
      },
      "\u2190 Back to Transcript"
    ), batchDone ? /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-primary",
        style: { padding: "12px 30px" },
        onClick: onFinish,
        disabled: loading
      },
      "View Final Report \u2192"
    ) : /* @__PURE__ */ React17.createElement(
      "button",
      {
        type: "button",
        className: "btn btn-primary",
        style: { padding: "12px 30px" },
        onClick: onNextQuestion,
        disabled: loading
      },
      "Next Question \u2192"
    )))))))), activeSource && /* @__PURE__ */ React17.createElement(
      "div",
      {
        style: {
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
        },
        onClick: () => setActiveSource(null)
      },
      /* @__PURE__ */ React17.createElement(
        "div",
        {
          style: {
            background: "#FFFFFF",
            borderRadius: "14px",
            maxWidth: "540px",
            width: "100%",
            padding: "24px",
            boxShadow: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)"
          },
          onClick: (e) => e.stopPropagation()
        },
        /* @__PURE__ */ React17.createElement("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "14px" } }, /* @__PURE__ */ React17.createElement("div", null, /* @__PURE__ */ React17.createElement("span", { className: "eyebrow", style: { color: "var(--green)" } }, "Evaluation Reference"), /* @__PURE__ */ React17.createElement("h3", { style: { fontSize: "1.2rem", margin: "4px 0 0", color: "#101828" } }, activeSource.title), activeSource.section && /* @__PURE__ */ React17.createElement("div", { className: "small muted", style: { marginTop: "2px" } }, "Curriculum Section: ", activeSource.section)), /* @__PURE__ */ React17.createElement(
          "button",
          {
            type: "button",
            onClick: () => setActiveSource(null),
            style: { background: "none", border: "none", fontSize: "1.5rem", cursor: "pointer", color: "#98A2B3", lineHeight: 1 }
          },
          "\xD7"
        )),
        /* @__PURE__ */ React17.createElement("div", { style: { background: "#F9FAFB", border: "1px solid #EAECF0", borderRadius: "8px", padding: "14px 16px", margin: "16px 0", lineHeight: 1.6, fontSize: "0.92rem", color: "#344054" } }, activeSource.claim ? /* @__PURE__ */ React17.createElement("p", { style: { margin: 0 } }, /* @__PURE__ */ React17.createElement("b", null, "Evaluated Claim:"), ' "', activeSource.claim, '"') : /* @__PURE__ */ React17.createElement("p", { style: { margin: 0 } }, "No claim-specific reference is available.")),
        /* @__PURE__ */ React17.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: "10px", marginTop: "18px" } }, activeSource.url && /* @__PURE__ */ React17.createElement(
          "a",
          {
            href: activeSource.url,
            target: "_blank",
            rel: "noopener noreferrer",
            className: "btn btn-primary small",
            style: { padding: "8px 16px", textDecoration: "none" }
          },
          "Open Source Reference \u2197"
        ), /* @__PURE__ */ React17.createElement(
          "button",
          {
            type: "button",
            className: "btn btn-secondary small",
            style: { padding: "8px 16px" },
            onClick: () => setActiveSource(null)
          },
          "Close"
        ))
      )
    ));
  }
  function TranscriptReviewView(props) {
    return /* @__PURE__ */ React17.createElement(EvaluationStageView, { ...props, initialStage: "transcript" });
  }
  function EvaluationResultView(props) {
    return /* @__PURE__ */ React17.createElement(EvaluationStageView, { ...props, initialStage: "evaluation" });
  }

  // ui/src/screens/interview/FinalReportView.jsx
  var React18 = window.React;
  function FinalReportView({ report, onRestartTopic, onChooseNewTopic, onReturnDashboard }) {
    const readinessVal = report?.metrics?.overall_readiness || report?.readiness;
    const readiness = formatReadiness(readinessVal);
    const profile = report?.dimension_profile || report?.depth_profile || {};
    const summary = report?.summary || report?.assessment?.summary || (report?.in_progress ? "These results cover your completed answers so far." : "The written assessment is unavailable. Your evaluated answers and calculated results are saved.");
    const questionsCount = report?.metrics?.questions_answered ?? report?.questions_answered ?? 0;
    return /* @__PURE__ */ React18.createElement("div", { className: "wrap", style: { paddingTop: "24px", paddingBottom: "50px", position: "relative" } }, /* @__PURE__ */ React18.createElement(
      "button",
      {
        type: "button",
        className: "btn-back-arrow",
        onClick: onReturnDashboard,
        title: "Back to Dashboard",
        "aria-label": "Back",
        style: { position: "absolute", left: "0", top: "24px" }
      },
      /* @__PURE__ */ React18.createElement("svg", { width: "18", height: "18", viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2.2", strokeLinecap: "round", strokeLinejoin: "round" }, /* @__PURE__ */ React18.createElement("line", { x1: "19", y1: "12", x2: "5", y2: "12" }), /* @__PURE__ */ React18.createElement("polyline", { points: "12 19 5 12 12 5" }))
    ), /* @__PURE__ */ React18.createElement("div", { style: { textAlign: "center", marginBottom: "28px" } }, /* @__PURE__ */ React18.createElement("span", { className: "eyebrow" }, report?.in_progress ? "Interview In Progress" : "Interview Complete"), /* @__PURE__ */ React18.createElement("h1", { style: { fontSize: "1.75rem", marginTop: "6px" } }, "Candidate Evaluation Report"), /* @__PURE__ */ React18.createElement("p", { className: "small muted", style: { marginTop: "4px" } }, report?.topic || "Technical Interview", " \xB7 ", questionsCount, " questions evaluated")), /* @__PURE__ */ React18.createElement("div", { className: "card readiness", style: { padding: "26px", marginBottom: "20px" } }, /* @__PURE__ */ React18.createElement("h3", null, "Performance in This Interview"), /* @__PURE__ */ React18.createElement("div", { style: { margin: "14px 0" } }, /* @__PURE__ */ React18.createElement("span", { className: `pill ${readiness.pill}`, style: { fontSize: "1rem", padding: "8px 18px" } }, readiness.text)), /* @__PURE__ */ React18.createElement("p", { className: "small muted", style: { lineHeight: 1.5 } }, summary), report?.limited_evidence && /* @__PURE__ */ React18.createElement("p", { className: "small muted" }, "This report uses fewer than five completed answers, so it covers a limited sample of your knowledge.")), /* @__PURE__ */ React18.createElement("div", { className: "card readiness", style: { padding: "26px", marginBottom: "28px" } }, /* @__PURE__ */ React18.createElement("h3", null, "Profile Breakdown"), /* @__PURE__ */ React18.createElement("div", { className: "scores", style: { marginTop: "16px", display: "grid", gap: "14px" } }, Object.entries(profile).map(([dim, score]) => {
      let numScore = 0;
      let displayScore = "";
      let pct = 0;
      if (typeof score === "number") {
        numScore = score;
        displayScore = `${score}/10`;
        pct = Math.min(100, Math.round(numScore / 10 * 100));
      } else if (score && typeof score === "object") {
        if (score.score !== void 0) {
          numScore = Number(score.score) || 0;
          displayScore = `${numScore}/10`;
          pct = Math.min(100, Math.round(numScore / 10 * 100));
        } else if (score.tested !== void 0) {
          const tested = score.tested || 0;
          if (tested > 0) {
            const demonstrated = score.demonstrated || 0;
            const partial = score.partially_demonstrated || 0;
            displayScore = `${demonstrated} demonstrated, ${partial} partial / ${tested} tested`;
            pct = Math.min(100, Math.round(demonstrated / tested * 100));
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
      return /* @__PURE__ */ React18.createElement("div", { key: dim }, /* @__PURE__ */ React18.createElement("div", { className: "score-top", style: { display: "flex", justifyContent: "space-between", marginBottom: "4px" } }, /* @__PURE__ */ React18.createElement("span", null, niceDimensionName(dim)), /* @__PURE__ */ React18.createElement("b", null, displayScore)), /* @__PURE__ */ React18.createElement("div", { className: "rbar", style: { height: "8px", background: "#EAEFEA", borderRadius: "4px", overflow: "hidden" } }, /* @__PURE__ */ React18.createElement("i", { style: { display: "block", height: "100%", width: `${pct}%`, background: pct > 0 ? "var(--green)" : "#D0D5DD", borderRadius: "4px" } })));
    }))), report?.assessment && /* @__PURE__ */ React18.createElement("div", { className: "card", style: { padding: "26px", marginBottom: "28px" } }, [
      ["demonstrated_strengths", "Demonstrated Strengths"],
      ["developing_areas", "Developing Areas"],
      ["recurring_knowledge_gaps", "Knowledge Gaps"],
      ["persistent_misconceptions", "Misconceptions to Review"],
      ["insufficiently_tested_areas", "Areas Not Sufficiently Tested"],
      ["recommended_revision_topics", "Recommended Revision Topics"]
    ].map(([field, label]) => report.assessment[field]?.length > 0 && /* @__PURE__ */ React18.createElement("section", { key: field, style: { marginBottom: "18px" } }, /* @__PURE__ */ React18.createElement("h3", null, label), /* @__PURE__ */ React18.createElement("ul", { style: { paddingLeft: "20px", lineHeight: 1.6 } }, report.assessment[field].map((item, index) => /* @__PURE__ */ React18.createElement("li", { key: index }, item)))))), /* @__PURE__ */ React18.createElement("div", { style: { display: "flex", gap: "12px", justifyContent: "center", flexWrap: "wrap" } }, /* @__PURE__ */ React18.createElement("button", { className: "btn btn-primary", style: { padding: "12px 24px" }, onClick: onRestartTopic }, "Practice Another 5 Questions"), /* @__PURE__ */ React18.createElement("button", { className: "btn btn-ghost", style: { padding: "12px 24px" }, onClick: onChooseNewTopic }, "Choose Different Topic"), /* @__PURE__ */ React18.createElement("button", { className: "btn btn-ghost", style: { padding: "12px 24px" }, onClick: onReturnDashboard }, "Return to Dashboard")));
  }

  // ui/src/App.jsx
  var React19 = window.React;
  var { useState: useState11, useEffect: useEffect7, useReducer, useCallback: useCallback2, useRef: useRef6 } = React19;
  var ErrorBoundary = class extends React19.Component {
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
        return /* @__PURE__ */ React19.createElement("div", { style: { padding: "40px 20px", textAlign: "center", maxWidth: "600px", margin: "60px auto" } }, /* @__PURE__ */ React19.createElement("h2", { style: { color: "#D92D20", marginBottom: "12px" } }, "Something went wrong"), /* @__PURE__ */ React19.createElement("p", { style: { color: "#667085", lineHeight: 1.5 } }, this.state.error?.message || "An unexpected error occurred while rendering the view."), /* @__PURE__ */ React19.createElement(
          "button",
          {
            type: "button",
            className: "btn btn-primary",
            style: { marginTop: "20px", padding: "10px 24px" },
            onClick: () => {
              this.setState({ hasError: false, error: null });
              window.location.reload();
            }
          },
          "Reload Page"
        ));
      }
      return this.props.children;
    }
  };
  function App() {
    const [route, setRoute] = useState11("login");
    const [user, setUser] = useState11(null);
    const [isGuest, setIsGuest] = useState11(false);
    const [history, setHistory] = useState11([]);
    const [initialSignupEmail, setInitialSignupEmail] = useState11("");
    const [selectedHistorySubject, setSelectedHistorySubject] = useState11("Java");
    const [historySubjectQuestions, setHistorySubjectQuestions] = useState11([]);
    const [selectedQuestionIndex, setSelectedQuestionIndex] = useState11(0);
    const [historyLoading, setHistoryLoading] = useState11(false);
    const [isStopping, setIsStopping] = useState11(false);
    const [interview, dispatch] = useReducer(interviewReducer, initialInterviewState);
    const mediaRecorderRef = useRef6(null);
    const audioChunksRef = useRef6([]);
    const timerIntervalRef = useRef6(null);
    const operationRef = useRef6(0);
    const busyRef = useRef6(false);
    const recordingVersionRef = useRef6(0);
    const startingRecordingRef = useRef6(false);
    const navigationRef = useRef6(0);
    const transcriptionRef = useRef6(null);
    const cancelRecording = useCallback2(() => {
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
          recorder.stream.getTracks().forEach((track) => track.stop());
        }
      }
      mediaRecorderRef.current = null;
    }, []);
    const navigate = useCallback2((targetScreen) => {
      navigationRef.current += 1;
      setRoute(targetScreen);
      window.scrollTo(0, 0);
    }, []);
    const loadHistory = useCallback2(async () => {
      const navigation = navigationRef.current;
      const res = await apiRequest("/api/history");
      if (navigation !== navigationRef.current) return;
      if (res.ok && res.interviews) {
        setHistory(res.interviews);
      }
    }, []);
    useEffect7(() => {
    }, []);
    useEffect7(() => {
      if (route === "dash" || route === "topics" || route === "progress") {
        loadHistory();
      }
    }, [route, loadHistory]);
    const handleLogin = useCallback2(async (email, password) => {
      const res = await apiRequest("/api/login", { email, password });
      if (res.ok && res.user) {
        setUser(res.user);
        setIsGuest(false);
        navigate("dash");
        return null;
      }
      return res.message || "Invalid credentials.";
    }, [navigate]);
    const handleSignup = useCallback2(async (name, email, password) => {
      const res = await apiRequest("/api/signup", { name, email, password });
      if (res.ok && res.user) {
        setUser(res.user);
        setIsGuest(false);
        navigate("dash");
        return null;
      }
      return res.message || "Could not create account.";
    }, [navigate]);
    const handleGuestLogin = useCallback2(async () => {
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
    const handleLogout = useCallback2(async () => {
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
    const handleSelectHistorySubject = useCallback2(async (subjectName) => {
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
    const handleSelectHistoryQuestion = useCallback2((index) => {
      setSelectedQuestionIndex(index);
      navigate("history_question");
    }, [navigate]);
    const handleStartTopic = useCallback2(async (topic) => {
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
    const handleStartRecord = useCallback2(async () => {
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
          stream.getTracks().forEach((track) => track.stop());
          return;
        }
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
        const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : void 0);
        mediaRecorderRef.current = recorder;
        recorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) {
            audioChunksRef.current.push(e.data);
          }
        };
        recorder.onstop = async () => {
          clearInterval(timerIntervalRef.current);
          try {
            if (recorder.stream) {
              recorder.stream.getTracks().forEach((track) => track.stop());
            }
          } catch (e) {
          }
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
          const timeout = setTimeout(() => controller.abort(), 18e4);
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
        recorder.start(500);
        dispatch({ type: "START_RECORDING" });
        if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = setInterval(() => {
          dispatch({ type: "TICK_TIMER" });
        }, 1e3);
      } catch (e) {
        stream?.getTracks().forEach((track) => track.stop());
        if (recordingVersion !== recordingVersionRef.current) return;
        alert(e.name === "NotAllowedError" ? "Please allow microphone access to record your answer." : e.message || "Could not start recording. Please check your microphone.");
      } finally {
        if (recordingVersion === recordingVersionRef.current) startingRecordingRef.current = false;
      }
    }, [interview.interviewId, interview.questionNumber, cancelRecording]);
    const handleStopRecord = useCallback2(() => {
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
    const handleSubmitEvaluation = useCallback2(async () => {
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
    const handleNextQuestion = useCallback2(async () => {
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
    const handleBackFromInterview = useCallback2(() => {
      operationRef.current += 1;
      busyRef.current = false;
      cancelRecording();
      dispatch({ type: "RESET" });
      navigate("topics");
    }, [navigate, cancelRecording]);
    const handleFinishReport = useCallback2(async () => {
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
    const handleStopInterview = useCallback2(async () => {
      if (busyRef.current) return;
      cancelRecording();
      const hasCompletedAnswers = interview.questionNumber > 1 || interview.status === "EVALUATION";
      if (!hasCompletedAnswers) {
        handleBackFromInterview();
        return;
      }
      if (interview.status === "RECORDING") dispatch({ type: "RECORDING_FAILED" });
      await handleFinishReport();
    }, [interview.questionNumber, interview.status, cancelRecording, handleBackFromInterview, handleFinishReport]);
    const handleOpenPastReport = useCallback2(async (id) => {
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
    useEffect7(() => {
      return () => {
        operationRef.current += 1;
        cancelRecording();
      };
    }, [cancelRecording]);
    const historyCounts = history.reduce((acc, row) => {
      acc[row.topic] = (acc[row.topic] || 0) + (row.questions_answered || 0);
      return acc;
    }, {});
    return /* @__PURE__ */ React19.createElement("div", { className: !["login", "signup", "interview", "history_subject", "history_question"].includes(route) ? "workspace-shell" : "" }, route !== "login" && route !== "signup" && route !== "interview" && route !== "history_subject" && route !== "history_question" && /* @__PURE__ */ React19.createElement(
      WorkspaceNav,
      {
        user,
        isGuest,
        activeRoute: route,
        onNavigate: navigate,
        onLogout: handleLogout
      }
    ), route === "login" && /* @__PURE__ */ React19.createElement(
      LoginScreen,
      {
        onLogin: handleLogin,
        onSwitchToSignup: (em) => {
          setInitialSignupEmail(em);
          navigate("signup");
        },
        onGuestLogin: handleGuestLogin
      }
    ), route === "signup" && /* @__PURE__ */ React19.createElement(
      SignupScreen,
      {
        initialEmail: initialSignupEmail,
        onSignup: handleSignup,
        onSwitchToLogin: () => navigate("login")
      }
    ), route === "dash" && /* @__PURE__ */ React19.createElement(
      DashboardScreen,
      {
        user,
        isGuest,
        history,
        onStartInterview: () => navigate("topics"),
        onSetupInterview: () => navigate("profile"),
        onOpenPanel: () => navigate("panel"),
        onOpenPastReport: handleOpenPastReport
      }
    ), route === "profile" && /* @__PURE__ */ React19.createElement(ResumeSetupScreen, { isGuest, onPractice: () => navigate("topics"), onPanel: () => navigate("panel") }), route === "panel" && /* @__PURE__ */ React19.createElement(PanelScreen, { isGuest, onSetup: () => navigate("profile") }), route === "topics" && /* @__PURE__ */ React19.createElement(
      TopicsScreen,
      {
        onSelectTopic: handleStartTopic,
        onBack: () => navigate("dash"),
        historyCounts
      }
    ), route === "progress" && /* @__PURE__ */ React19.createElement(
      ProgressScreen,
      {
        user,
        isGuest,
        history,
        historyCounts,
        onStartInterview: () => navigate("topics"),
        onSelectTopic: handleStartTopic,
        onOpenPastReport: handleOpenPastReport,
        onBack: () => navigate("dash")
      }
    ), route === "history" && /* @__PURE__ */ React19.createElement(
      HistoryScreen,
      {
        user,
        isGuest,
        historyCounts,
        onSelectSubject: handleSelectHistorySubject,
        onBack: () => navigate("dash")
      }
    ), route === "history_subject" && /* @__PURE__ */ React19.createElement(
      SubjectHistoryScreen,
      {
        subject: selectedHistorySubject,
        questions: historySubjectQuestions,
        loading: historyLoading,
        onSelectQuestion: handleSelectHistoryQuestion,
        onBack: () => navigate("history"),
        onNavigate: navigate,
        onStartInterview: handleStartTopic
      }
    ), route === "history_question" && /* @__PURE__ */ React19.createElement(
      QuestionPreviewScreen,
      {
        subject: selectedHistorySubject,
        questions: historySubjectQuestions,
        currentIndex: selectedQuestionIndex,
        onBack: () => navigate("history_subject"),
        onNavigateIndex: (idx) => setSelectedQuestionIndex(idx),
        onNavigate: navigate
      }
    ), route === "interview" && /* @__PURE__ */ React19.createElement("div", null, interview.status === "LOADING" && /* @__PURE__ */ React19.createElement("div", { className: "interview-loading-container" }, /* @__PURE__ */ React19.createElement("img", { src: "/Images/logo.png", alt: "CrackProof Logo", className: "interview-pulse-logo" }), /* @__PURE__ */ React19.createElement("h2", { style: { fontSize: "1.5rem", fontWeight: 700, color: "#101828", marginBottom: "8px" } }, "Preparing your ", interview.topic, " Technical Interview"), /* @__PURE__ */ React19.createElement("p", { style: { color: "#667085", fontSize: "0.98rem" } }, "Formulating foundational questions and setting up textbook evaluation rubrics...")), interview.status === "QUESTION" && /* @__PURE__ */ React19.createElement(
      QuestionRecordingView,
      {
        topic: interview.topic,
        questionNumber: interview.questionNumber,
        questionText: interview.questionText,
        isRecording: false,
        recSeconds: 0,
        loading: interview.loading,
        onStartRecord: handleStartRecord,
        onStopRecord: handleStopRecord,
        onBack: handleBackFromInterview,
        onStopInterview: handleStopInterview
      }
    ), interview.status === "RECORDING" && /* @__PURE__ */ React19.createElement(
      QuestionRecordingView,
      {
        topic: interview.topic,
        questionNumber: interview.questionNumber,
        questionText: interview.questionText,
        isRecording: true,
        recSeconds: interview.recSeconds,
        loading: interview.loading,
        onStartRecord: handleStartRecord,
        onStopRecord: handleStopRecord,
        onBack: handleBackFromInterview,
        onStopInterview: handleStopInterview
      }
    ), interview.status === "REVIEW" && /* @__PURE__ */ React19.createElement(
      TranscriptReviewView,
      {
        topic: interview.topic,
        questionNumber: interview.questionNumber,
        questionText: interview.questionText,
        transcript: interview.transcript,
        audioBlob: interview.audioBlob,
        loading: interview.loading,
        onUpdateTranscript: (val) => dispatch({ type: "UPDATE_TRANSCRIPT", payload: val }),
        onSubmitEvaluation: handleSubmitEvaluation,
        onRetry: handleStartRecord,
        onBack: handleBackFromInterview,
        onStopInterview: handleStopInterview
      }
    ), interview.status === "EVALUATION" && /* @__PURE__ */ React19.createElement(
      EvaluationResultView,
      {
        topic: interview.topic,
        questionNumber: interview.questionNumber,
        questionText: interview.questionText,
        transcript: interview.transcript,
        audioBlob: interview.audioBlob,
        audioPath: interview.audioPath,
        loading: interview.loading,
        evaluation: interview.evaluation,
        batchDone: interview.batchDone,
        onNextQuestion: handleNextQuestion,
        onFinish: handleFinishReport,
        onBack: handleBackFromInterview,
        onStopInterview: handleStopInterview
      }
    )), route === "report" && /* @__PURE__ */ React19.createElement(
      FinalReportView,
      {
        report: interview.report,
        onRestartTopic: () => handleStartTopic(interview.report?.topic || "Java"),
        onChooseNewTopic: () => navigate("topics"),
        onReturnDashboard: () => navigate("dash")
      }
    ), isStopping && /* @__PURE__ */ React19.createElement("div", { className: "stop-loading-backdrop" }, /* @__PURE__ */ React19.createElement("div", { className: "stop-loading-card" }, /* @__PURE__ */ React19.createElement("div", { className: "stop-spinner" }), /* @__PURE__ */ React19.createElement("h3", { style: { fontSize: "1.25rem", fontWeight: 700, color: "#101828", margin: "0 0 8px" } }, "Ending Interview Session"), /* @__PURE__ */ React19.createElement("p", { style: { color: "#667085", fontSize: "0.92rem", margin: 0 } }, "Compiling your demonstrated strengths, knowledge gaps, and evaluation report..."))));
  }
  var rootElement = document.getElementById("root");
  if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
      /* @__PURE__ */ React19.createElement(ErrorBoundary, null, /* @__PURE__ */ React19.createElement(App, null))
    );
  }
})();
