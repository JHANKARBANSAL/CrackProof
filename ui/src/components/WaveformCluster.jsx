const React = window.React;

export function WaveformCluster({ isRecording, side = "left" }) {
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
