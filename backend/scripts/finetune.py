import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
import torch
import os

def main():
    print("Loading synthetic dataset...")
    # Load dataset
    df = pd.read_csv("data/dataset.csv")
    
    # Map string labels to integers
    model_id = "j-hartmann/emotion-english-distilroberta-base"
    
    # We retrieve the label mapping from the distilroberta configuration
    labels = sorted(df['label'].unique())
    id2label = {i: label for i, label in enumerate(labels)}
    label2id = {label: i for i, label in enumerate(labels)}
    
    df['label'] = df['label'].map(label2id)

    # Split dataset
    train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

    train_dataset = Dataset.from_pandas(train_df)
    eval_dataset = Dataset.from_pandas(eval_df)

    # Initialize tokenizer
    print(f"Loading tokenizer {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    tokenized_train = train_dataset.map(tokenize_function, batched=True)
    tokenized_eval = eval_dataset.map(tokenize_function, batched=True)

    # Load model
    print("Loading base model...")
    model = AutoModelForSequenceClassification.from_pretrained(
        model_id, 
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True # if labels size changed, init new classifier head
    )

    # Setup Trainer
    training_args = TrainingArguments(
        output_dir="./models/fine_tuned_emotion",
        eval_strategy="epoch",  # Changed from evaluation_strategy for accelerate compatibility
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        save_strategy="epoch",
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        processing_class=tokenizer,
    )

    # Start training
    print("Beginning fine-tuning (resuming from checkpoint if available)...")
    checkpoint = None
    if os.path.exists("./models/fine_tuned_emotion"):
        checkpoints = [d for d in os.listdir("./models/fine_tuned_emotion") if d.startswith("checkpoint-")]
        if checkpoints:
            checkpoint = True # Trainer will find the latest one in output_dir

    trainer.train(resume_from_checkpoint=checkpoint)

    # Save final model locally
    final_path = "./models/fine_tuned_emotion/final"
    os.makedirs(final_path, exist_ok=True)
    trainer.save_model(final_path)
    print(f"Fine-tuning complete. Model saved to {final_path}")

if __name__ == "__main__":
    main()
