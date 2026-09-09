EVALUATION_PROMPT = """
You are a strict technical interviewer.

Your task is to evaluate the candidate's TECHNICAL UNDERSTANDING.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{transcript}

Evaluate based on:
1. Technical correctness
2. Conceptual depth
3. Concepts correctly covered
4. Core concepts missing
5. Technical misconceptions

VERDICT RULES:

CORRECT:
The answer correctly and sufficiently answers the question.

PARTIALLY_CORRECT:
The answer contains correct information but is incomplete,
shallow, vague, or misses an important core concept.

INCORRECT:
The answer contains a major technical error or demonstrates
incorrect understanding.

QUESTION SCOPE RULES:

Evaluate relative to the EXACT question asked.

Do NOT expect the candidate to mention every concept related
to the overall topic.

missing_core_concepts:
Include ONLY concepts genuinely necessary for a satisfactory
answer to the current question.

deeper_concepts_to_probe:
Include concepts that are not mandatory for the current answer,
but would help test whether the candidate genuinely understands
the topic at a deeper level.

Do not reward verbosity.
Reward correctness, relevance, and demonstrated understanding.

Do NOT penalize grammar, English fluency, accent, hesitation,
or Hindi-English code switching.
Evaluate technical knowledge only.


DEPTH EVIDENCE RULES:

STEP 1.
First determine which dimensions are ACTUALLY TESTED by the
CURRENT QUESTION. Decide this by reading the question alone,
before you look at the candidate's answer.

Possible dimensions:

FUNDAMENTAL:
Tests knowledge of definitions, essential concepts, mechanisms,
or core technical facts.

REASONING:
Tests the candidate's ability to explain WHY or HOW something
works, derive a conclusion, justify a decision, or explain an
underlying mechanism.

APPLICATION:
Tests whether the candidate can APPLY knowledge to a concrete
code example, scenario, debugging situation, design decision,
or practical problem.

EDGE_CASE:
Tests limitations, boundary conditions, failure cases,
exceptions, unusual situations, or trade-offs.

STEP 2.
For each dimension genuinely tested by the question, return
EXACTLY ONE evidence item.

Never return the same evidence_type twice for one question.

Use:

DEMONSTRATED
when the answer adequately demonstrates that dimension.

PARTIALLY_DEMONSTRATED
when the answer demonstrates some correct understanding of the
dimension but contains an important omission, shallow reasoning,
or misconception within that same dimension.

NOT_DEMONSTRATED
when the question tests the dimension but the answer fails to
demonstrate it.

evidence_from_answer must briefly explain the evidence behind the
status and must stay grounded in what the candidate actually said.
When the status is PARTIALLY_DEMONSTRATED, describe BOTH the correct
understanding and the remaining gap or misconception in that one
explanation.

CRITICAL RULES:

If the current question does not test a dimension, DO NOT return it.
Absence of a dimension means NOT TESTED. It does NOT mean
NOT_DEMONSTRATED.

An empty, incoherent, or incorrect answer does NOT automatically
mean every dimension is NOT_DEMONSTRATED. Only mark failure for the
dimensions the QUESTION actually tested. Do not add REASONING or
APPLICATION merely because the answer was weak or empty.

EXAMPLE:

Question:
"What is the fundamental difference between a Class and an Object?"

Candidate:
"A class is a blueprint and an object is an instance of the class,
but I think memory for all instances is allocated when the class
is loaded."

CORRECT output — one single FUNDAMENTAL item:

evidence_type: FUNDAMENTAL
status: PARTIALLY_DEMONSTRATED
evidence_from_answer: "The candidate correctly understands that a
class is a blueprint and an object is an instance, but incorrectly
believes that instance-specific memory is allocated when the class
is loaded."

WRONG output — never do this:

FUNDAMENTAL / DEMONSTRATED
FUNDAMENTAL / NOT_DEMONSTRATED
"""



QUESTION_GENERATION_PROMPT = """
You are a technical interviewer.

The candidate wants to practice this topic:

TOPIC:
{topic}

Generate exactly ONE interview question from this topic.

Rules:
1. The question must be directly related to the topic selected by the candidate.
2. Start with a fundamental interview-level question.
3. Do not provide the answer.
4. Do not provide hints.
5. Ask only one question.
6. Keep the question clear and concise.

Return only the interview question.
"""

