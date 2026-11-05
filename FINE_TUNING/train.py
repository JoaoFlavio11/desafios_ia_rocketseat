import os
import argparse
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def train_model(
    train_file: str = "treino.jsonl",
    test_file: str = "teste.jsonl",
    checkpoint: str = "bert-base-uncased",
    output_dir: str = "./bert-department-classification",
    epochs: int = 5,
    batch_size: int = 8,
    push_to_hub: bool = False,
    hub_repo_id: str = None,
):
    """Executa o pipeline de Fine-Tuning do modelo BERT para classificação de departamento."""
    print("=" * 70)
    print("🚀 INICIANDO TREINAMENTO DE FINE-TUNING — BERT CLASSIFIER")
    print(f"📦 Modelo base: {checkpoint}")
    print(f"📄 Arquivo de treino: {train_file}")
    print(f"📄 Arquivo de teste: {test_file}")
    print(f"⚙️  Épocas: {epochs} | Batch size: {batch_size}")
    print("=" * 70 + "\n")

    from datasets import load_dataset
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        DataCollatorWithPadding,
        TrainingArguments,
        Trainer,
    )
    import numpy as np
    import evaluate

    # 1. Carregamento dos dados JSONL
    print("1️⃣  Carregando e preparando datasets...")
    dataset = load_dataset("json", data_files={"train": train_file, "test": test_file})
    dataset = dataset.map(
        lambda ex: {
            "input": ex["prompt"],
            "output": ex["completion"],
        },
        remove_columns=["prompt", "completion"],
    )

    # 2. Tokenização e mapeamento de labels
    print("2️⃣  Tokenizando textos com WordPiece...")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    label_map = {"suporte": 0, "venda": 1}

    def transform_labels(batch):
        return {"label": [label_map[item.strip().lower()] for item in batch["output"]]}

    def tokenize_fn(batch):
        return tokenizer(batch["input"], padding=True, truncation=True)

    tokenized_datasets = dataset.map(tokenize_fn, batched=True)
    tokenized_datasets = tokenized_datasets.map(transform_labels, batched=True)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # 3. Configuração do modelo e hiperparâmetros
    print("3️⃣  Inicializando modelo de classificação e hiperparâmetros...")
    model = AutoModelForSequenceClassification.from_pretrained(checkpoint, num_labels=2)

    os.environ["WANDB_DISABLE"] = "true"
    os.environ["WANDB_MODE"] = "offline"

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        weight_decay=0.01,
        logging_dir="./logs.log",
        logging_steps=50,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        report_to="none",
    )

    metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    # 4. Inicialização do Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # 5. Execução do treinamento
    print("\n4️⃣  Executando fine-tuning do modelo...")
    train_results = trainer.train()
    print("✅ Treinamento finalizado!")

    # 6. Avaliação final
    print("\n5️⃣  Avaliando modelo no conjunto de teste...")
    eval_results = trainer.evaluate()
    print(f"📊 Resultados da Avaliação: {eval_results}")

    # 7. Salvando modelo localmente
    print(f"\n6️⃣  Salvando modelo treinado em '{output_dir}'...")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("💾 Modelo salvo com sucesso!")

    # 8. Opcional: Push to Hub
    if push_to_hub and hub_repo_id:
        print(f"\n7️⃣  Enviando modelo para o Hugging Face Hub: {hub_repo_id}...")
        hf_token = os.getenv("HF_TOKEN")
        trainer.push_to_hub(hub_repo_id, token=hf_token)
        print("☁️  Modelo publicado no Hub com sucesso!")

    return eval_results


def main():
    parser = argparse.ArgumentParser(description="Fine-Tuning de Modelo BERT para Classificação de Atendimento (Venda vs Suporte)")
    parser.add_argument("--train-file", type=str, default="data/treino.jsonl", help="Caminho do arquivo de treino")
    parser.add_argument("--test-file", type=str, default="data/teste.jsonl", help="Caminho do arquivo de teste")
    parser.add_argument("--checkpoint", type=str, default=os.getenv("MODEL_CHECKPOINT", "bert-base-uncased"), help="Checkpoint base do modelo")
    parser.add_argument("--output-dir", type=str, default="./bert-department-classification", help="Diretório para salvar o modelo")
    parser.add_argument("--epochs", type=int, default=5, help="Número de épocas de treinamento")
    parser.add_argument("--batch-size", type=int, default=8, help="Tamanho do batch")
    parser.add_argument("--push-to-hub", action="store_true", help="Se definido, envia o modelo ao Hugging Face Hub")
    parser.add_argument("--repo-id", type=str, default=os.getenv("HF_REPO_ID", None), help="ID do repositório no Hub")

    args = parser.parse_args()
    train_model(
        train_file=args.train_file,
        test_file=args.test_file,
        checkpoint=args.checkpoint,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        push_to_hub=args.push_to_hub,
        hub_repo_id=args.repo_id,
    )


if __name__ == "__main__":
    main()

