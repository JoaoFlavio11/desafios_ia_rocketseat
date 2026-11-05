import os
import pytest
from rag_service import (
    QUESTIONS,
    answer_with_naive_rag,
    answer_with_parent_rag,
    answer_with_rerank_rag,
    get_compatible_retrievers,
)


def test_questions_integrity():
    """Valida se as 5 perguntas obrigatórias do desafio estão presentes."""
    assert len(QUESTIONS) == 5
    assert "ambiente natural do sertão" in QUESTIONS[0]
    assert "características da população sertaneja" in QUESTIONS[1]
    assert "Guerra de Canudos" in QUESTIONS[2]
    assert "Antônio Conselheiro" in QUESTIONS[3]
    assert "crítica social e política" in QUESTIONS[4]


def test_pdf_exists():
    """Valida se o livro Os Sertões em PDF está disponível na pasta."""
    pdf_path = os.path.join(os.path.dirname(__file__), "os-sertoes.pdf")
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 1_000_000


def test_compatible_retrievers_import():
    """Valida se os recuperadores compatíveis do LangChain são importados sem erro."""
    ParentRetriever, CompressionRetriever, ByteStore = get_compatible_retrievers()
    assert ParentRetriever is not None
    assert CompressionRetriever is not None
    assert ByteStore is not None


def test_naive_rag_answers():
    """Testa a geração de resposta com Naive RAG para a pergunta 1."""
    pdf_path = os.path.join(os.path.dirname(__file__), "os-sertoes.pdf")
    resp = answer_with_naive_rag(QUESTIONS[0], pdf_path=pdf_path, index_offset=0)
    assert resp is not None
    assert len(resp) > 80
    assert "sertão" in resp.lower() or "euclides" in resp.lower()


def test_parent_rag_answers():
    """Testa a geração de resposta com Parent RAG para a pergunta 2."""
    pdf_path = os.path.join(os.path.dirname(__file__), "os-sertoes.pdf")
    resp = answer_with_parent_rag(QUESTIONS[1], pdf_path=pdf_path, index_offset=1)
    assert resp is not None
    assert len(resp) > 80
    assert "sertanejo" in resp.lower() or "forte" in resp.lower() or "população" in resp.lower()


def test_rerank_rag_answers():
    """Testa a geração de resposta com Rerank RAG para a pergunta 4."""
    pdf_path = os.path.join(os.path.dirname(__file__), "os-sertoes.pdf")
    resp = answer_with_rerank_rag(QUESTIONS[3], pdf_path=pdf_path, index_offset=3)
    assert resp is not None
    assert len(resp) > 80
    assert "conselheiro" in resp.lower()
