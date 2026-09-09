# Depth Evidence Rubric

<!--
source: SOLO Taxonomy, Biggs, J. B. & Collis, K. F. (1982),
        "Evaluating the Quality of Learning: The SOLO Taxonomy"
reference: https://www.structural-learning.com/post/what-is-solo-taxonomy
subject: RUBRIC
STATUS: NOT CURRENTLY USED.
      Wiring this into EVALUATION_PROMPT was measured and made the
      evaluation LESS stable, not more: evidence patterns went from
      1 unique in 4 runs to 3 unique in 4 runs on the same answer.
      Kept as documentation of where the four depth dimensions come
      from. Do not wire it in again without re-measuring.
-->

## Where this comes from

CrackProof's four depth dimensions are not invented. They line up with
the SOLO taxonomy, a published framework for judging the *quality* of
understanding rather than the quantity of facts recalled.

| SOLO level (Biggs & Collis, 1982) | What the response looks like | CrackProof |
|---|---|---|
| Prestructural | Misses the point entirely | `NOT_DEMONSTRATED` |
| Unistructural | Identifies a single isolated fact | `FUNDAMENTAL` |
| Multistructural | Several facts, not connected together | `PARTIALLY_DEMONSTRATED` |
| Relational | Connects the facts, explains why and how | `REASONING` |
| Extended abstract | Generalises beyond the given case | `APPLICATION`, `EDGE_CASE` |

---

## FUNDAMENTAL

Tests whether the candidate holds the core facts: definitions,
mechanisms, essential components. SOLO calls this unistructural, moving
to multistructural as more facts appear.

**DEMONSTRATED** — States the concept correctly and completely enough
for the question asked. The definition is accurate, not merely a
keyword. Verbs at this level: identify, name, define, recall.

**PARTIALLY_DEMONSTRATED** — Correct on part of the concept but
incomplete, or correct alongside a misconception about the same
concept. Multistructural: pieces are present but not assembled, or one
piece is wrong.

**NOT_DEMONSTRATED** — The stated definition is wrong, or the answer
misses the point of the question entirely. Prestructural.

---

## REASONING

Tests whether the candidate can explain *why* or *how* something works
rather than restating that it does. SOLO calls this relational: the
separate facts are connected into a coherent whole.

**DEMONSTRATED** — Gives the underlying mechanism or a causal chain
that actually explains the behaviour. Verbs: explain, compare, analyse.
Naming a cause without connecting it to the effect is not enough.

**PARTIALLY_DEMONSTRATED** — Gestures at a reason but the chain is
incomplete, circular, or partly wrong. Often reads as several correct
facts placed side by side without the link between them.

**NOT_DEMONSTRATED** — Restates the fact rather than explaining it, or
offers no reason at all when the question asked for one.

---

## APPLICATION

Tests whether the candidate can take the concept to a concrete case:
code, a scenario, a debugging situation, a design decision. SOLO calls
this extended abstract, since it means using the idea beyond the form
in which it was learned.

**DEMONSTRATED** — Applies the concept correctly to a specific case,
with the details right. A worked example, correct code behaviour, or a
justified design choice.

**PARTIALLY_DEMONSTRATED** — Attempts the application and gets the
shape right but the details wrong, or gives an example so generic that
it does not show the concept being used.

**NOT_DEMONSTRATED** — Cannot move from the definition to a case, or
the applied example is incorrect.

---

## EDGE_CASE

Tests whether the candidate can reason about limits: boundary
conditions, failure modes, exceptions, trade-offs. Also extended
abstract, since it means generalising to situations not given.

**DEMONSTRATED** — Names a real limitation, failure case, or trade-off
and explains when it matters.

**PARTIALLY_DEMONSTRATED** — Knows a limit exists but cannot say when
it applies or why, or names a trade-off without either side of it.

**NOT_DEMONSTRATED** — Treats the concept as universally applicable
when the question asked about its limits.

---

## Rules that override everything above

1. **Only judge dimensions the QUESTION actually tests.** Decide which
   dimensions apply by reading the question, before reading the answer.
   A dimension the question does not test must not appear at all.

2. **Absence is not failure.** A dimension that does not appear means
   it was never asked about. It does not mean the candidate failed it.

3. **One judgement per dimension per question.** If the same dimension
   is both demonstrated and contradicted within one answer, that is a
   single `PARTIALLY_DEMONSTRATED`, not two separate entries.

4. **A weak or empty answer does not fail every dimension.** It fails
   only the dimensions the question actually tested.

5. **Judge technical evidence only.** Grammar, accent, fluency,
   hesitation and Hindi-English code switching are never evidence.
