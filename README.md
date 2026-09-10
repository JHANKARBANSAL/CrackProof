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
| Retrieval | 1884 chunks from 71 Wikipedia articles; local embeddings, BM25 fallback |
| Storage | Supabase Postgres, SQLite when running locally |
| Recordings | The candidate's own browser, never the server |
| Interface | Flask and plain JavaScript. No framework, no build step |

## Running it locally

```bash
pip install -r requirements.txt

python3 corpus_fetcher.py     # download the knowledge base, once
python3 knowledge_base.py     # split it into searchable chunks

python3 server.py             # http://localhost:5000
```

`.env` needs one key to run:

```
GROQ_API_KEY=...              # free at console.groq.com
DATABASE_URL=...              # optional; SQLite is used without it
```

There is also a terminal version, `python3 main.py`, which is where
the interview logic was first built and debugged.

## Things decided deliberately

**Recordings stay in the browser.** The evaluation runs on the
transcript, so the audio has no job after transcription. It is kept in
IndexedDB on the device that recorded it and the server deletes its
copy immediately. Nobody's voice sits on a server, and playback still
works where it was recorded.

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
