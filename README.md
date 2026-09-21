# CrackProof

An adaptive technical interview that answers a question most practice
tools cannot: **where does that judgement come from?**

You pick a subject and answer out loud. It transcribes what you said,
finds the specific gap in your understanding, and asks the next
question about *that gap*. At the end it tells you what you showed,
what was missing, and links the exact source for every claim it makes.

## What makes it different

Most tools tell you that you were wrong. This one shows you where it
says so.

```
Missing Core Concepts:
- Normalization prevents insertion, update and deletion anomalies
    source: Relational database — section "Normalization"
    https://en.wikipedia.org/wiki/Relational_database#Normalization
```

That link is real and opens at that section. It is not the model
recalling a source; the model only picks a number from a list of
passages that were actually retrieved, and the URL is filled in from
that list. It cannot invent one.

## How a question follows the last answer

```
Q1  "What is the difference between == and .equals()?"
     → answer is good, but never mentions null handling
     → gap found: "Null handling in .equals (NPE)"

Q2  "If String a = null, what happens when you call a.equals(b)?"
     → the gap, asked directly
```

The interview is not a fixed list. Each question is written from the
gap the previous answer left.

## Depth, not just right or wrong

Every answer is judged on four dimensions, and only on the ones the
question actually tested:

| | |
|---|---|
| `FUNDAMENTAL` | Does the definition hold up |
| `REASONING` | Can they explain why, not just what |
| `APPLICATION` | Can they use it on a real case |
| `EDGE_CASE` | Do they know where it breaks |

A dimension the question never asked about is reported as **not
covered**, never as a failure. Absence of evidence is not evidence of
absence, and the interface is careful never to blur the two.

## Numbers are computed, prose is written

Scores, coverage and the readiness label are calculated in Python and
cannot be changed by the model. Strengths, gaps and the summary are
written by the model and contain no numbers. The report marks which is
which, because the two carry different weight.

## Built with

| | |
|---|---|
| Evaluation and questions | Groq, `gpt-oss-120b` |
| Speech to text | Groq Whisper `large-v3`, local Whisper as fallback |
| Retrieval | 1904 reference chunks; local embeddings, BM25 fallback |
| Storage | Supabase Postgres, SQLite when running locally |
| Recordings | Temporary upload for transcription; playback in the current browser page |
| Interface | React 18, custom CSS, esbuild; Flask API |

## Running it locally

```bash
pip install -r requirements.txt
npm ci
npm run build                # rebuild after editing ui/src

python3 server.py             # http://localhost:5000
```

`.env` needs one key to run:

```
GROQ_API_KEY=...              # free at console.groq.com
DATABASE_URL=...              # optional; SQLite is used without it
SECRET_KEY=...                # required stable secret for deployed workers
```

There is also a terminal version, `python3 main.py`, which is where
the interview logic was first built and debugged.

Active web interview state is stored in `interview_sessions`, alongside
account history. Guest history is scoped to a signed browser cookie.
Configured PostgreSQL outages return an error rather than silently switching
to a different database. Old account reports remain readable; legacy guest
records without ownership data are not exposed by guessed IDs.

Local regression checks (AI responses are mocked in the web tests):

```bash
python3 -m unittest test_web -v
python3 test_rag_pipeline.py
node --test tests/ui-regression.mjs
npm run build
```

## Things decided deliberately

**Recordings stay in the browser.** The evaluation runs on the
transcript. The server deletes its temporary audio file after transcription.
The active React interface retains a playback blob for the current page;
reloading or leaving the question does not preserve that audio.

**The transcript is shown before it is graded, and can be edited.** If
Whisper mishears a word, the candidate fixes it at that moment rather
than being marked down for it.

**A transcript that cannot be trusted is not graded at all.** Wrong
language, mostly non-Latin characters, low confidence or near silence
sends the same question back to be recorded again. It does not count
as an attempt.

**Thresholds here are prototype heuristics, not validated assessment
scales.** They are labelled that way in the code, and `STRONG` means
"in this interview", not "ready to be hired".

## Known limits

- The knowledge base is 71 Wikipedia articles. Wikipedia explains what
  a concept is, not what a good interview answer contains.
- Audio does not follow you to another device. Transcripts and reports
  do.
- Evaluation quality has been measured, not assumed: the same answer
  can still receive different verdicts across runs, which is why
  grounding was added and why the feedback control exists.

## Resume & Role Setup

Open **My Profile** or **Build my profile** from the dashboard. The flow is
target role and experience → optional PDF resume → editable skills/projects →
review and save. Manual entry works without an AI provider. Saved profiles are
isolated by account or guest session; signing in does not migrate a guest profile.

PDF extraction uses `pypdf` and the existing configured LLM with a Pydantic schema.
The upload accepts text PDFs up to 5 MB and 10 pages; encrypted, malformed,
image-only and oversized PDFs return a useful error. OCR is not implemented.
Analysis sends extracted text to the configured AI provider. The app stores only
the candidate-confirmed profile, not the PDF or raw extracted text. The AI provider's
own retention rules still apply. Listed skills are self-reported, not proficiency scores.

`GET/POST /api/profile` reads/saves the owner-scoped profile. `POST /api/resume/parse`
accepts a multipart `resume` file and returns a preview without saving it.
The additive `candidate_profiles` table is created at startup. Account deletion
also removes the account's profile. This setup customizes the AI Panel described below;
the existing core-CS knowledge interviews remain a separate practice mode.

Run resume/profile checks with `python -m unittest test_candidate_profile -v`.

The target role field includes 18 searchable suggestions and accepts custom roles.
The optional **Check job description** action checks whether pasted text can guide
an interview for the selected role. It identifies relevant requirements, missing
detail, unrelated text, or a different role. Reviews clear when the role or text
changes. Requirements are never automatically added to the candidate's skills.
This is AI guidance, not a job-authenticity check, ATS score, or hiring prediction.
`POST /api/profile/job-description` returns the review without saving the profile.

The interface uses the existing React/esbuild setup, a shared `ui/design.css`
visual layer, local Lucide icons, and two generated illustrations. See
[design review and verification](design-review/README.md).

## AI persona panel

Open **AI Panel** after saving a profile. Three interviewer roles each ask two
questions: Technical Interviewer, Project Reviewer and Hiring Manager. The existing
LLM generates profile-aware questions, uses prior answers for follow-ups, and provides
coaching feedback. This is one model with explicit persona prompts and a small state
machine, not separately trained models or autonomous multi-agent orchestration.

Candidates can type or record English answers, review transcripts, and submit.
Browser speech synthesis can read questions aloud. Audio is turn-by-turn, not a
continuous streaming call. Recordings stop after two minutes; server-side audio is
temporary. The app saves submitted answers before requesting the next question,
so AI failures can be retried without losing answers. The latest 20 sessions can be
reopened from the panel page; panel sessions have their own history and are not
included in knowledge-assessment progress scores.

The profile snapshot, current question, transcript and report live in the
owner-scoped `panel_sessions` table, with optimistic concurrency checks. Account
deletion removes account panel sessions. The `/api/panels` routes support starting,
resuming, answering, advancing and finishing early. Feedback is based only on
submitted answers and is labelled AI coaching, not a hiring decision.

Run panel tests with `python -m unittest test_panel -v`.
See [AGORA_SETUP.md](AGORA_SETUP.md) for the proposed Agora streaming integration;
Agora credentials and the live RTC integration are still outstanding.
