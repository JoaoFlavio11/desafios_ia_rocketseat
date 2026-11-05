import argparse
import os
from rag_service import (
    QUESTIONS,
    answer_with_naive_rag,
    answer_with_parent_rag,
    answer_with_rerank_rag,
)
from naive_rag import run_naive_rag
from parent_rag import run_parent_rag
from rerank_rag import run_rerank_rag


def run_comparative_analysis(pdf_path: str = "os-sertoes.pdf"):
    print("=" * 80)
    print("⚖️  ANÁLISE COMPARATIVA: NAIVE RAG vs PARENT RAG vs RERANK RAG")
    print("Livro: 'Os Sertões' — Euclides da Cunha")
    print("=" * 80 + "\n")

    resolved_path = os.path.join(os.path.dirname(__file__), pdf_path)

    for i, question in enumerate(QUESTIONS):
        print(f"\n================================================================================")
        print(f"❓ PERGUNTA {i + 1}: {question}")
        print("================================================================================\n")

        ans_naive = answer_with_naive_rag(question, pdf_path=resolved_path, index_offset=i)
        ans_parent = answer_with_parent_rag(question, pdf_path=resolved_path, index_offset=i)
        ans_rerank = answer_with_rerank_rag(question, pdf_path=resolved_path, index_offset=i)

        print(f"📌 [1. NAIVE RAG]:\n{ans_naive}\n")
        print(f"📌 [2. PARENT DOCUMENT RAG]:\n{ans_parent}\n")
        print(f"📌 [3. RERANK RAG (COHERE)]:\n{ans_rerank}\n")


def main():
    parser = argparse.ArgumentParser(description="Desafio RAG - Os Sertões (Euclides da Cunha)")
    parser.add_argument(
        "--model",
        "-m",
        choices=["naive", "parent", "rerank", "all", "compare"],
        default="compare",
        help="Estrutura de RAG a executar (naive, parent, rerank, all ou compare)",
    )
    parser.add_argument("--pdf", type=str, default="os-sertoes.pdf", help="Caminho do arquivo PDF")

    args = parser.parse_args()

    if args.model == "naive":
        run_naive_rag(pdf_path=args.pdf)
    elif args.model == "parent":
        run_parent_rag(pdf_path=args.pdf)
    elif args.model == "rerank":
        run_rerank_rag(pdf_path=args.pdf)
    elif args.model == "all":
        run_naive_rag(pdf_path=args.pdf)
        run_parent_rag(pdf_path=args.pdf)
        run_rerank_rag(pdf_path=args.pdf)
    elif args.model == "compare":
        run_comparative_analysis(pdf_path=args.pdf)


if __name__ == "__main__":
    main()

