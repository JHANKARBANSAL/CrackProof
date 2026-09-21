const React = window.React;

export function Navbar({ user, isGuest, activeRoute, onNavigate, onLogout }) {
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
          <button type="button" className={activeRoute === "profile" ? "on" : ""} onClick={() => onNavigate("profile")}>My Profile</button>
          <button type="button" className={activeRoute === "panel" ? "on" : ""} onClick={() => onNavigate("panel")}>AI Panel</button>
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

          <div className="nav-vertical-divider" aria-hidden="true" />

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
