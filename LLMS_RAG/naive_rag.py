import argparse
import os
from rag_service import QUESTIONS, answer_with_naive_rag


def run_naive_rag(pdf_path: str = "os-sertoes.pdf"):
    print("=" * 70)
    print("📖 EXECUTANDO: NAIVE RAG (Os Sertões - Euclides da Cunha)")
    print("=" * 70)
    print("Estratégia: Chunking direto (4000 chars) -> Chroma VectorDB -> Top-3 Similaridade -> LLM\n")

    resolved_path = os.path.join(os.path.dirname(__file__), pdf_path)

    for i, question in enumerate(QUESTIONS):
        print(f"🔹 [Pergunta {i + 1}]: {question}")
        resposta = answer_with_naive_rag(question, pdf_path=resolved_path, index_offset=i)
        print(f"🔸 [Resposta Naive RAG]:\n{resposta}\n")
        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Executa o modelo Naive RAG sobre o livro Os Sertões.")
    parser.add_argument("--pdf", type=str, default="os-sertoes.pdf", help="Caminho para o arquivo PDF")
    args = parser.parse_args()
    run_naive_rag(pdf_path=args.pdf)


if __name__ == "__main__":
    main()
