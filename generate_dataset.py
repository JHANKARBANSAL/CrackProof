"""
CrackProof Gold-Standard Dataset Generator & Question-Level Splitter.

Generates 48 Canonical Interview Questions x 3 Balanced Samples = 144 Samples across:
- Java (8 questions = 24 samples)
- OOP (8 questions = 24 samples)
- DBMS (8 questions = 24 samples)
- OS (8 questions = 24 samples)
- CN (8 questions = 24 samples)
- DSA (8 questions = 24 samples)

Each sample conforms 100% to AnswerEvaluation Pydantic schema in evaluator.py:
- verdict: CORRECT | PARTIALLY_CORRECT | INCORRECT (Exact 1:1:1 balance)
- correctness_score: 0-10
- depth_score: 0-10
- correct_points: list[str]
- missing_core_concepts: list[str]
- deeper_concepts_to_probe: list[str]
- misconceptions: list[str]
- evidence: list[DepthEvidence]
- citations: list[Citation] (verified against reference [1], [2])
- reasoning: str

Splits strictly at the QUESTION level with 0.0% data leakage:
- Train : 36 unique questions (108 samples) - 6 per subject
- Val   :  6 unique questions ( 18 samples) - 1 per subject
- Test  :  6 unique questions ( 18 samples) - 1 per subject (HELD OUT)
"""

from dataset_builder.build import main, RAW_DATASET_POOL, build_chatml_row, SYSTEM_PROMPT

if __name__ == "__main__":
    main()
