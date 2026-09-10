# CrackProof UI

`index.html` is a working front-end prototype. Open it in a browser -
no build step, no server, no dependencies.

## What it is

All seven screens, clickable end to end:

    Login  ->  Dashboard  ->  Choose a Topic  ->  Recording
           ->  Transcript ->  Evaluation      ->  Report

It runs on sample data. Nothing is wired to the Python backend yet.

## Images

Every illustration and icon from `../Images/` is embedded in the file
as a base64 data URI. That is deliberate: the page must work when
opened directly from disk and when published, and neither case can
reliably load a sibling folder. The source files stay in `../Images/`
so they can be re-exported at any time.

Embedded: logo, landing_pg, mountain, progress, cube, java, database,
gear, network. About 320 KB in total.

Still drawn as inline SVG, because no image was supplied: the DSA
topic icon, the mic icon, and the checkmark icons. The progress chart
and the recording waveform are deliberately SVG and CSS rather than
images, because both have to move with real data.

## Rules this UI follows

These come from the backend's own guarantees and must survive any
redesign:

- A depth dimension that was never tested renders as "not covered
  yet" in neutral grey. It is never shown as a score, and never sits
  in the same visual family as NOT_DEMONSTRATED.
- `probe_strategy` and `probe_target` exist in the data and are never
  shown to the candidate.
- Overall readiness is labelled as being about this interview only.
- Computed numbers and AI-written prose are marked differently, since
  the backend guarantees the numbers are deterministic and the prose
  is not.
- Citations show a real source link and are never hidden behind a
  hover or a modal.

## Resolved: the 0-100 figure is gone

An earlier draft showed "72/100" on the report. The backend never
produced that number, so the UI would have been inventing it. It has
been removed. The report now shows only what the backend actually
returns: the `overall_readiness` label, and `average_correctness_score`
and `average_depth_score` as two separate bars out of 10.

If a single headline number is ever wanted, compute it in Python
alongside the other metrics. Never derive it in the UI.
