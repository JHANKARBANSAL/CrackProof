const React = window.React;
import { Icon } from "./Icon.jsx";
const links = [
  ["dash", "Overview", "layout-dashboard"], ["topics", "Knowledge practice", "book-open"],
  ["panel", "AI interview panel", "audio-lines"], ["profile", "My profile", "contact-round"],
  ["progress", "My progress", "chart-no-axes-combined"], ["history", "Practice history", "history"]
];
export function WorkspaceNav({ user, isGuest, activeRoute, onNavigate, onLogout }) {
  const name = isGuest ? "Guest" : user?.name || user?.email?.split("@")[0] || "Candidate";
  return <>
    <aside className="workspace-sidebar">
      <button className="workspace-brand" onClick={() => onNavigate("dash")} aria-label="CrackProof home"><img src="/Images/logo.png" alt="CrackProof" /><span>INTERVIEW STUDIO</span></button>
      <span className="sidebar-caption">YOUR WORKSPACE</span>
      <nav aria-label="Main navigation">{links.map(([route, label, icon]) => <button key={route} aria-current={activeRoute === route ? "page" : undefined} className={activeRoute === route ? "active" : ""} onClick={() => onNavigate(route)}><Icon name={icon}/><span>{label}</span>{route === "panel" && <span className="nav-new">AI</span>}</button>)}</nav>
      <div className="sidebar-tip"><Icon name="sparkles" size={22}/><strong>A little practice.<br/>A lot more confidence.</strong><p>Bring your experience. Find your next step.</p><button onClick={() => onNavigate("profile")}>Build your profile <Icon name="arrow-up-right" size={16}/></button></div>
      <div className="sidebar-account"><div className="avatar">{name[0].toUpperCase()}</div><div><strong>{name}</strong><small>{isGuest ? "Guest workspace" : "Personal workspace"}</small></div><button onClick={onLogout} title="Sign out" aria-label="Sign out"><Icon name="log-out" size={18}/></button></div>
    </aside>
    <header className="workspace-topbar"><div><span className="muted">Workspace</span><span className="topbar-slash">/</span><strong>{links.find(item => item[0] === activeRoute)?.[1] || "Practice report"}</strong></div><span className="workspace-mode"><span/>{isGuest ? "Guest mode" : "Your practice space"}</span></header>
  </>;
}
