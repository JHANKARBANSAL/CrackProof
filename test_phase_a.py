#!/usr/bin/env python3
"""
CrackProof Phase A Readiness Test Suite.

Run this script to verify that Phase A (Dataset & Pre-Fine-Tuning Contracts)
is 100% ready before proceeding to Phase B (Fine-Tuning / Experimentation).

Usage:
    python3 test_phase_a.py
"""

import json
import os
import re
import sys

# Ensure current working directory is in sys.path
sys.path.insert(0, os.getcwd())

try:
    from evaluator import AnswerEvaluation
except ImportError as e:
    print(f"❌ Error importing evaluator.py: {e}")
    sys.exit(1)


GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def check(title, condition, details=""):
    if condition:
        print(f"  {GREEN}✔ PASS{RESET} : {title}")
        if details:
            print(f"         {details}")
        return True
    else:
        print(f"  {RED}✘ FAIL{RESET} : {title}")
        if details:
            print(f"         {RED}{details}{RESET}")
        return False


def main():
    print(f"\n{BOLD}======================================================{RESET}")
    print(f"{BOLD}       CRACKPROOF PHASE A READINESS TEST SUITE       {RESET}")
    print(f"{BOLD}======================================================{RESET}\n")

    splits = ["train", "val", "test"]
    files_exist = True
    for s in splits:
        path = f"dataset/{s}.jsonl"
        if not os.path.exists(path):
            files_exist = False
            print(f"  {RED}✘ FAIL{RESET} : File {path} does not exist!")

    if not files_exist:
        print("\nRun: python3 generate_dataset.py first.\n")
        sys.exit(1)

    # 1. Load data
    data = {}
    for s in splits:
        with open(f"dataset/{s}.jsonl", "r", encoding="utf-8") as f:
            data[s] = [json.loads(line) for line in f]

    all_samples = [item for s in splits for item in data[s]]
    passed_all = True

    # -------------------------------------------------------------
    # GATE 1: Sample Counts & Ratios
    # -------------------------------------------------------------
    print(f"{BOLD}[Gate 1] Dataset Scale & Split Sizing{RESET}")
    c1 = check(
        "Total sample count is exactly 144",
        len(all_samples) == 144,
        f"Found {len(all_samples)} samples (Expected: 144)"
    )
    c2 = check(
        "Train split has 108 samples (75%)",
        len(data["train"]) == 108,
        f"Found {len(data['train'])} samples"
    )
    c3 = check(
        "Validation split has 18 samples (12.5%)",
        len(data["val"]) == 18,
        f"Found {len(data['val'])} samples"
    )
    c4 = check(
        "Test split has 18 samples (12.5%)",
        len(data["test"]) == 18,
        f"Found {len(data['test'])} samples"
    )
    passed_all = passed_all and c1 and c2 and c3 and c4

    # -------------------------------------------------------------
    # GATE 2: Question Allocation & Balance
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 2] Question Allocation & Cardinality{RESET}")
    qids = {s: {r["question_id"] for r in data[s]} for s in splits}
    all_qids = set.union(*qids.values())

    c5 = check(
        "Total unique questions is exactly 48",
        len(all_qids) == 48,
        f"Found {len(all_qids)} questions across all splits"
    )
    c6 = check(
        "Train has 36 unique questions, Val has 6, Test has 6",
        len(qids["train"]) == 36 and len(qids["val"]) == 6 and len(qids["test"]) == 6,
        f"Train: {len(qids['train'])}, Val: {len(qids['val'])}, Test: {len(qids['test'])}"
    )

    # Check exactly 3 samples per question
    by_q = {}
    for r in all_samples:
        qid = r["question_id"]
        by_q[qid] = by_q.get(qid, 0) + 1
    exact_3 = all(count == 3 for count in by_q.values())
    c7 = check(
        "Every question has exactly 3 samples (Correct, Partial, Incorrect)",
        exact_3,
        f"Violations: {[q for q, c in by_q.items() if c != 3]}"
    )
    passed_all = passed_all and c5 and c6 and c7

    # -------------------------------------------------------------
    # GATE 3: Subject & Verdict Balance (No Blindness)
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 3] Subject Coverage & Verdict Balance{RESET}")
    subjects = ["Java", "OOP", "DBMS", "OS", "CN", "DSA"]
    
    subject_ok = True
    for s in splits:
        subs = {r["subject"] for r in data[s]}
        if subs != set(subjects):
            subject_ok = False
            break

    c8 = check(
        "All 6 core subjects are represented in EVERY split",
        subject_ok,
        f"Subjects: {subjects}"
    )

    verdict_ok = True
    for s in splits:
        v_counts = {}
        for r in data[s]:
            v = json.loads(r["messages"][-1]["content"])["verdict"]
            v_counts[v] = v_counts.get(v, 0) + 1
        expected = len(data[s]) // 3
        if not all(cnt == expected for cnt in v_counts.values()):
            verdict_ok = False
            break

    c9 = check(
        "Exact 1:1:1 Verdict Balance across Train (36/36/36), Val (6/6/6), Test (6/6/6)",
        verdict_ok,
        "Every split contains equal proportions of CORRECT, PARTIALLY_CORRECT, INCORRECT"
    )
    passed_all = passed_all and c8 and c9

    # -------------------------------------------------------------
    # GATE 4: Zero Leakage Verification
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 4] Strict Zero Leakage Verification{RESET}")
    train_val_id = qids["train"] & qids["val"]
    train_test_id = qids["train"] & qids["test"]
    val_test_id = qids["val"] & qids["test"]
    id_leakage = len(train_val_id) + len(train_test_id) + len(val_test_id)

    c10 = check(
        "Question ID overlap is strictly 0.0%",
        id_leakage == 0,
        f"Overlaps detected: {train_val_id | train_test_id | val_test_id}"
    )

    def extract_q(content):
        match = re.search(r"INTERVIEW QUESTION:\s*(.*?)\n\nCANDIDATE ANSWER:", content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip().lower() if match else content.strip().lower()

    qtexts = {s: {extract_q(r["messages"][1]["content"]) for r in data[s]} for s in splits}
    text_leakage = len(qtexts["train"] & qtexts["val"]) + len(qtexts["train"] & qtexts["test"]) + len(qtexts["val"] & qtexts["test"])

    c11 = check(
        "Normalized Question Text overlap is strictly 0.0%",
        text_leakage == 0,
        f"Text overlaps: {len(qtexts['train'] & qtexts['val'])} (Train/Val), {len(qtexts['train'] & qtexts['test'])} (Train/Test)"
    )
    passed_all = passed_all and c10 and c11

    # -------------------------------------------------------------
    # GATE 5: Production Schema Validation
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 5] Production Schema Compliance (AnswerEvaluation){RESET}")
    schema_errors = 0
    score_errors = 0
    for r in all_samples:
        content = json.loads(r["messages"][-1]["content"])
        try:
            obj = AnswerEvaluation.model_validate(content)
            if not (0 <= obj.correctness_score <= 10 and 0 <= obj.depth_score <= 10):
                score_errors += 1
        except Exception:
            schema_errors += 1

    c12 = check(
        "100% of samples (144/144) validate against AnswerEvaluation schema",
        schema_errors == 0,
        f"Schema validation errors: {schema_errors}"
    )
    c13 = check(
        "100% of score boundaries are valid (0 <= score <= 10)",
        score_errors == 0,
        f"Score boundary errors: {score_errors}"
    )
    passed_all = passed_all and c12 and c13

    # -------------------------------------------------------------
    # GATE 6: Grounding & Citation Integrity
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 6] RAG Grounding & Citation Source Verification{RESET}")
    citation_errors = 0
    total_citations = 0
    for r in all_samples:
        user_prompt = r["messages"][1]["content"]
        assistant_json = json.loads(r["messages"][-1]["content"])
        citations = assistant_json.get("citations", [])
        for cit in citations:
            total_citations += 1
            src_num = cit.get("source_number")
            if f"[{src_num}]" not in user_prompt:
                citation_errors += 1

    c14 = check(
        f"All {total_citations} citations match actual [N] tags in user prompt",
        citation_errors == 0,
        f"Hallucinated citations: {citation_errors}"
    )
    passed_all = passed_all and c14

    # -------------------------------------------------------------
    # GATE 7: ChatML Formatting & Token Lengths
    # -------------------------------------------------------------
    print(f"\n{BOLD}[Gate 7] ChatML Integrity & Training Readiness{RESET}")
    chatml_ok = True
    for r in all_samples:
        msgs = r.get("messages", [])
        if len(msgs) != 3 or msgs[0]["role"] != "system" or msgs[1]["role"] != "user" or msgs[2]["role"] != "assistant":
            chatml_ok = False
            break

    c15 = check(
        "Every row has exactly 3 ChatML turns: system -> user -> assistant",
        chatml_ok,
        "System prompt, user interview prompt, assistant evaluation JSON"
    )
    passed_all = passed_all and c15

    # -------------------------------------------------------------
    # SUMMARY REPORT
    # -------------------------------------------------------------
    print(f"\n{BOLD}======================================================{RESET}")
    if passed_all:
        print(f"{GREEN}{BOLD}🎉 ALL 7 TEST GATES PASSED! PHASE A IS VERIFIED & READY.{RESET}")
        print(f"{BOLD}======================================================{RESET}")
        print(f"• Question Bank : 48 Canonical Questions (8 per subject x 6 subjects)")
        print(f"• Train Split   : 108 samples (36 questions) -> Ready for QLoRA")
        print(f"• Val Split     : 18 samples (6 questions)   -> Ready for Checkpoint Selection")
        print(f"• Test Split    : 18 samples (6 questions)   -> {BOLD}LOCKED & FROZEN for Benchmark{RESET}")
        print(f"\nYou can now safely proceed to {BOLD}PHASE B — EXPERIMENT{RESET}.\n")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}❌ SOME GATES FAILED! INSPECT ERRORS ABOVE.{RESET}")
        print(f"{BOLD}======================================================{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
