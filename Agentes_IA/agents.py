import os
from crewai import Agent, LLM
from tools import game_search_tool, thumbnail_visual_planner


def get_default_llm():
    """Configura e retorna a LLM padrão com base no ambiente."""
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    if api_key and not api_key.startswith("sua_chave"):
        return LLM(model=model, api_key=api_key)
    return None


def create_video_scriptwriter(llm=None) -> Agent:
    """Agente 1: Roteirista de Vídeo."""
    return Agent(
        role="Roteirista de Vídeo Especialista em Games",
        goal="Pesquisar e elaborar um roteiro detalhado, estruturado e completo para o YouTube sobre o tema: {query}",
        backstory=(
            "Você é um roteirista sênior do YouTube especializado na indústria de videogames e storytelling de entretenimento. "
            "Você domina ganchos de retenção nos primeiros 30 segundos, ritmo narrativo envolvente, contextualização histórica "
            "e análises aprofundadas de gameplay, enredo e impacto cultural dos jogos. "
            "Você utiliza ferramentas de pesquisa para embasar seu roteiro com dados confiáveis, premiações e opiniões da comunidade gamer."
        ),
        tools=[game_search_tool],
        llm=llm or get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_thumbnail_creator(llm=None) -> Agent:
    """Agente 2: Criador de Thumbnails."""
    return Agent(
        role="Criador de Thumbnails e Designer Visual para YouTube",
        goal="Criar três opções distintas e chamativas de thumbnails inspiradas no roteiro de {query}, maximizando a taxa de clique (CTR)",
        backstory=(
            "Você é um designer gráfico sênior e diretor de arte especializado em miniaturas para canais de games no YouTube. "
            "Você compreende a psicologia das cores, o valor do contraste dramático, expressões faciais marcantes e a regra dos terços. "
            "Seu trabalho é transformar os momentos mais emocionantes e visuais do roteiro em 3 conceitos conceituais de thumbnails "
            "com prompts detalhados para ferramentas de geração de imagem como DALL-E e Midjourney."
        ),
        tools=[thumbnail_visual_planner],
        llm=llm or get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_reviewer(llm=None) -> Agent:
    """Agente 3: Revisor e Produtor Executivo de Conteúdo."""
    return Agent(
        role="Revisor e Produtor Executivo de Conteúdo",
        goal="Revisar o texto do roteiro de {query}, escolher a melhor thumbnail com justificativa de CTR e compilar a versão final com roteiro + thumbnails",
        backstory=(
            "Você é o editor-chefe de um canal de sucesso de games. Você é implacável com a clareza, coerência e dinamismo do texto, "
            "garantindo que o roteiro soe natural quando lido em voz alta pelo apresentador. "
            "Você analisa criticamente as três opções de thumbnails geradas pelo designer, seleciona a campeã com base no apelo ao público gamer "
            "e entrega o documento final unificado em Markdown de alta qualidade."
        ),
        tools=[],
        llm=llm or get_default_llm(),
        verbose=True,
        allow_delegation=False,
    )

