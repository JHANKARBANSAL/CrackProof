const React = window.React;
const { useState } = React;

export function LoginScreen({ onLogin, onSwitchToSignup, onGuestLogin }) {
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
        <div className="auth-card">
          <div className="auth-brand">
            <img src="/Images/logo.png" alt="CrackProof Logo" className="auth-logo" />
            <p className="auth-tagline">Practice. Understand. Improve.</p>
          </div>

          <h1 className="auth-title">Your next chapter<br/>starts here.</h1>
          <p className="auth-subtitle">Sign in to your interview workspace.</p>

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

        <div className="auth-illustration">
          <span className="eyebrow">PRACTICE FOR WHAT'S NEXT</span><h2>Good preparation.<br/>A different kind of confidence.</h2><img src="/Images/interview-desk.png" alt="A laptop and conversation tools for interview preparation" /><p>Core concepts. Your own story. A panel that challenges you.</p>
        </div>
      </div>
    </div>
  );
}
