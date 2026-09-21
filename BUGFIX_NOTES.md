# Existing-platform bug fixes

No resume, persona-panel, learning, or fine-tuning features were added.
The existing React/Flask stack is retained, with no new runtime library.

## Fixed

- Active interviews now persist in the database instead of process memory.
- Account and signed guest-cookie ownership are checked before accessing sessions.
- Guessed guest-history IDs no longer expose other visitors' answers.
- UUID interview IDs avoid collisions between sessions started in the same second.
- Repeated evaluations do not add duplicate answers. Revision checks prevent
  concurrent requests from overwriting each other's saved state and report.
- Delayed next-question requests cannot skip a question; five-question limits
  and completed-interview boundaries are enforced.
- Failed question/evaluation requests preserve a retryable interview state.
- Saved reports are read from the saved-report endpoint, without new AI calls.
- Finalizing a report preserves its question-answer turns and detailed history.
- Partial history uses actual calculated metrics rather than placeholder readiness.
- Guest mode clears account authentication before starting guest work.
- Guest dashboard/history use owner-checked records, avoiding duplicate and
  malformed local-storage summaries.
- Transcription quality failures are respected, even when text is nonempty.
- Exiting a recording cancels pending transcription and releases microphone tracks.
- Evaluation failures clear loading state and keep the transcript editable.
- Pending evaluation/next/report operations are protected against repeat clicks.
- Citation links retain their source data; missing citations no longer display a
  fabricated textbook source or an unrelated first reference.
- Playback blob URLs are released, and paused audio resumes from its position.
- Reports display limited-evidence notices, actual dimension counts, and the
  generated revision advice. Practice volume is not labelled as mastery.
- Mobile navigation and progress cards no longer overflow at the checked width.
- Embedding-service failures fall back to BM25; Computer Networks maps to CN.
- Web requests never rebuild missing embeddings synchronously.
- Invalid JSON/types, empty audio, unsupported audio extensions, and large uploads
  receive client errors. Internal error details are not returned to browsers.
- Configured PostgreSQL failures no longer silently switch to a different database.
- Interview/account deletion also removes persisted state and associated feedback.
- Docker builds the React bundle and excludes local secrets, recordings and databases.
- CI builds the frontend and runs the new regression checks.

## Verification

- 19 offline Python regression tests passed, including simultaneous evaluations.
- 5 JavaScript regression tests passed.
- Existing 3 RAG tests and all 7 dataset-validation gates passed.
- Frontend production bundle generated successfully.
- Browser checks: guest entry, dashboard, progress, saved report, subject history,
  and the saved transcript/evaluation view; mobile dashboard/progress at 390px.
- Real-provider smoke test passed: generated question, synthetic speech through
  Groq transcription, structured evaluation with 5 sources, final narrative,
  and saved-history retrieval. It used a temporary SQLite database.

## Practical limits

- Physical microphone capture and browser permission handling still need a human
  device check. Synthetic audio tested the server transcription pipeline.
- Docker build could not run because the local Docker daemon was stopped.
- Old guest records without ownership data are intentionally not exposed by IDs.
  Existing account reports remain readable, including legacy disk-backed turns.
- Playback audio is limited to the current page; transcripts and evaluations persist.
- These checks cover the repaired cases, not a guarantee of zero future bugs.
