"""
CrackProof Phase B: Base Model Benchmark on Frozen Test Set.

Evaluates raw Qwen2.5-3B-Instruct (base model without fine-tuning)
on dataset/test.jsonl (18 frozen samples) using Ollama local inference.

Metrics calculated:
1. Valid JSON Parsing Rate (%)
2. Pydantic Schema Adherence Rate (%)
3. Verdict Classification Accuracy (%)
4. Mean Absolute Error (MAE) on Correctness & Depth Scores
5. Citation Grounding & Source Number Accuracy (%)
6. Per-Subject Performance Breakdown (Java, OOP, DBMS, OS, CN, DSA)

Saves detailed predictions to benchmark_base_model_predictions.json.
"""

import json
import os
import sys
import time
import urllib.request
from evaluator import AnswerEvaluation

TEST_FILE = "dataset/test.jsonl"
OUTPUT_FILE = "benchmark_base_model_predictions.json"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def query_ollama(messages):
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.0,
            "seed": 42,
        },
        "format": "json"  # request JSON mode
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["message"]["content"]


def clean_json_text(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def run_benchmark():
    print("===============================================================")
    print("CRACKPROOF PHASE B: BASE MODEL BENCHMARK ON FROZEN TEST SET")
    print(f"Model       : {MODEL_NAME} (Base Model, Zero-Shot / Un-tuned)")
    print(f"Test Set    : {TEST_FILE} (18 Frozen Samples across 6 Subjects)")
    print("===============================================================\n")

    if not os.path.exists(TEST_FILE):
        print(f"Error: {TEST_FILE} does not exist!")
        sys.exit(1)

    with open(TEST_FILE, "r", encoding="utf-8") as f:
        test_samples = [json.loads(line) for line in f]

    print(f"Loaded {len(test_samples)} test samples.\n")

    results = []
    json_parse_success = 0
    schema_valid_success = 0
    verdict_matches = 0
    total_samples = len(test_samples)
    
    correctness_errors = []
    depth_errors = []
    citation_valid_count = 0
    citation_total_count = 0

    subject_stats = {}

    for i, item in enumerate(test_samples):
        qid = item["question_id"]
        subject = item["subject"]
        msgs = item["messages"]
        ground_truth = json.loads(msgs[-1]["content"])
        
        prompt_messages = msgs[:-1]
        user_prompt = prompt_messages[1]["content"]

        print(f"[{i+1}/{total_samples}] Evaluating {qid} ({subject}) - True: {ground_truth['verdict']} (Score: {ground_truth['correctness_score']}/10)...", end=" ", flush=True)

        start_time = time.time()
        raw_response = query_ollama(prompt_messages)
        latency = time.time() - start_time

        parsed_json = None
        is_valid_json = False
        is_schema_valid = False
        pred_verdict = None
        pred_corr = None
        pred_depth = None
        pred_citations = []
        schema_error_msg = ""

        try:
            parsed_json = json.loads(clean_json_text(raw_response))
            is_valid_json = True
            json_parse_success += 1
        except Exception as e:
            schema_error_msg = f"JSON Decode Error: {e}"

        if is_valid_json and isinstance(parsed_json, dict):
            try:
                # Validate against production Pydantic schema
                AnswerEvaluation.model_validate(parsed_json)
                is_schema_valid = True
                schema_valid_success += 1
            except Exception as e:
                schema_error_msg = f"Pydantic Validation Error: {e}"

            pred_verdict = parsed_json.get("verdict")
            pred_corr = parsed_json.get("correctness_score")
            pred_depth = parsed_json.get("depth_score")
            pred_citations = parsed_json.get("citations", [])

        # Verdict match check
        verdict_match = (pred_verdict == ground_truth["verdict"])
        if verdict_match:
            verdict_matches += 1

        # Score delta check
        if isinstance(pred_corr, (int, float)):
            corr_err = abs(pred_corr - ground_truth["correctness_score"])
            correctness_errors.append(corr_err)
        if isinstance(pred_depth, (int, float)):
            depth_err = abs(pred_depth - ground_truth["depth_score"])
            depth_errors.append(depth_err)

        # Citation verification against prompt [N]
        for cit in pred_citations:
            citation_total_count += 1
            if isinstance(cit, dict) and "source_number" in cit:
                src_tag = f"[{cit['source_number']}]"
                if src_tag in user_prompt:
                    citation_valid_count += 1

        # Track by subject
        if subject not in subject_stats:
            subject_stats[subject] = {"total": 0, "verdict_match": 0, "schema_valid": 0}
        subject_stats[subject]["total"] += 1
        if verdict_match:
            subject_stats[subject]["verdict_match"] += 1
        if is_schema_valid:
            subject_stats[subject]["schema_valid"] += 1

        status_str = f"Pred: {pred_verdict} ({pred_corr}/10) | Match: {'✔' if verdict_match else '✘'} | Schema: {'✔' if is_schema_valid else '✘'} ({latency:.1f}s)"
        print(status_str)

        results.append({
            "sample_index": i,
            "question_id": qid,
            "subject": subject,
            "latency_seconds": round(latency, 2),
            "ground_truth": ground_truth,
            "raw_response": raw_response,
            "parsed_prediction": parsed_json,
            "is_valid_json": is_valid_json,
            "is_schema_valid": is_schema_valid,
            "schema_error": schema_error_msg,
            "verdict_match": verdict_match,
            "predicted_verdict": pred_verdict,
            "true_verdict": ground_truth["verdict"],
            "predicted_correctness_score": pred_corr,
            "true_correctness_score": ground_truth["correctness_score"],
            "predicted_depth_score": pred_depth,
            "true_depth_score": ground_truth["depth_score"]
        })

    # Summary calculations
    json_rate = (json_parse_success / total_samples) * 100
    schema_rate = (schema_valid_success / total_samples) * 100
    accuracy = (verdict_matches / total_samples) * 100
    mae_corr = (sum(correctness_errors) / len(correctness_errors)) if correctness_errors else float("nan")
    mae_depth = (sum(depth_errors) / len(depth_errors)) if depth_errors else float("nan")
    citation_precision = (citation_valid_count / citation_total_count * 100) if citation_total_count else 0.0

    print("\n" + "=" * 65)
    print("BASE MODEL BENCHMARK RESULTS (BASELINE SUMMARY)")
    print("=" * 65)
    print(f"Total Evaluated Samples         : {total_samples}")
    print(f"Valid JSON Rate                 : {json_rate:.1f}% ({json_parse_success}/{total_samples})")
    print(f"Pydantic Schema Adherence       : {schema_rate:.1f}% ({schema_valid_success}/{total_samples})")
    print(f"Verdict Classification Accuracy  : {accuracy:.1f}% ({verdict_matches}/{total_samples})")
    print(f"Correctness Score MAE           : {mae_corr:.2f} points")
    print(f"Depth Score MAE                 : {mae_depth:.2f} points")
    print(f"Citation Grounding Precision    : {citation_precision:.1f}% ({citation_valid_count}/{citation_total_count})")
    print("-" * 65)
    print("Subject-by-Subject Breakdown:")
    for sub, stats in subject_stats.items():
        acc = (stats["verdict_match"] / stats["total"]) * 100
        sch = (stats["schema_valid"] / stats["total"]) * 100
        print(f"  • {sub:<6}: Verdict Acc: {acc:>5.1f}% | Schema Adherence: {sch:>5.1f}% ({stats['total']} samples)")
    print("=" * 65)

    # Save detailed output file
    output_data = {
        "benchmark_metadata": {
            "model": MODEL_NAME,
            "test_file": TEST_FILE,
            "total_samples": total_samples,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": {
                "json_parse_rate_percent": round(json_rate, 2),
                "schema_adherence_percent": round(schema_rate, 2),
                "verdict_accuracy_percent": round(accuracy, 2),
                "correctness_score_mae": round(mae_corr, 2),
                "depth_score_mae": round(mae_depth, 2),
                "citation_precision_percent": round(citation_precision, 2)
            },
            "subject_breakdown": subject_stats
        },
        "predictions": results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n[SAVED] Full baseline predictions saved to: {OUTPUT_FILE}")
    return output_data


if __name__ == "__main__":
    run_benchmark()
