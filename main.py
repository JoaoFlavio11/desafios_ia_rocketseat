from datetime import date
from uuid import UUID, uuid4
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Rocketseat - Desafio Prompt Engineering: FastAPI Item API",
    description="API para validação e processamento de objetos do tipo Item com geração dinâmica de UUID.",
    version="1.0.0",
)


class Item(BaseModel):
    nome: str = Field(
        ...,
        max_length=25,
        description="Nome do item com no máximo 25 caracteres.",
        examples=["Notebook Gamer"],
    )
    valor: float = Field(
        ...,
        description="Valor numérico do item.",
        examples=[4500.50],
    )
    data: date = Field(
        ...,
        description="Data no formato YYYY-MM-DD. Não pode ser superior à data atual.",
        examples=["2026-11-04"],
    )

    @field_validator("data")
    @classmethod
    def validar_data_nao_futura(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("A data não pode ser superior à data atual.")
        return v


class ItemResponse(Item):
    uuid: UUID = Field(
        ...,
        description="Identificador único gerado dinamicamente para o item processado.",
    )


@app.post(
    "/items/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar e processar Item",
    description="Valida o objeto Item recebido e retorna os dados com um UUID dinâmico gerado.",
)
@app.post(
    "/item/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_item(item: Item) -> ItemResponse:
    item_dict = item.model_dump()
    return ItemResponse(uuid=uuid4(), **item_dict)


@app.get("/", summary="Health Check")
def health_check():
    return {
        "status": "online",
        "message": "Desafio Prompt Engineering FastAPI endpoint está rodando com sucesso!",
    }
