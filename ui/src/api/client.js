/**
 * API Client & Formatting Helpers
 */

export async function apiRequest(path, data = null) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 180000);
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

export function formatReadiness(val) {
  if (val === "STRONG" || val === "READY") return { text: "Strong", pill: "pill-g" };
  if (val === "DEVELOPING" || val === "ALMOST_READY") return { text: "Developing", pill: "pill-a" };
  if (val === "NEEDS_IMPROVEMENT") return { text: "Needs Practice", pill: "pill-n" };
  return { text: "In Progress", pill: "pill-b" };
}

export function niceDimensionName(dim) {
  const map = {
    FUNDAMENTAL: "Core Concepts",
    REASONING: "Technical Reasoning",
    APPLICATION: "Real-World Application",
    EDGE_CASE: "Edge Cases & Depth"
  };
  return map[dim] || dim;
}
