import argparse
import os
import json
from classifier import DepartmentClassifier


def run_evaluation(test_file: str = "data/teste.jsonl", model_path: str = None):
    print("=" * 70)
    print("📊 AVALIAÇÃO DO MODELO NO DATASET DE TESTE")
    print(f"📄 Arquivo: {test_file}")
    print("=" * 70)

    classifier = DepartmentClassifier(model_path=model_path)
    metrics = classifier.evaluate_file(test_file)

    print(f"\n📈 Total de exemplos avaliados: {metrics['total_examples']}")
    print(f"🎯 Acertos: {metrics['correct_predictions']} / {metrics['total_examples']}")
    print(f"🏆 Acurácia Geral: {metrics['accuracy'] * 100:.2f}%\n")

    print("--- Métricas Detalhadas por Classe ---")
    for cls_name, cls_metrics in metrics["metrics_by_class"].items():
        print(f"• Classe [{cls_name.upper()}]:")
        print(f"   - Total de amostras: {cls_metrics['total']}")
        print(f"   - Precisão: {cls_metrics['precision'] * 100:.2f}%")
        print(f"   - Recall:   {cls_metrics['recall'] * 100:.2f}%")
    print("=" * 70 + "\n")
    return metrics


def run_interactive_demo(model_path: str = None):
    classifier = DepartmentClassifier(model_path=model_path)
    sample_queries = [
        "Olá! Vi que o aspirador de pó robô está em promoção, ainda tem em estoque?",
        "Comprei uma cafeteira semana passada e ela não está esquentando a água, como peço a troca?",
        "Qual o valor do frete para o CEP 01001-000 se eu comprar a geladeira duplex?",
        "Meu ar-condicionado está fazendo um barulho muito estranho depois que liguei hoje de manhã.",
        "Gostaria de ver o catálogo de sofás e opções de parcelamento no cartão.",
        "Como faço para solicitar a segunda via da nota fiscal do meu pedido?",
    ]

    print("=" * 75)
    print("🎮 DEMONSTRAÇÃO DO BOT DE ATENDIMENTO — CLASSIFICAÇÃO AUTOMÁTICA")
    print("=" * 75)

    for i, query in enumerate(sample_queries, start=1):
        res = classifier.predict(query)
        cat_badge = "🛒 [VENDA]" if res["category"] == "venda" else "🛠️  [SUPORTE]"
        print(f"\n💬 Exemplo {i}: \"{query}\"")
        print(f"   {cat_badge} (Confiança: {res['confidence'] * 100:.1f}%) | Motor: {res['engine']}")
    print("\n" + "=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Desafio Fine-Tuning: Classificador de Mensagens de Atendimento (Venda vs Suporte)")
    parser.add_argument(
        "--mode",
        choices=["evaluate", "demo", "predict", "train"],
        default="demo",
        help="Modo de execução: demo, evaluate, predict ou train",
    )
    parser.add_argument("--message", type=str, default="Quero comprar uma TV 4k", help="Mensagem para predizer (usado no modo predict)")
    parser.add_argument("--test-file", type=str, default="data/teste.jsonl", help="Arquivo JSONL de teste")
    parser.add_argument("--model-path", type=str, default="./bert-department-classification", help="Caminho do modelo local")

    args = parser.parse_args()

    if args.mode == "demo":
        run_interactive_demo(model_path=args.model_path)
        run_evaluation(test_file=args.test_file, model_path=args.model_path)
    elif args.mode == "evaluate":
        run_evaluation(test_file=args.test_file, model_path=args.model_path)
    elif args.mode == "predict":
        from predict import predict_message
        predict_message(args.message, model_path=args.model_path)
    elif args.mode == "train":
        from train import train_model
        train_model()


if __name__ == "__main__":
    main()

