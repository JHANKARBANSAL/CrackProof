"""
Prepares RAG-Grounded Fine-Tuning Dataset for CrackProof Evaluator.

Takes evaluations.jsonl (from dual_evaluate.py) or raw Q&A pairs,
formats them into standard ChatML/OpenAI fine-tuning JSONL format:
    {"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}

Each sample includes:
  - System: Evaluation prompt + SOLO taxonomy depth rubric
  - User: Question + Candidate spoken transcript + Retrieved RAG passages with [1], [2]
  - Assistant: Target structured JSON with 4 depth dimensions, verdict, and citations

Usage:
    python3 prepare_training_data.py --in evaluations.jsonl --out-dir dataset/
"""

import json
import os
import sys
import random

from prompts import EVALUATION_PROMPT, RUBRIC_BLOCK, GROUNDING_BLOCK
from rubric import get_rubric
from grounding import get_reference


def build_system_prompt():
    """Constructs the system prompt with rubric included."""
    rubric_text = get_rubric()
    prompt = EVALUATION_PROMPT
    if rubric_text:
        prompt = prompt + RUBRIC_BLOCK.format(rubric=rubric_text)
    return prompt.strip()


def format_user_prompt(question, transcript, reference_text):
    """Formats the user prompt with question, transcript, and RAG references."""
    user_content = f"INTERVIEW QUESTION:\n{question}\n\nCANDIDATE ANSWER:\n{transcript}"
    if reference_text:
        user_content += GROUNDING_BLOCK.format(reference=reference_text)
    return user_content.strip()


def convert_evaluation_row(row):
    """
    Converts one evaluation row into a training sample.
    Uses evaluation_a (or evaluation_b if verified/preferred).
    """
    question = row.get("question", "")
    transcript = row.get("answer", "")
    subject = row.get("subject", "")

    # Target evaluation output
    eval_target = row.get("evaluation_a") or row.get("evaluation")
    if not eval_target:
        return None

    # Retrieve RAG reference text
    reference_text, _ = get_reference(question, subject, top_k=5)

    system_prompt = build_system_prompt()
    user_prompt = format_user_prompt(question, transcript, reference_text)
    assistant_content = json.dumps(eval_target, indent=2)

    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }


def main():
    in_file = "evaluations.jsonl"
    out_dir = "dataset"

    if "--in" in sys.argv:
        in_file = sys.argv[sys.argv.index("--in") + 1]

    if "--out-dir" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out-dir") + 1]

    os.makedirs(out_dir, exist_ok=True)

    if not os.path.exists(in_file):
        print(f"Error: {in_file} not found. Run dual_evaluate.py first.")
        return

    samples = []
    with open(in_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                sample = convert_evaluation_row(row)
                if sample:
                    samples.append(sample)
            except Exception as e:
                print(f"Skipping malformed row: {e}")

    if not samples:
        print("No valid samples found to export.")
        return

    # Shuffle and split: 85% train, 15% validation
    random.seed(42)
    random.shuffle(samples)

    split_idx = max(1, int(len(samples) * 0.85))
    train_samples = samples[:split_idx]
    val_samples = samples[split_idx:] if len(samples) > 1 else samples

    train_path = os.path.join(out_dir, "train.jsonl")
    val_path = os.path.join(out_dir, "val.jsonl")

    with open(train_path, "w") as f:
        for s in train_samples:
            f.write(json.dumps(s) + "\n")

    with open(val_path, "w") as f:
        for s in val_samples:
            f.write(json.dumps(s) + "\n")

    print(f"\nSuccessfully prepared RAG fine-tuning dataset:")
    print(f"  Total samples : {len(samples)}")
    print(f"  Train set     : {len(train_samples)} -> {train_path}")
    print(f"  Validation set: {len(val_samples)} -> {val_path}")


if __name__ == "__main__":
    main()
