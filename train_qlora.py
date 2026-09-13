"""
CrackProof QLoRA Fine-Tuning Script.

Fine-tunes an open-source LLM (Llama-3.1-8B-Instruct or Qwen2.5-7B-Instruct)
to act as the specialized CrackProof Technical Evaluator.

Features:
  - 4-bit quantization (bitsandbytes) for low-memory GPU training (works on free Colab T4 / A10G)
  - LoRA adapter (PEFT) on attention projection layers (q, k, v, o, gate, up, down)
  - Formatted ChatML dataset (train.jsonl and val.jsonl)
  - Saves adapter to ./crackproof_qlora_adapter

Usage:
    pip install torch transformers peft trl bitsandbytes accelerate
    python3 train_qlora.py --base-model meta-llama/Meta-Llama-3.1-8B-Instruct
"""

import os
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Train CrackProof QLoRA Evaluator")
    parser.add_argument(
        "--base-model",
        type=str,
        default="Qwen/Qwen2.5-3B-Instruct",
        help="Hugging Face model ID (e.g. Qwen/Qwen2.5-3B-Instruct)"
    )
    parser.add_argument("--data-dir", type=str, default="dataset", help="Directory containing train.jsonl & val.jsonl")
    parser.add_argument("--output-dir", type=str, default="./crackproof_qlora_adapter", help="Directory to save adapter")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs")
    parser.add_argument("--batch-size", type=int, default=2, help="Per-device train batch size")
    parser.add_argument("--lr", type=float, default=2e-4, help="Learning rate")
    args = parser.parse_args()

    train_file = os.path.join(args.data_dir, "train.jsonl")
    val_file = os.path.join(args.data_dir, "val.jsonl")

    if not os.path.exists(train_file):
        print(f"Error: {train_file} not found. Run python3 prepare_training_data.py first.")
        sys.exit(1)

    print(f"Loading environment for QLoRA training on: {args.base_model}")

    try:
        import random
        import numpy as np
        import torch
        import transformers
        from datasets import load_dataset
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainingArguments,
            Trainer,
            DataCollatorForSeq2Seq,
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    except ImportError as e:
        print(f"\nMissing required ML training packages: {e}")
        print("Install them with:\n  pip install torch transformers peft trl bitsandbytes accelerate datasets\n")
        sys.exit(1)

    # Set explicit random seeds for deterministic reproducibility
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)
    transformers.set_seed(42)

    print("\n[1/5] Loading quantized 4-bit base model...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    print("\n[2/5] Configuring LoRA adapter...")
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    print("\n[3/5] Loading datasets...")
    dataset = load_dataset("json", data_files={"train": train_file, "validation": val_file})

    print("\n[4/5] Starting SFT training...")
    # Dynamic eval keyword for Hugging Face version compatibility
    eval_key = "eval_strategy" if hasattr(TrainingArguments, "eval_strategy") else "evaluation_strategy"

    training_kwargs = {
        "output_dir": args.output_dir,
        "num_train_epochs": args.epochs,
        "per_device_train_batch_size": args.batch_size,
        "gradient_accumulation_steps": 4,
        "learning_rate": args.lr,
        "optim": "paged_adamw_8bit",
        "lr_scheduler_type": "cosine",
        "logging_steps": 1,
        eval_key: "steps",
        "eval_steps": 2,
        "save_strategy": "steps",
        "save_steps": 2,
        "save_total_limit": 2,
        "load_best_model_at_end": True,
        "metric_for_best_model": "eval_loss",
        "greater_is_better": False,
        "fp16": True,
        "report_to": "none",
        "seed": 42,
        "data_seed": 42,
    }

    # Completion-only loss masking:
    # System, User, Question, Candidate Answer, and RAG Reference tokens -> labels = -100
    # Assistant JSON completion tokens -> supervised token IDs
    def tokenize_completion_only(batch):
        input_ids_list = []
        labels_list = []
        attention_mask_list = []
        max_seq_len = 2048

        for messages in batch["messages"]:
            prompt_messages = messages[:-1]
            prompt_text = tokenizer.apply_chat_template(
                prompt_messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            full_text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )

            prompt_ids = tokenizer(prompt_text, add_special_tokens=False)["input_ids"]
            full_ids = tokenizer(full_text, add_special_tokens=False)["input_ids"]

            # Prompt tokens get label -100 (ignored in loss computation)
            # Assistant completion tokens get their actual token IDs
            labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]

            if len(full_ids) > max_seq_len:
                full_ids = full_ids[:max_seq_len]
                labels = labels[:max_seq_len]

            input_ids_list.append(full_ids)
            labels_list.append(labels)
            attention_mask_list.append([1] * len(full_ids))

        return {
            "input_ids": input_ids_list,
            "labels": labels_list,
            "attention_mask": attention_mask_list,
        }

    train_data = dataset["train"].map(
        tokenize_completion_only,
        batched=True,
        remove_columns=dataset["train"].column_names,
    )
    val_data = dataset["validation"].map(
        tokenize_completion_only,
        batched=True,
        remove_columns=dataset["validation"].column_names,
    )

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        pad_to_multiple_of=8,
        label_pad_token_id=-100,
    )

    training_args = TrainingArguments(**training_kwargs)
    import inspect
    trainer_kwargs = {
        "model": model,
        "train_dataset": train_data,
        "eval_dataset": val_data,
        "data_collator": data_collator,
        "args": training_args,
    }
    if "processing_class" in inspect.signature(Trainer.__init__).parameters:
        trainer_kwargs["processing_class"] = tokenizer
    else:
        trainer_kwargs["tokenizer"] = tokenizer

    trainer = Trainer(**trainer_kwargs)

    trainer.train()

    print(f"\n[5/5] Saving best fine-tuned LoRA adapter to {args.output_dir}...")
    trainer.model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Fine-tuning completed successfully!")

    # Generate loss curve if matplotlib is available
    try:
        import matplotlib.pyplot as plt
        train_steps, train_losses = [], []
        eval_steps, eval_losses = [], []
        for entry in trainer.state.log_history:
            if "loss" in entry and "step" in entry:
                train_steps.append(entry["step"])
                train_losses.append(entry["loss"])
            if "eval_loss" in entry and "step" in entry:
                eval_steps.append(entry["step"])
                eval_losses.append(entry["eval_loss"])

        if train_losses:
            plt.figure(figsize=(10, 5), dpi=150)
            plt.plot(train_steps, train_losses, label="Training Loss", color="#1f77b4", linewidth=2, marker="o")
            if eval_losses:
                plt.plot(eval_steps, eval_losses, label="Validation Loss", color="#d62728", linewidth=2, linestyle="--", marker="s")
            plt.title("CrackProof QLoRA: Training vs Validation Loss Curve")
            plt.xlabel("Optimizer Steps")
            plt.ylabel("Loss")
            plt.grid(True, linestyle=":", alpha=0.6)
            plt.legend()
            plt.tight_layout()
            plt.savefig("crackproof_loss_curve.png", dpi=300)
            print("[PLOT] Saved loss curve to crackproof_loss_curve.png")
    except Exception as e:
        print(f"Plot generation skipped: {e}")


if __name__ == "__main__":
    main()
