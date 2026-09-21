import test from "node:test";
import assert from "node:assert/strict";
import { initialInterviewState, interviewReducer } from "../ui/src/state/interviewReducer.js";
import { apiRequest, formatReadiness } from "../ui/src/api/client.js";

test("a failed evaluation keeps the answer editable and clears the spinner", () => {
  const review = { ...initialInterviewState, status: "REVIEW", transcript: "My answer" };
  const pending = interviewReducer(review, { type: "START_EVALUATION" });
  const failed = interviewReducer(pending, { type: "SET_ERROR", payload: "Please retry" });
  assert.equal(failed.loading, false);
  assert.equal(failed.status, "REVIEW");
  assert.equal(failed.transcript, "My answer");
});

test("moving to the next question clears the previous answer and audio", () => {
  const old = { ...initialInterviewState, transcript: "Previous", audioBlob: {}, evaluation: {}, loading: true };
  const next = interviewReducer(old, { type: "SET_NEXT_QUESTION", payload: { questionNumber: 2, questionText: "Next?" } });
  assert.equal(next.transcript, "");
  assert.equal(next.audioBlob, null);
  assert.equal(next.evaluation, null);
  assert.equal(next.loading, false);
});

test("saved reports are fetched with GET and HTTP failures are not successes", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async (path, options) => {
      assert.equal(path, "/api/interview/saved");
      assert.equal(options.method, "GET");
      return { ok: false, json: async () => ({ ok: true, message: "Not found" }) };
    };
    const result = await apiRequest("/api/interview/saved");
    assert.equal(result.ok, false);
    assert.equal(result.message, "Not found");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("network and non-JSON errors return a retryable result", async () => {
  const originalFetch = globalThis.fetch;
  try {
    globalThis.fetch = async () => { throw new Error("offline"); };
    assert.equal((await apiRequest("/api/history")).ok, false);
    globalThis.fetch = async () => ({ ok: false, json: async () => { throw new Error("HTML error page"); } });
    assert.equal((await apiRequest("/api/history")).ok, false);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("batch performance is not labelled as job readiness", () => {
  assert.equal(formatReadiness("STRONG").text, "Strong");
  assert.equal(formatReadiness("DEVELOPING").text, "Developing");
});
