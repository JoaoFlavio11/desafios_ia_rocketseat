import argparse
import os
from rag_service import QUESTIONS, answer_with_rerank_rag


def run_rerank_rag(pdf_path: str = "os-sertoes.pdf"):
    print("=" * 70)
    print("📖 EXECUTANDO: RERANK RAG (Os Sertões - Euclides da Cunha)")
    print("=" * 70)
    print("Estratégia: Recuperação ampla Top-10 no VectorDB + Reclassificação semântica (Cohere Rerank) Top-3 -> LLM\n")

    resolved_path = os.path.join(os.path.dirname(__file__), pdf_path)

    for i, question in enumerate(QUESTIONS):
        print(f"🔹 [Pergunta {i + 1}]: {question}")
        resposta = answer_with_rerank_rag(question, pdf_path=resolved_path, index_offset=i)
        print(f"🔸 [Resposta Rerank RAG]:\n{resposta}\n")
        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Executa o modelo Rerank RAG sobre o livro Os Sertões.")
    parser.add_argument("--pdf", type=str, default="os-sertoes.pdf", help="Caminho para o arquivo PDF")
    args = parser.parse_args()
    run_rerank_rag(pdf_path=args.pdf)


if __name__ == "__main__":
    main()

