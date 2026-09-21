const React = window.React;
const { useEffect, useRef, useState } = React;
import { apiRequest } from "../../api/client.js";
import { RolePicker } from "../../components/RolePicker.jsx";
import { Icon } from "../../components/Icon.jsx";

const emptyProfile = {
  target_role: "", experience_level: "Fresher", job_description: "",
  skills: [], projects: [], education: "", work_summary: ""
};

export function ResumeSetupScreen({ isGuest, onPractice, onPanel }) {
  const [profile, setProfile] = useState(emptyProfile);
  const [skillsText, setSkillsText] = useState("");
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [loadFailed, setLoadFailed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [file, setFile] = useState(null);
  const [extracted, setExtracted] = useState(null);
  const [saved, setSaved] = useState(false);
  const [jdReview, setJdReview] = useState(null);
  const [reviewingJD, setReviewingJD] = useState(false);
  const uploadController = useRef(null);
  const mounted = useRef(true);
  const busyRef = useRef(false);

  useEffect(() => {
    mounted.current = true;
    loadProfile();
    return () => { mounted.current = false; uploadController.current?.abort(); };
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
    setProfile(previous => ({ ...previous, [field]: value }));
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
    if (file.size > 5 * 1024 * 1024) { setError("Please select a PDF smaller than 5 MB."); return; }
    busyRef.current = true;
    setBusy(true);
    setError("");
    setExtracted(null);
    const controller = new AbortController();
    uploadController.current = controller;
    const timeout = setTimeout(() => controller.abort(), 180000);
    try {
      const body = new FormData();
      body.append("resume", file);
      const response = await fetch("/api/resume/parse", { method: "POST", body, signal: controller.signal });
      if (response.status === 413) throw new Error("Please select a smaller PDF.");
      const result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.message || "Could not analyze this resume.");
      if (mounted.current) setExtracted(result.details);
    } catch (error) {
      if (mounted.current) setError(error.name === "AbortError" ? "Analysis timed out. Retry or enter details manually." : error.message);
    } finally {
      clearTimeout(timeout);
      uploadController.current = null;
      busyRef.current = false;
      if (mounted.current) setBusy(false);
    }
  }

  function applyExtracted() {
    setProfile(previous => ({ ...previous, ...extracted }));
    setSkillsText(extracted.skills.join(", "));
    setExtracted(null);
    setSaved(false);
    setNotice("Resume details added to the form. Check and correct them before saving.");
  }

  function next(event) {
    event.preventDefault();
    setError("");
    if (step === 1) {
      const skills = [...new Set(skillsText.split(",").map(value => value.trim()).filter(Boolean))];
      if (!skills.length || skills.length > 30 || skills.some(value => value.length > 120)) {
        setError("Enter 1–30 skills, separated by commas. Keep each skill under 120 characters.");
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
    if (!result.ok) { setError(result.message); return; }
    setNotice("");
    setSaved(true);
    setProfile(result.profile);
    setSkillsText(result.profile.skills.join(", "));
  }

  if (loading) return <div className="wrap" role="status">Loading your interview setup…</div>;
  if (loadFailed) return <div className="wrap"><p role="alert">{error}</p><button className="btn btn-primary" onClick={loadProfile}>Retry loading setup</button></div>;

  return <main className="wrap setup-page">
    <div className="setup-heading"><span className="eyebrow">MAKE IT PERSONAL</span>
      <h1>Your ambition. Your interview.</h1>
      <p className="muted">A little context helps us ask the right questions.</p>
    </div>
    <ol className="setup-steps" aria-label="Setup progress">
      {["Your goal", "Resume & skills", "Review & save"].map((label, index) => <li key={label} aria-current={step === index ? "step" : undefined} className={step === index ? "active" : ""}><span>{index + 1}</span>{label}</li>)}
    </ol>
    {error && <p className="formError" role="alert">{error}</p>}
    {notice && <p className="setup-notice" role="status">{notice}</p>}
    <div className="profile-layout"><form onSubmit={next} className="card setup-card">
      <fieldset disabled={busy} className="setup-fields">
        {step === 0 && <>
          <div className="form-section-heading"><span className="section-icon"><Icon name="target"/></span><div><h2>Set your direction</h2><p className="muted">Tell us where you want to go.</p></div></div>
          <RolePicker value={profile.target_role} onChange={value => update("target_role", value)} />
          <label>Experience <select className="inp" value={profile.experience_level} onChange={event => update("experience_level", event.target.value)}>{["Fresher", "0–2 years", "3–5 years", "5+ years"].map(level => <option key={level}>{level}</option>)}</select></label>
          <div className="jd-block"><label htmlFor="job-description">Have a specific job in mind? <span className="optional-tag">OPTIONAL</span></label><p className="field-hint">Paste its description to focus your panel on the actual responsibilities and skills.</p><textarea id="job-description" className="inp" rows={5} maxLength={8000} value={profile.job_description} onChange={event => update("job_description", event.target.value)} placeholder="Paste responsibilities, required skills and experience from the job posting…" />
            <div className="jd-action-row"><button className="btn btn-secondary" type="button" disabled={!profile.target_role.trim() || !profile.job_description.trim() || busy} onClick={checkDescription}><Icon name="sparkles" size={16}/>{reviewingJD ? "Reviewing description…" : "Check job description"}</button><span className="field-hint">{profile.job_description.length.toLocaleString()} / 8,000</span></div>
            <p className="field-hint">AI checks relevance and detail—not job authenticity or your chances of selection. Checking sends this text to the configured AI provider.</p>
            {jdReview && <section className={`jd-review ${jdReview.assessment === "useful" ? "jd-useful" : "jd-advice"}`} aria-label="Job description review" aria-live="polite"><strong><Icon name={jdReview.assessment === "useful" ? "circle-check" : "circle-alert"} size={18}/>{{useful:"Useful for your interview",needs_detail:"A little more detail would help",role_mismatch:"This may be a different role",not_a_job_description:"This doesn't look like a job description"}[jdReview.assessment]}</strong><p>{jdReview.summary}</p>
              {!!jdReview.relevant_skills.length && <div><h3>Skills mentioned</h3><div className="skill-tags">{jdReview.relevant_skills.map(skill => <span key={skill}>{skill}</span>)}</div></div>}
              {!!jdReview.focus_areas.length && <div><h3>Suggested interview focus</h3><ul>{jdReview.focus_areas.map(area => <li key={area}>{area}</li>)}</ul></div>}
              {!!jdReview.missing_details.length && <div><h3>Worth adding</h3><ul>{jdReview.missing_details.map(detail => <li key={detail}>{detail}</li>)}</ul></div>}
              {!!jdReview.evidence.length && <details><summary>Why this feedback?</summary>{jdReview.evidence.map(quote => <blockquote key={quote}>{quote}</blockquote>)}</details>}
              {jdReview.assessment !== "useful" && <button type="button" className="btn" onClick={() => update("job_description", "")}>Continue without this description</button>}
            </section>}
          </div>
        </>}
        {step === 1 && <>
          <div className="form-section-heading"><span className="section-icon"><Icon name="file-text"/></span><h2>Your experience, in your words</h2></div>
          <p className="muted">Upload a resume to fill the form, or enter everything below yourself.</p>
          <div className="setup-upload">
            <label>Resume PDF <input type="file" accept=".pdf,application/pdf" onChange={event => { setFile(event.target.files[0] || null); setExtracted(null); setError(""); }} /></label>
            <p className="small muted">Text PDFs only · up to 5 MB · up to 10 pages</p>
            <p className="small muted">Analyze sends extracted resume text to the configured AI provider. The app does not keep your original PDF or raw text. Only details you review and save are stored.</p>
            <button type="button" className="btn btn-secondary" disabled={!file || busy} onClick={analyzeResume}>{busy ? "Analyzing resume…" : "Analyze resume"}</button>
          </div>
          {extracted && <section className="setup-extraction" aria-label="Extracted resume preview">
            <h3>Resume preview</h3><p className="small muted">AI can make mistakes. Using these details replaces the skills, projects, education and work fields below.</p>
            <Details profile={extracted} />
            <div className="setup-actions"><button type="button" className="btn btn-secondary" onClick={applyExtracted}>Use these details</button><button type="button" className="btn" onClick={() => setExtracted(null)}>Discard extraction</button></div>
          </section>}
          <label>Skills <textarea className="inp" required rows={3} value={skillsText} onChange={event => { setSkillsText(event.target.value); setSaved(false); }} placeholder="Python, SQL, React" /><span className="small muted">Separate skills with commas. Listed skills are self-reported, not verified proficiency.</span></label>
          <div><h3>Projects <span className="small muted">(optional, up to 8)</span></h3>
            {profile.projects.map((project, index) => <div className="setup-project" key={index}>
              <label>Project {index + 1} title<input className="inp" required maxLength={120} value={project.title} onChange={event => update("projects", profile.projects.map((item, i) => i === index ? { ...item, title: event.target.value } : item))} /></label>
              <label>Your contribution & technologies<textarea className="inp" rows={3} maxLength={2000} value={project.description} onChange={event => update("projects", profile.projects.map((item, i) => i === index ? { ...item, description: event.target.value } : item))} /></label>
              <button type="button" className="btn" onClick={() => update("projects", profile.projects.filter((_, i) => i !== index))}>Remove project {index + 1}</button>
            </div>)}
            <button type="button" className="btn btn-secondary" disabled={profile.projects.length >= 8} onClick={() => update("projects", [...profile.projects, { title: "", description: "" }])}>+ Add project</button>
          </div>
          <label>Education <span className="muted">(optional)</span><textarea className="inp" rows={2} maxLength={2000} value={profile.education} onChange={event => update("education", event.target.value)} /></label>
          <label>Work / internship experience <span className="muted">(optional)</span><textarea className="inp" rows={3} maxLength={3000} value={profile.work_summary} onChange={event => update("work_summary", event.target.value)} /></label>
        </>}
        {step === 2 && <>
          <h2>{saved ? "Your setup is saved" : "Ready to save your setup?"}</h2>
          <p className="muted">Review your details. You can return here to update them.</p>
          <dl className="setup-summary"><dt>Target role</dt><dd>{profile.target_role}</dd><dt>Experience</dt><dd>{profile.experience_level}</dd>{profile.job_description && <><dt>Job description</dt><dd>{profile.job_description}</dd></>}</dl>
          <Details profile={profile} />
          <p className="setup-notice">Save your profile, then meet the Technical Interviewer, Project Reviewer and Hiring Manager in the AI Panel. You choose when to start.</p>
          <p className="small muted">{isGuest ? "Guest setup is linked to this browser session. Signing in uses a separate account profile." : "Your confirmed profile is saved with your account."}</p>
          {saved && <p role="status" className="setup-success">Saved successfully. Your profile is ready for the AI Panel.</p>}
        </>}
        <div className="setup-actions">
          {step > 0 && <button type="button" className="btn btn-secondary" onClick={() => { setStep(step - 1); setError(""); setNotice(""); }}>Back</button>}
          {step < 2 ? <button className="btn btn-primary" type="submit">{step === 0 ? "Continue to resume & skills" : "Review setup"} →</button> : <>
            <button type="button" className="btn btn-primary" onClick={save} disabled={saved || busy}>{busy ? "Saving…" : saved ? "Setup saved" : "Confirm & save setup"}</button>
            {saved && <><button type="button" className="btn btn-secondary" onClick={onPanel}>Meet the AI Panel →</button><button type="button" className="btn" onClick={onPractice}>Practice core CS</button></>}
          </>}
        </div>
      </fieldset>
    </form>
    <aside className="profile-companion"><div className="companion-art"><img src="/Images/interview-desk.png" alt=""/></div><span className="eyebrow">YOUR INTERVIEW BLUEPRINT</span><h2>{profile.target_role || "Made around you."}</h2><p>{profile.target_role ? `${profile.experience_level} · Personalized practice` : "Your goals, skills and projects shape the conversation."}</p><div className="companion-lines"><div><Icon name="briefcase-business"/><span><strong>A clear direction</strong><small>{profile.target_role || "Start with your target role"}</small></span></div><div><Icon name="file-text"/><span><strong>Your own experience</strong><small>Resume upload or manual entry</small></span></div><div><Icon name="audio-lines"/><span><strong>Three perspectives</strong><small>Technical, project and hiring personas</small></span></div></div><p className="companion-note"><Icon name="shield-check" size={18}/>You review every detail before saving.</p></aside></div>
  </main>;
}

function Details({ profile }) {
  return <dl className="setup-summary">
    <dt>Skills</dt><dd>{profile.skills.length ? profile.skills.join(", ") : "None added"}</dd>
    <dt>Projects</dt><dd>{profile.projects.length ? profile.projects.map((project, index) => <div key={index}><strong>{project.title}</strong><p>{project.description}</p></div>) : "None added"}</dd>
    <dt>Education</dt><dd>{profile.education || "Not added"}</dd>
    <dt>Work experience</dt><dd>{profile.work_summary || "Not added"}</dd>
  </dl>;
}
