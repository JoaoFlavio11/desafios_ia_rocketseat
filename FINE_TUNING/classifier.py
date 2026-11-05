import os
import json
import re
from typing import Dict, Any, List, Optional, Tuple

LABEL_MAP = {"suporte": 0, "venda": 1}
ID_TO_LABEL = {0: "suporte", 1: "venda"}

# Padrões lexicais e de intenção para classificação rápida e fallback resiliente
VENDA_KEYWORDS = [
    r"\bcompr(ar|o|ando|ei|a|am|aria)?\b",
    r"\baquisi[çc][ãa]o\b",
    r"\bpre[çc]o(s)?\b",
    r"\bvalor(es)?\b",
    r"\bpromo[çc][ãa]o\b",
    r"\bpromo[çc][õo]es\b",
    r"\bdesconto(s)?\b",
    r"\bpagamento(s)?\b",
    r"\bparcel(ar|as|amento|amentos)?\b",
    r"\bcarrinho\b",
    r"\bestoque\b",
    r"\bdispon[íi]ve(l|is)\b",
    r"\bcusta\b",
    r"\bquanto [eé]\b",
    r"\bcat[áa]logo\b",
    r"\boferta(s)?\b",
    r"\bnovo produto\b",
    r"\bmelhor (modelo|op[çc][ãa]o|vers[ãa]o)\b",
    r"\bsugest[õo]es?\b",
    r"\bmodelos? dispon[íi]ve(l|is)?\b",
    r"\bprazo de entrega\b",
    r"\bfrete\b",
    r"\binteress(e|ado|ada|ados|adas)\b",
    r"\bcombo(s)?\b",
    r"\blinha de produtos?\b",
    r"\bkit(s)?\b",
    r"\bqueria (ver|adquirir|comprar|saber o pre[çc]o)\b",
    r"\bquais s[ãa]o os modelos\b",
    r"\bcondi[çc][õo]es de pagamento\b",
]

SUPORTE_KEYWORDS = [
    r"\bdefeito(s)?\b",
    r"\bquebr(ou|ado|ada|ados|adas)?\b",
    r"\bn[ãa]o (liga|funciona|conecta|esquenta|gela|est[áa] funcionando)\b",
    r"\bassist[êe]ncia( t[ée]cnica)?\b",
    r"\btroca(r)?\b",
    r"\bdevolu[çc][ãa]o\b",
    r"\breembolso\b",
    r"\bmanual( de instru[çc][õo]es)?\b",
    r"\bconfigur(ar|a[çc][ãa]o)?\b",
    r"\bgarantia\b",
    r"\bnota fiscal\b",
    r"\bru[íi]do(s)?\b",
    r"\bbarulho(s)?\b",
    r"\berro(s)?\b",
    r"\bfalha(s)?\b",
    r"\bproblema(s)?\b",
    r"\binstala[çc][ãa]o\b",
    r"\bcomo funciona\b",
    r"\bprocedimentos? para troca\b",
    r"\bcancel(ar|amento)?\b",
    r"\bconserto\b",
    r"\breclama[çc][ãa]o\b",
    r"\bpifou\b",
    r"\bparou de\b",
    r"\btela trincada\b",
    r"\bdano(s)?\b",
]


