from datetime import date, timedelta
from uuid import UUID
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_criar_item_valido():
    hoje = date.today().isoformat()
    payload = {
        "nome": "Teclado Mecanico",
        "valor": 299.90,
        "data": hoje,
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["nome"] == payload["nome"]
    assert data["valor"] == payload["valor"]
    assert data["data"] == payload["data"]
    assert "uuid" in data

    # Valida se o UUID gerado é um UUID válido
    parsed_uuid = UUID(data["uuid"])
    assert str(parsed_uuid) == data["uuid"]


def test_criar_item_com_nome_maior_que_25_caracteres():
    payload = {
        "nome": "EsteNomePossuiMaisDeVinteECincoCaracteres",
        "valor": 100.0,
        "data": date.today().isoformat(),
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("nome" in str(err.get("loc", [])) for err in errors)


def test_criar_item_com_data_no_futuro():
    amanha = (date.today() + timedelta(days=1)).isoformat()
    payload = {
        "nome": "Mouse Gamer",
        "valor": 150.0,
        "data": amanha,
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("A data não pode ser superior à data atual." in str(err.get("msg", "")) for err in errors)


def test_criar_item_com_valor_invalido():
    payload = {
        "nome": "Monitor",
        "valor": "valor_invalido_nao_numerico",
        "data": date.today().isoformat(),
    }
    response = client.post("/items/", json=payload)
    assert response.status_code == 422