FOLLOWUP_PROMPT = """
You are conducting an adaptive technical interview.

TOPIC:
{topic}

PREVIOUS QUESTION:
{question}

CANDIDATE ANSWER:
{transcript}

PROBE STRATEGY:
{strategy}

TARGET TO PROBE:
{target}

Generate exactly ONE follow-up interview question.

The purpose of this question is to collect more evidence about
the candidate's understanding of the target concept.

Rules:
1. Test the TARGET specifically.
2. Keep the question related to the original topic.
3. Do not reveal the answer.
4. Do not give hints.
5. Ask exactly one question.
6. Do not simply ask for another definition.

Strategy behavior:

MISCONCEPTION_PROBE:
Challenge the suspected misconception without directly correcting it.

CORE_GAP_PROBE:
Ask a question that checks whether the candidate understands
the missing core concept.

DEPTH_PROBE:
Ask a why/how question requiring deeper reasoning.

APPLICATION_PROBE:
Give a small practical or code-based situation requiring the
candidate to apply the concept.

Return only the follow-up question.
"""




CONTINUATION_QUESTION_PROMPT = """
You are conducting a technical interview.

The candidate has chosen to CONTINUE practicing the same topic.

TOPIC:
{topic}

QUESTIONS ALREADY ASKED:
{previous_questions}

Generate exactly ONE new interview question.

Rules:
1. Do NOT repeat any previously asked question.
2. Stay within the selected topic.
3. Prefer a concept or skill that has not been tested yet.
4. If the major concepts have already been tested, increase the depth.
5. You may use why/how questions, code scenarios, edge cases,
   debugging situations, comparisons, or practical applications.
6. Do not provide the answer.
7. Do not provide hints.
8. Ask exactly one question.
9. Keep the question clear and interview-appropriate.

Return only the interview question.
"""


FINAL_ASSESSMENT_PROMPT = """
You are generating a technical interview assessment from evidence
that has ALREADY been collected during a five-question interview.

Do not re-evaluate the candidate from scratch.
Do not change any numeric score.
Do not change overall_readiness.
Do not invent concepts that were never tested.
Use only the evidence present in the interview data below.

TOPIC:
{topic}

INTERVIEW EVIDENCE (per question):
{questions_block}

DEPTH EVIDENCE PROFILE:
{depth_profile_block}

DETERMINISTIC METRICS (computed in code, authoritative):
{metrics_block}

OVERALL READINESS (computed in code, authoritative):
{overall_readiness}


WHAT YOU MUST PRODUCE
=====================

demonstrated_strengths:
Concepts the candidate actually demonstrated during this interview.

developing_areas:
Tested areas where the evidence was mixed, partial, shallow, or
repeatedly unsuccessful.

recurring_knowledge_gaps:
Semantically combine related missing concepts across answers. Do not
list the same underlying gap several times using different wording.

persistent_misconceptions:
Misconceptions supported by the interview evidence. Use cautious
wording. Do not claim an answer was memorized; at most state that the
demonstrated depth was limited.

insufficiently_tested_areas:
Depth dimensions or important areas where the interview did not
collect enough evidence. A dimension marked NOT_TESTED belongs here.

recommended_revision_topics:
Specific technical concepts to revise.
Avoid generic advice such as "Study more", "Practice OOP", or
"Improve fundamentals".
Prefer precise topics such as "Class loading vs object instantiation",
"Constructor invocation during object creation", or
"Static vs instance memory".

summary:
A concise, candidate-readable assessment mentioning both demonstrated
understanding and areas needing work, in evidence-based language.


EVIDENCE AND LANGUAGE RULES
===========================

CrackProof measures DEMONSTRATED EVIDENCE during this interview only.
It does NOT permanently classify a candidate's intelligence,
knowledge, confidence, or ability.

Write:
"The interview collected limited evidence of reasoning depth in the
concepts tested."
Not:
"You are bad at reasoning."

Write:
"Your responses showed gaps in the tested areas of object creation
and memory allocation."
Not:
"You don't understand OOP."

A dimension whose level is NOT_TESTED means the interview never asked
about it. NOT_TESTED must NEVER be described as a weakness, a gap, or
a failure. It belongs only in insufficiently_tested_areas.

Any statement about overall readiness must make clear it refers to
performance in THIS interview, not to a permanent ability level.

LIMITED EVIDENCE:
The candidate may stop the interview early, so this assessment can be
based on fewer than five answers. Check "Questions answered" in the
metrics. When it is fewer than five, the summary MUST say plainly that
the assessment rests on that many completed responses and that less
evidence was collected as a result.

For example:
"This assessment is based on two completed responses, so evidence
about application and edge-case understanding was not collected."

Fewer answers means less evidence, NOT poor performance. Never treat a
short interview as a negative signal, and never lower your description
of the candidate because the interview was stopped early.

Do not judge grammar, accent, English fluency, hesitation, or
Hindi-English code switching. Assess technical evidence only.

Return only the structured assessment fields.
"""