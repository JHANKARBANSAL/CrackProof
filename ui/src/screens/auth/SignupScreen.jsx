const React = window.React;
const { useState } = React;

export function SignupScreen({ onSignup, onSwitchToLogin, initialEmail = "" }) {
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
        <div className="auth-card">
          <div className="auth-brand">
            <img src="/Images/logo.png" alt="CrackProof Logo" className="auth-logo" />
            <p className="auth-tagline">Practice. Understand. Improve.</p>
          </div>

          <h1 className="auth-title">Create Account</h1>
          <p className="auth-subtitle">Join CrackProof to save and track your progress</p>

          <form onSubmit={handleSubmit}>
            <div className="auth-field">
              <label htmlFor="signupName">Full Name</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <input
                  id="signupName"
                  className="inp"
                  type="text"
                  placeholder="Your Name"
                  autoComplete="name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </div>

            <div className="auth-field">
              <label htmlFor="signupEmail">Email</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                <input
                  id="signupEmail"
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
              <label htmlFor="signupPw">Password</label>
              <div className="input-wrap">
                <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                </svg>
                <input
                  id="signupPw"
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
              {loading ? "Creating Account..." : "Sign Up"}
            </button>
          </form>

          <p className="auth-footer">
            Already have an account?{" "}
            <a href="#" onClick={(e) => { e.preventDefault(); onSwitchToLogin(); }}>
              Sign in
            </a>
          </p>
        </div>

        <div className="auth-illustration">
          <span className="eyebrow">YOUR NEXT CHAPTER STARTS HERE</span>
          <h2>Turn practice into<br />your next opportunity.</h2>
          <img src="/Images/interview-desk.png" alt="An illustrated interview workspace with a laptop and a confidence checkmark" />
          <p>Build your profile. Practice your skills. Find your voice.</p>
        </div>
      </div>
    </div>
  );
}
