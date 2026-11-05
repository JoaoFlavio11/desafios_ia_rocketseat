import os
import json
import pytest
from classifier import DepartmentClassifier, LABEL_MAP, ID_TO_LABEL


def test_datasets_exist():
    """Valida se os arquivos de treino e teste existem e possuem tamanho consistente."""
    base_dir = os.path.dirname(__file__)
    train_path = os.path.join(base_dir, "data", "treino.jsonl")
    test_path = os.path.join(base_dir, "data", "teste.jsonl")

    assert os.path.exists(train_path)
    assert os.path.exists(test_path)
    assert os.path.getsize(train_path) > 10_000
    assert os.path.getsize(test_path) > 2_000


def test_datasets_format_and_counts():
    """Valida se os arquivos JSONL possuem as chaves prompt/completion e contagens esperadas."""
    base_dir = os.path.dirname(__file__)
    train_path = os.path.join(base_dir, "data", "treino.jsonl")
    test_path = os.path.join(base_dir, "data", "teste.jsonl")

    valid_classes = {"venda", "suporte"}

    with open(train_path, "r", encoding="utf-8") as f:
        train_lines = [json.loads(line) for line in f if line.strip()]

    with open(test_path, "r", encoding="utf-8") as f:
        test_lines = [json.loads(line) for line in f if line.strip()]

    assert len(train_lines) == 500
    assert len(test_lines) == 100

    for item in train_lines:
        assert "prompt" in item
        assert "completion" in item
        assert item["completion"].strip().lower() in valid_classes

    for item in test_lines:
        assert "prompt" in item
        assert "completion" in item
        assert item["completion"].strip().lower() in valid_classes


def test_label_mappings():
    """Valida o mapeamento numérico das labels para o modelo BERT."""
    assert LABEL_MAP["suporte"] == 0
    assert LABEL_MAP["venda"] == 1
    assert ID_TO_LABEL[0] == "suporte"
    assert ID_TO_LABEL[1] == "venda"


def test_classifier_venda_intent():
    """Valida se intenções de compra são classificadas como 'venda'."""
    classifier = DepartmentClassifier()

    queries = [
        "Quero comprar uma televisão de 50 polegadas, tem em estoque?",
        "Qual o preço do micro-ondas inox com entrega para São Paulo?",
        "Tem promoção de Black Friday para lavadora de roupas?",
        "Gostaria de saber as opções de parcelamento sem juros no cartão de crédito.",
    ]

    for q in queries:
        res = classifier.predict(q)
        assert res["category"] == "venda"
        assert res["confidence"] > 0.60


def test_classifier_suporte_intent():
    """Valida se intenções de suporte/dúvida/problema são classificadas como 'suporte'."""
    classifier = DepartmentClassifier()

    queries = [
        "Meu ar-condicionado parou de gelar e está fazendo um barulho estranho.",
        "Como faço para solicitar a troca do liquidificador que veio com defeito?",
        "Preciso da segunda via do manual de instruções do fogão elétrico.",
        "A encomenda chegou com a embalagem rasgada e a tela trincada.",
    ]

    for q in queries:
        res = classifier.predict(q)
        assert res["category"] == "suporte"
        assert res["confidence"] > 0.60


def test_evaluation_on_test_dataset():
    """Valida se a acurácia sobre o arquivo de teste atinge padrão satisfatório."""
    classifier = DepartmentClassifier()
    test_path = os.path.join(os.path.dirname(__file__), "data", "teste.jsonl")

    metrics = classifier.evaluate_file(test_path)
    assert metrics["total_examples"] == 100
    assert metrics["correct_predictions"] >= 90
    assert metrics["accuracy"] >= 0.90
    assert metrics["metrics_by_class"]["venda"]["precision"] > 0.85
    assert metrics["metrics_by_class"]["suporte"]["precision"] > 0.85

