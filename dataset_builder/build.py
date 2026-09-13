"""
Master Dataset Assembler & Question-Level Splitter for CrackProof.

Combines the 48-question pools across all 6 core CS subjects:
- Java (8)
- OOP (8)
- DBMS (8)
- OS (8)
- CN (8)
- DSA (8)

Total: 48 questions x 3 samples = 144 gold-standard samples.
Outputs:
- dataset/train.jsonl (108 samples, 36 questions)
- dataset/val.jsonl   (18 samples, 6 questions)
- dataset/test.jsonl  (18 samples, 6 questions)
"""

import json
import os
import sys
import re

sys.path.insert(0, os.getcwd())

from evaluator import AnswerEvaluation
from dataset_builder.java_pool import JAVA_POOL
from dataset_builder.oop_pool import OOP_POOL
from dataset_builder.dbms_pool import DBMS_POOL
from dataset_builder.os_pool import OS_POOL
from dataset_builder.cn_pool import CN_POOL
from dataset_builder.dsa_pool import DSA_POOL

RAW_DATASET_POOL = (
    JAVA_POOL
    + OOP_POOL
    + DBMS_POOL
    + OS_POOL
    + CN_POOL
    + DSA_POOL
)

SYSTEM_PROMPT = """You are a strict technical interviewer.
Your task is to evaluate the candidate's TECHNICAL UNDERSTANDING.
Evaluate based on:
1. Technical correctness (0-10)
2. Conceptual depth (0-10)
3. SOLO Taxonomy Depth Dimensions: FUNDAMENTAL, REASONING, APPLICATION, EDGE_CASE
4. Concepts correctly covered, missing core concepts & technical misconceptions
5. Grounding: Cite reference passages [1], [2] when provided.
Do NOT penalize grammar, English fluency, accent, or Hindi-English code-switching.
Always output valid JSON conforming to the CrackProof AnswerEvaluation schema."""


def build_chatml_row(q_item, sample):
    """Formats sample into ChatML messages."""
    user_text = (
        f"INTERVIEW QUESTION:\n{q_item['question']}\n\n"
        f"CANDIDATE ANSWER:\n{sample['answer']}\n\n"
        f"REFERENCE MATERIAL:\n{q_item['reference']}"
    )
    assistant_text = json.dumps(sample["evaluation"], indent=2)

    return {
        "question_id": q_item["question_id"],
        "subject": q_item["subject"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_text}
        ]
    }


