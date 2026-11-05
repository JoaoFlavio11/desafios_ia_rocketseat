import argparse
import json
from classifier import DepartmentClassifier


def predict_message(text: str, model_path: str = None):
    classifier = DepartmentClassifier(model_path=model_path)
    result = classifier.predict(text)
    print("\n" + "=" * 60)
    print("🤖 CLASSIFICAÇÃO DE MENSAGEM DO BOT")
    print("=" * 60)
    print(f"💬 Mensagem: \"{result['prompt']}\"")
    print(f"🏷️  Categoria: {result['category'].upper()}")
    print(f"🎯 Confiança: {result['confidence'] * 100:.2f}%")
    print(f"⚙️  Motor: {result['engine']}")
    print(f"📊 Probabilidades: {json.dumps(result['probabilities'], indent=2)}")
    print("=" * 60 + "\n")
    return result


def main():
    parser = argparse.ArgumentParser(description="Classificação em tempo real de mensagem de cliente")
    parser.add_argument("message", type=str, nargs="?", default="Olá, gostaria de saber o preço da TV 55 polegadas e se tem desconto à vista.", help="Texto da mensagem do cliente")
    parser.add_argument("--model-path", type=str, default="./bert-department-classification", help="Caminho do modelo treinado")

    args = parser.parse_args()
    predict_message(args.message, model_path=args.model_path)


if __name__ == "__main__":
    main()
