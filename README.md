# 🚀 Desafio: Prompt Engineering — Rocketseat

Este repositório contém a resolução completa e documentada do **Desafio: Prompt Engineering** da Rocketseat.

O objetivo do desafio é demonstrar o domínio de diferentes técnicas de Engenharia de Prompt (*Zero-Shot*, *Few-Shot*, *Chain of Thought* e a metodologia *CIDI: Contexto, Ideia/Instrução, Detalhamento e Iteração*) aplicadas a 4 cenários práticos, culminando na implementação de uma API em **FastAPI** com testes automatizados.

---

## 📑 Sumário

1. [Questão 1 — Ray Tracing e Cálculo de Cor do Pixel](#-questão-1--ray-tracing-e-cálculo-de-cor-do-pixel)
2. [Questão 2 — Decomposição Numérica de 142.981](#-questão-2--decomposição-numérica-de-142981)
3. [Questão 3 — As Crônicas de Gelo e Fogo e a Filosofia de Maquiavel](#-questão-3--as-crônicas-de-gelo-e-fogo-e-a-filosofia-de-maquiavel)
4. [Questão 4 — Endpoint com FastAPI (Item com UUID dinâmico)](#-questão-4--endpoint-com-fastapi-item-com-uuid-dinâmico)
5. [Como Executar o Projeto da Questão 4 Localmente](#-como-executar-o-projeto-da-questão-4-localmente)
6. [Executando os Testes Automatizados](#-executando-os-testes-automatizados)

---

## 🎯 Questão 1 — Ray Tracing e Cálculo de Cor do Pixel

### Enunciado
> *Utilize uma ferramenta de IA Generativa para saber como o algoritmo de Ray Tracing calcula a cor de um pixel em uma imagem renderizada.*

### Técnica Utilizada
* **Zero-Shot Prompting**

### Justificativa da Técnica
Optou-se pela utilização da técnica de **Zero-Shot**, considerando que o *Ray Tracing* é um algoritmo amplamente documentado, consolidado na literatura de Computação Gráfica e com formulações matemáticas bem estabelecidas. Como a questão é conceitual e direta, o modelo já possui base de conhecimento suficiente para formular uma resposta rica e detalhada sem a necessidade de exemplos prévios (*Few-Shot*) ou instruções intermediárias complexas.

### Prompt de Entrada
```text
Como o algoritmo de Ray Tracing calcula a cor de um pixel em uma imagem renderizada?
```

### Resposta Gerada / Esperada
O algoritmo de **Ray Tracing** (Traçado de Raios) calcula a cor final de um pixel simulando o caminho inverso que a luz percorreria do olho/câmera até as fontes de luz na cena:

1. **Geração do Raio Primário (Camera/Eye Ray):**
   - Para cada pixel da imagem final, traça-se um raio partindo da posição da câmera (origem) e passando pelas coordenadas correspondentes do pixel no plano de projeção (espaço de tela).
2. **Teste de Interseção (Ray-Scene Intersection):**
   - O algoritmo calcula se o raio intercepta alguma geometria 3D (esferas, triângulos, malhas).
   - Identifica-se o ponto de impacto mais próximo da câmera ($t_{min}$).
3. **Cálculo da Iluminação Local (Shading):**
   - No ponto de impacto, obtém-se o vetor normal da superfície, a textura e as propriedades do material (difuso, especular, rugosidade).
   - **Raios de Sombra (Shadow Rays):** Disparam-se raios em direção a cada fonte de luz para verificar oclusão. Se houver um objeto no caminho, o ponto está em sombra.
   - Aplica-se um modelo de iluminação (ex.: Phong ou PBR - *Physically Based Rendering*), somando as componentes ambiente, difusa e especular.
4. **Recursão — Raios Secundários (Reflexão e Refração):**
   - Se a superfície for reflexiva (como metal ou espelho), dispara-se um raio refletido.
   - Se for transparente/dielétrica (como vidro ou água), dispara-se um raio refratado aplicando a Lei de Snell.
   - A cor obtida recursivamente por esses raios é ponderada e somada à cor do ponto.
5. **Combinação e Cor Final do Pixel:**
   - A cor final do pixel é a soma acumulada de todas essas contribuições luminosas, frequentemente refinada com técnicas de *antialiasing* (supersampling de múltiplos raios por pixel).

---

## 🔢 Questão 2 — Decomposição Numérica de 142.981

### Enunciado
> *Utilize uma ferramenta de IA Generativa para obter uma resposta completa de como fazer a decomposição numérica de 142.981.*

### Técnicas Utilizadas
* **Few-Shot Prompting**
* **Chain of Thought (CoT - Cadeia de Pensamento)**

### Justificativa da Técnica
Modelos de linguagem às vezes cometem imprecisões em tarefas puramente aritméticas ou representam números em formatos divergentes do esperado. A combinação de:
1. **Few-Shot:** Define de antemão o padrão exato de formatação matemática desejado.
2. **Chain of Thought:** Obriga a IA a explicitar as classes e ordens decimais passo a passo antes de entregar o resultado final, eliminando alucinações e garantindo precisão matemática.

### Prompt de Entrada
```text
Faça a decomposição numérica de 142.981 passo a passo como no exemplo abaixo:

Exemplos:
483 = 400 + 80 + 3
7840 = 7000 + 800 + 40 + 0
```

### Resposta Gerada / Esperada
Para decompor o número **142.981**, analisamos cada dígito de acordo com sua respectiva ordem posicional no sistema decimal:

* **1** na ordem das centenas de milhar: $1 \times 100.000 = 100.000$
* **4** na ordem das dezenas de milhar: $4 \times 10.000 = 40.000$
* **2** na ordem das unidades de milhar: $2 \times 1.000 = 2.000$
* **9** na ordem das centenas simples: $9 \times 100 = 900$
* **8** na ordem das dezenas simples: $8 \times 10 = 80$
* **1** na ordem das unidades simples: $1 \times 1 = 1$

**Formato aditivo final:**
```text
142.981 = 100.000 + 40.000 + 2.000 + 900 + 80 + 1
```

---

## ⚔️ Questão 3 — As Crônicas de Gelo e Fogo e a Filosofia de Maquiavel

### Enunciado
> *Utilize uma ferramenta de IA Generativa para obter quais personagens de As Crônicas de Gelo e Fogo possuem características inspiradas na filosofia de Maquiavel.*

### Técnica Utilizada
* **Metodologia CIDI (Contexto, Instruções/Ideia, Detalhamento e Iteração)** combinada com **Role Prompting**.

### Justificativa da Técnica
A análise comparativa entre uma obra literária de ficção e um tratado político da Renascença (*O Príncipe*, de Nicolau Maquiavel) requer profundidade analítica, rigor conceitual e capacidade de sintetizar psicologia de personagens e teoria política. O framework **CIDI** isola a persona, as instruções operacionais, os critérios conceituais (*virtù*, *fortuna*, moralidade pragmática) e o formato de saída, prevenindo respostas superficiais.

### Prompt de Entrada
```text
[Contexto]
Você é um especialista em literatura comparada e filosofia política clássica, com conhecimento aprofundado sobre a saga "As Crônicas de Gelo e Fogo" de George R. R. Martin e os tratados de Nicolau Maquiavel (em especial "O Príncipe").

[Instruções]
Identifique e analise detalhadamente quais personagens de "As Crônicas de Gelo e Fogo" personificam preceitos e comportamentos associados à filosofia política maquiavélica.

[Detalhamento]
A filosofia de Maquiavel fundamenta-se na manutenção do poder por meio do pragmatismo, na separação entre a moral religiosa e a eficácia política ("os fins justificam os meios"), na preferência por ser temido a ser amado, e no equilíbrio dinâmico entre:
- Virtù: astúcia, competência estratégica, adaptabilidade e força de vontade.
- Fortuna: a sorte, os imprevistos e as circunstâncias externas.

Na sua resposta:
1. Destaque os principais personagens maquiavélicos (ex.: Tywin Lannister, Petyr Baelish, Varys, Cersei Lannister, Tyrion Lannister).
2. Para cada personagem, aponte ações práticas e justifique como se relacionam com conceitos maquiavélicos.
3. Diferencie quem aplica o maquiavelismo com sucesso daquele que fracassa por cometer excessos.

[Iterações]
Estruture a resposta com títulos claros, tópicos bem delineados e uma conclusão reflexiva sobre o realismo político na obra.
```

### Resposta Gerada / Esperada

#### 1. Tywin Lannister — O Arquétipo do Príncipe Temido
* **Conceito Maquiavélico:** *"É muito mais seguro ser temido do que amado, quando se tem de renunciar a um dos dois."*
* **Aplicações na Obra:** 
  - Tywin compreende que o poder deriva da reputação e da autoridade implacável. O massacre dos Reyne de Castamere gerou a balada *"As Chuvas de Castamere"*, usada como instrumento de dissuasão psicológica sem necessidade de derramamento contínuo de sangue.
  - A articulação do **Casamento Vermelho** é a pura manifestação de *"os fins justificam os meios"*: Tywin justificou o ato argumentando que matar algumas dezenas de homens em um banquete salvou a vida de dezenas de milhares em batalha, garantindo a sobrevivência de sua dinastia.

#### 2. Petyr Baelish (Mindinho) — A Virtù Oportunista e o Caos como Escada
* **Conceito Maquiavélico:** *Virtù* pura manipulando a *Fortuna*.
* **Aplicações na Obra:**
  - Nascido sem terras influentes ou nobreza de destaque, Mindinho usa a inteligência financeira, bajulação e conspirações para subir de posição.
  - Sua máxima *"O caos não é um abismo, o caos é uma escada"* traduz a capacidade de se antecipar e aproveitar a instabilidade para expandir sua influência pessoal, sem apego a honra ou lealdades fixas.

#### 3. Varys (O Aranha) — A Razão de Estado e o Bem Coletivo
* **Conceito Maquiavélico:** A preservação do Estado acima da virtude individual.
* **Aplicações na Obra:**
  - Diferente de Mindinho, que busca o ganho próprio, Varys age explicitamente em nome do *"reino"*.
  - Ele não hesita em mudar de lealdades, conspirar assassinatos e tecer mentiras se o resultado final trouxer estabilidade institucional a Westeros, mostrando que ações moralmente questionáveis são justificadas pelo resultado político.

#### 4. Cersei Lannister — O Fracasso da Ilusão Maquiavélica
* **Conceito Maquiavélico:** Confundir crueldade com força e ser odiada em vez de temida.
* **Aplicações na Obra:**
  - Maquiavel alertou enfaticamente que o governante deve evitar a qualquer custo tornar-se **odiado e desprezado**.
  - Cersei tenta imitar o pai (Tywin), mas carece de prudência. Ao armar a Fé Militante para destruir seus rivais políticos, ela cria uma força incontrolável que se volta contra si mesma, demonstrando ausência de prudência (*virtù*) e submissão aos caprichos da *fortuna*.

---

## ⚡ Questão 4 — Endpoint com FastAPI (Item com UUID dinâmico)

### Enunciado e Especificações
> *Utilizando uma ferramenta de IA generativa, crie um endpoint com FastAPI que valide e processe a entrada de um objeto do tipo Item. Siga as especificações abaixo:*
>
> 1. **Estrutura do `Item`:**
>    - `nome`: `string` com tamanho máximo de 25 caracteres.
>    - `valor`: `float`.
>    - `data`: valor do tipo `date`, que não pode ser superior à data atual.
> 2. **Requisitos:**
>    - O endpoint deve validar os valores recebidos.
>    - Após a validação, o corpo da requisição (`Item`) deve ser retornado com um novo campo adicional: `uuid`. Este campo deve conter um identificador único gerado dinamicamente.

### Técnica Utilizada
* **Metodologia CIDI (Contexto, Instruções, Detalhes e Iterações)**

### Justificativa da Técnica
A geração de código robusto para back-end demanda precisão em tipos de dados, regras de negócio, convenções de framework (FastAPI/Pydantic) e validação de borda (ex.: data futura, limitação de caracteres). Estruturar a solicitação via **CIDI** garante que a IA entregue:
- Tipagem estrita com Pydantic v2;
- Validador personalizado (`@field_validator`) para a regra de data;
- DTOs separados para entrada (`Item`) e saída (`ItemResponse`);
- Documentação interativa Swagger/OpenAPI integrada.

### Prompt de Entrada
```text
[Contexto]
Você é um desenvolvedor Python sênior especializado em FastAPI e Pydantic. O objetivo é implementar uma API para validação e enriquecimento de dados de itens.

[Instruções]
Crie um endpoint HTTP POST utilizando o framework FastAPI que:
1. Valide a estrutura e os dados de um objeto do tipo "Item" conforme as regras fornecidas.
2. Adicione dinamicamente um identificador único universal (UUID v4) ao objeto após a validação.
3. Retorne o objeto completo processado contendo os dados originais acrescidos do campo "uuid".

[Detalhes]
Estrutura e regras de validação do Item:
- nome: string com no máximo 25 caracteres.
- valor: float.
- data: date no formato YYYY-MM-DD, com a regra de que NÃO pode ser superior à data atual (date.today()).

Requisitos técnicos adicionais:
- Utilize Pydantic (Field e field_validator) para validações automáticas e geração de erro 422 HTTP quando inválido.
- Defina o status code de sucesso como 201 (Created).
- Forneça código limpo, documentado com docstrings e compatível com uvicorn.

[Iterações]
Disponibilize também comandos de inicialização do servidor e exemplos de requisição via cURL.
```

---

## 💻 Código da Aplicação (`main.py`)

O código completo foi implementado e está pronto para execução no arquivo [`main.py`](file:///Users/joaoflavio/projetos-e-estudos/last-rocket/main.py):

```python
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
```

---

## 🛠️ Como Executar o Projeto da Questão 4 Localmente

### 1. Pré-requisitos
* Python 3.10+ (ou superior)

### 2. Ativar o Ambiente Virtual e Instalar Dependências
```bash
# Criar e ativar o ambiente virtual (já configurado neste diretório)
source .venv/bin/activate

# Instalar dependências (caso necessário)
pip install -r requirements.txt
```

### 3. Iniciar o Servidor
```bash
uvicorn main:app --reload
```

### 4. Acessar a Documentação Interativa
* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Testes de Requisição

### Exemplo de Sucesso (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Mouse Sem Fio",
    "valor": 149.90,
    "data": "2026-11-04"
  }'
```

**Resposta esperada (Status 201 Created):**
```json
{
  "nome": "Mouse Sem Fio",
  "valor": 149.90,
  "data": "2026-11-04",
  "uuid": "e932bce2-6b9a-4c28-98e3-547e8c071d1e"
}
```

### Exemplo de Erro — Nome Excedendo 25 Caracteres (Status 422)
```bash
curl -X POST "http://127.0.0.1:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "NomeMuitoLongoComMaisDeVinteECincoCaracteres",
    "valor": 50.0,
    "data": "2026-11-04"
  }'
```

### Exemplo de Erro — Data no Futuro (Status 422)
```bash
curl -X POST "http://127.0.0.1:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teclado",
    "valor": 200.0,
    "data": "2099-01-01"
  }'
```

---

## ✅ Executando os Testes Automatizados

O projeto conta com suíte de testes unitários automatizados cobrindo todos os fluxos de sucesso e exceção em [`test_main.py`](file:///Users/joaoflavio/projetos-e-estudos/last-rocket/test_main.py):

```bash
source .venv/bin/activate
pytest -v
```

**Resultado dos testes:**
```text
test_main.py::test_health_check PASSED                                   [ 20%]
test_main.py::test_criar_item_valido PASSED                              [ 40%]
test_main.py::test_criar_item_com_nome_maior_que_25_caracteres PASSED    [ 60%]
test_main.py::test_criar_item_com_data_no_futuro PASSED                  [ 80%]
test_main.py::test_criar_item_com_valor_invalido PASSED                  [100%]

========================= 5 passed in 0.36s =========================
```
