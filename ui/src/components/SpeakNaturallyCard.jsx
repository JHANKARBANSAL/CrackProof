const React = window.React;

export function SpeakNaturallyCard({ isRecording }) {
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
