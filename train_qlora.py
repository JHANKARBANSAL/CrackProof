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
        default="Qwen/Qwen2.5-7B-Instruct",
        help="Hugging Face model ID (e.g. Qwen/Qwen2.5-7B-Instruct or meta-llama/Meta-Llama-3.1-8B-Instruct)"
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
        import torch
        from datasets import load_dataset
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            TrainingArguments,
        )
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
        from trl import SFTTrainer
    except ImportError as e:
        print(f"\nMissing required ML training packages: {e}")
        print("Install them with:\n  pip install torch transformers peft trl bitsandbytes accelerate datasets\n")
        sys.exit(1)

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
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=4,
        learning_rate=args.lr,
        optim="paged_adamw_8bit",
        lr_scheduler_type="cosine",
        warmup_ratio=0.03,
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch",
        fp16=True,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        dataset_text_field="messages",
        max_seq_length=2048,
        tokenizer=tokenizer,
        args=training_args,
    )

    trainer.train()

    print(f"\n[5/5] Saving fine-tuned LoRA adapter to {args.output_dir}...")
    trainer.model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Fine-tuning completed successfully!")


if __name__ == "__main__":
    main()
