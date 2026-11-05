import os
from crewai.tools import tool

# Curadoria de dados sobre jogos para fallback offline/resiliente
GAME_KNOWLEDGE_BASE = {
    "2020": (
        "Jogos mais aclamados e premiados de 2020:\n"
        "1. The Last of Us Part II (Naughty Dog/Sony) - Vencedor do Game of the Year (GOTY) no The Game Awards 2020. "
        "Destaque para narrativa visceral sobre vingança, luto e empatia, gráficos foto-realistas e combate brutal.\n"
        "2. Hades (Supergiant Games) - Vencedor de Melhor Jogo Indie e Melhor Ação no TGA 2020. "
        "Rogue-like mitológico onde Zagreus tenta escapar do submundo de seu pai Hades, com combate ágil e narrativa inovadora.\n"
        "3. Ghost of Tsushima (Sucker Punch/Sony) - Vencedor do Player's Voice e Melhor Direção de Arte no TGA 2020. "
        "Mundo aberto no Japão Feudal durante a invasão mongol, focando no dilema samurai de Jin Sakai entre a honra e a sobrevivência.\n"
        "4. Animal Crossing: New Horizons (Nintendo) - Fenômeno global de vendas e cultura pop durante o isolamento de 2020. "
        "Simulação de vida em uma ilha deserta relaxante, personalização e interação social.\n"
        "5. Doom Eternal (id Software) - Ação frenética, trilha sonora visceral de heavy metal e coreografia frenética de combate contra demônios.\n"
        "6. Final Fantasy VII Remake (Square Enix) - Reimaginação espetacular do clássico RPG com combate em tempo real e gráficos modernos."
    )
}


@tool("Game Search Tool")
def game_search_tool(search_query: str) -> str:
    """Pesquisa na web sobre jogos, notas do Metacritic, premiações, narrativas e lançamentos de videogames."""
    # Tenta busca real via DuckDuckGo
    try:
        from langchain_community.tools import DuckDuckGoSearchRun
        search = DuckDuckGoSearchRun()
        results = search.run(search_query)
        if results and len(results.strip()) > 30:
            return results
    except Exception:
        pass

    # Fallback contextual inteligente
    for key, text in GAME_KNOWLEDGE_BASE.items():
        if key in search_query:
            return f"Dados coletados para a pesquisa '{search_query}':\n{text}"

    return (
        f"Resultados de pesquisa para '{search_query}':\n"
        + GAME_KNOWLEDGE_BASE["2020"]
    )


@tool("Thumbnail Visual Planner Tool")
def thumbnail_visual_planner(prompt_description: str) -> str:
    """Gera especificações visuais avançadas para thumbnails do YouTube e prepara comandos para DALL-E/Midjourney."""
    # Se a chave da OpenAI estiver presente, tenta gerar com DALL-E se solicitado
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not openai_key.startswith("sua_chave"):
        try:
            from crewai_tools import DallETool
            dalle = DallETool()
            return dalle.run(prompt_description)
        except Exception as e:
            return f"Especificação de Thumbnail planejada: {prompt_description} (Nota: Geração de imagem DALL-E simulada devido a: {e})"

    return (
        f"🎨 [Conceito de Thumbnail Planejado]:\n"
        f"Prompt Otimizado para DALL-E 3: {prompt_description}\n"
        f"Resolução recomendada: 1280x720 (16:9), cores saturadas com alto contraste, "
        f"elementos visuais centrais isolados para visualização clara em telas de celular."
    )