def main():
    print("===============================================================")
    print("CRACKPROOF 48-QUESTION GOLD-STANDARD DATASET ASSEMBLER")
    print("===============================================================\n")

    # 1. Verification of Questions & Samples
    print(f"Total Questions in Pool: {len(RAW_DATASET_POOL)}")
    assert len(RAW_DATASET_POOL) == 48, f"Expected 48 questions, got {len(RAW_DATASET_POOL)}"

    total_samples = 0
    validated_samples = 0
    citation_checks = 0
    all_rows = []

    for q_item in RAW_DATASET_POOL:
        assert len(q_item["samples"]) == 3, f"Question {q_item['question_id']} does not have exactly 3 samples!"
        verdicts = [s["evaluation"]["verdict"] for s in q_item["samples"]]
        assert verdicts == ["CORRECT", "PARTIALLY_CORRECT", "INCORRECT"], (
            f"Question {q_item['question_id']} does not have [CORRECT, PARTIALLY_CORRECT, INCORRECT] order! Got {verdicts}"
        )

        for s in q_item["samples"]:
            total_samples += 1
            # A. Pydantic validation
            try:
                AnswerEvaluation.model_validate(s["evaluation"])
                validated_samples += 1
            except Exception as e:
                print(f"[SCHEMA ERROR] Question {q_item['question_id']}: {e}")
                sys.exit(1)

            # B. Citation source_number integrity
            for cit in s["evaluation"].get("citations", []):
                src_num = cit["source_number"]
                assert f"[{src_num}]" in q_item["reference"], (
                    f"[CITATION ERROR] Question {q_item['question_id']}: Citation source [{src_num}] missing from reference!"
                )
                citation_checks += 1

            row = build_chatml_row(q_item, s)
            all_rows.append(row)

    print(f"[PASS] 100% Pydantic Schema Validation ({validated_samples}/{total_samples} samples passed).")
    print(f"[PASS] 100% Citation Grounding Verification ({citation_checks} citations verified against [N] tags).\n")

    # 2. Stratified Question Partitioning
    # 6 subjects x 8 questions:
    # Q1-Q6 -> Train (36 questions = 108 samples)
    # Q7    -> Val   (6 questions = 18 samples)
    # Q8    -> Test  (6 questions = 18 samples)
    by_question = {}
    for r in all_rows:
        qid = r["question_id"]
        if qid not in by_question:
            by_question[qid] = []
        by_question[qid].append(r)

    subjects = ["JAVA", "OOP", "DBMS", "OS", "CN", "DSA"]
    train_qids = []
    val_qids = []
    test_qids = []

    for sub in subjects:
        for i in range(1, 7):
            train_qids.append(f"{sub}_{i:02d}")
        val_qids.append(f"{sub}_07")
        test_qids.append(f"{sub}_08")

    print(f"Stratified Split Allocation:")
    print(f"  Train Question IDs ({len(train_qids)}): {train_qids}")
    print(f"  Val Question IDs   ({len(val_qids)}): {val_qids}")
    print(f"  Test Question IDs  ({len(test_qids)}): {test_qids}\n")

    train_rows = [r for qid in train_qids for r in by_question[qid]]
    val_rows   = [r for qid in val_qids for r in by_question[qid]]
    test_rows  = [r for qid in test_qids for r in by_question[qid]]

    # 3. Assert Zero Leakage
    train_set = set(train_qids)
    val_set   = set(val_qids)
    test_set  = set(test_qids)

    assert len(train_set.intersection(val_set)) == 0, "DATA LEAKAGE: Train & Val overlap!"
    assert len(train_set.intersection(test_set)) == 0, "DATA LEAKAGE: Train & Test overlap!"
    assert len(val_set.intersection(test_set)) == 0, "DATA LEAKAGE: Val & Test overlap!"

    # Normalized text leakage check
    def extract_q(content):
        match = re.search(r"INTERVIEW QUESTION:\s*(.*?)\n\nCANDIDATE ANSWER:", content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip().lower() if match else content.strip().lower()

    train_qtexts = {extract_q(r["messages"][1]["content"]) for r in train_rows}
    val_qtexts   = {extract_q(r["messages"][1]["content"]) for r in val_rows}
    test_qtexts  = {extract_q(r["messages"][1]["content"]) for r in test_rows}

    assert len(train_qtexts.intersection(val_qtexts)) == 0, "TEXT LEAKAGE: Train & Val overlap!"
    assert len(train_qtexts.intersection(test_qtexts)) == 0, "TEXT LEAKAGE: Train & Test overlap!"
    assert len(val_qtexts.intersection(test_qtexts)) == 0, "TEXT LEAKAGE: Val & Test overlap!"
    print("[PASS] Question-Level & Text-Level Leakage is strictly 0.0% across all splits.\n")

    # 4. Verify Subject & Verdict Balances
    def analyze_split(name, rows):
        sub_dist = {}
        verdict_dist = {}
        for r in rows:
            sub = r["subject"]
            sub_dist[sub] = sub_dist.get(sub, 0) + 1
            verdict = json.loads(r["messages"][-1]["content"])["verdict"]
            verdict_dist[verdict] = verdict_dist.get(verdict, 0) + 1
        print(f"Split {name.upper()} ({len(rows)} samples):")
        print(f"  Subjects : {sub_dist}")
        print(f"  Verdicts : {verdict_dist}")
        # Assert each subject has equal count
        expected_sub_count = len(rows) // 6
        assert all(c == expected_sub_count for c in sub_dist.values()), f"Imbalanced subjects in {name}!"
        # Assert each verdict has equal count (1:1:1 balance)
        expected_verdict_count = len(rows) // 3
        assert all(c == expected_verdict_count for c in verdict_dist.values()), f"Imbalanced verdicts in {name}!"

    analyze_split("Train", train_rows)
    analyze_split("Val", val_rows)
    analyze_split("Test", test_rows)

    # 5. Write to dataset directory
    os.makedirs("dataset", exist_ok=True)
    with open("dataset/train.jsonl", "w", encoding="utf-8") as f:
        for r in train_rows:
            f.write(json.dumps(r) + "\n")

    with open("dataset/val.jsonl", "w", encoding="utf-8") as f:
        for r in val_rows:
            f.write(json.dumps(r) + "\n")

    with open("dataset/test.jsonl", "w", encoding="utf-8") as f:
        for r in test_rows:
            f.write(json.dumps(r) + "\n")

    print("\n[SUCCESS] Successfully written gold-standard dataset files:")
    print(f"  - dataset/train.jsonl : {len(train_rows)} samples across {len(train_qids)} questions")
    print(f"  - dataset/val.jsonl   : {len(val_rows)} samples across {len(val_qids)} questions")
    print(f"  - dataset/test.jsonl  : {len(test_rows)} samples across {len(test_qids)} questions")
    print(f"Total Dataset Samples: {len(train_rows) + len(val_rows) + len(test_rows)} (100% Schema Validated & Grounded)")


if __name__ == "__main__":
    main()