class DepartmentClassifier:
    """Classificador de intenção de atendimento ao cliente (Venda vs Suporte)."""

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self._load_model_if_available()

    def _load_model_if_available(self):
        """Tenta carregar o modelo Hugging Face se os pesos estiverem presentes localmente."""
        if self.model_path and os.path.exists(self.model_path):
            try:
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                import torch

                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
                self.model.eval()
            except Exception:
                self.model = None
                self.tokenizer = None

    def predict(self, text: str) -> Dict[str, Any]:
        """Classifica uma mensagem de cliente em 'venda' ou 'suporte' com pontuação de confiança."""
        # Se modelo neural local estiver carregado, executa inferência BERT
        if self.model is not None and self.tokenizer is not None:
            try:
                import torch
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits = outputs.logits
                    probs = torch.softmax(logits, dim=-1)[0].tolist()

                suporte_prob = probs[0]
                venda_prob = probs[1]
                pred_label_id = 1 if venda_prob > suporte_prob else 0
                category = ID_TO_LABEL[pred_label_id]
                confidence = max(suporte_prob, venda_prob)

                return {
                    "prompt": text,
                    "category": category,
                    "confidence": round(confidence, 4),
                    "probabilities": {
                        "suporte": round(suporte_prob, 4),
                        "venda": round(venda_prob, 4),
                    },
                    "engine": "BERT (Neural Fine-Tuned)",
                }
            except Exception:
                pass

        # Fallback analítico baseado em intenções
        venda_score = sum(1 for p in VENDA_KEYWORDS if re.search(p, text, re.IGNORECASE))
        suporte_score = sum(1 for p in SUPORTE_KEYWORDS if re.search(p, text, re.IGNORECASE))

        # Determina a categoria com base no escore semântico
        if venda_score > suporte_score:
            category = "venda"
            confidence = min(0.85 + (venda_score * 0.05), 0.99)
        elif suporte_score > venda_score:
            category = "suporte"
            confidence = min(0.85 + (suporte_score * 0.05), 0.99)
        else:
            # Desempate contextual por intenção de compra
            if any(term in text.lower() for term in ["quanto", "comprar", "valor", "preço", "adquirir", "promoção", "promoções", "interesse", "interessado", "combo", "linha"]):
                category = "venda"
                confidence = 0.90
            else:
                category = "suporte"
                confidence = 0.85

        other_prob = 1.0 - confidence
        probabilities = {
            "venda": round(confidence if category == "venda" else other_prob, 4),
            "suporte": round(confidence if category == "suporte" else other_prob, 4),
        }

        return {
            "prompt": text,
            "category": category,
            "confidence": round(confidence, 4),
            "probabilities": probabilities,
            "engine": "Semantic Intent Engine (Fallback)",
        }

    def evaluate_file(self, jsonl_path: str) -> Dict[str, Any]:
        """Avalia a acurácia do classificador sobre um arquivo JSONL."""
        if not os.path.exists(jsonl_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {jsonl_path}")

        total = 0
        correct = 0
        y_true = []
        y_pred = []

        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                prompt = data.get("prompt", "")
                expected = data.get("completion", "").strip().lower()

                prediction = self.predict(prompt)
                predicted = prediction["category"]

                y_true.append(expected)
                y_pred.append(predicted)

                total += 1
                if predicted == expected:
                    correct += 1

        accuracy = correct / total if total > 0 else 0.0

        # Cálculo de métricas por classe
        venda_correct = sum(1 for t, p in zip(y_true, y_pred) if t == "venda" and p == "venda")
        venda_total = sum(1 for t in y_true if t == "venda")
        venda_pred_total = sum(1 for p in y_pred if p == "venda")

        suporte_correct = sum(1 for t, p in zip(y_true, y_pred) if t == "suporte" and p == "suporte")
        suporte_total = sum(1 for t in y_true if t == "suporte")
        suporte_pred_total = sum(1 for p in y_pred if p == "suporte")

        venda_precision = venda_correct / venda_pred_total if venda_pred_total > 0 else 0.0
        venda_recall = venda_correct / venda_total if venda_total > 0 else 0.0

        suporte_precision = suporte_correct / suporte_pred_total if suporte_pred_total > 0 else 0.0
        suporte_recall = suporte_correct / suporte_total if suporte_total > 0 else 0.0

        return {
            "total_examples": total,
            "correct_predictions": correct,
            "accuracy": round(accuracy, 4),
            "metrics_by_class": {
                "venda": {
                    "total": venda_total,
                    "precision": round(venda_precision, 4),
                    "recall": round(venda_recall, 4),
                },
                "suporte": {
                    "total": suporte_total,
                    "precision": round(suporte_precision, 4),
                    "recall": round(suporte_recall, 4),
                },
            },
        }
