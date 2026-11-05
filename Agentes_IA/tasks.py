from crewai import Task


def create_script_task(agent) -> Task:
    """Tarefa 1: Pesquisar e escrever o roteiro de vídeo."""
    return Task(
        description=(
            "1. Pesquise detalhadamente sobre o tema: '{query}' utilizando as ferramentas de busca disponíveis.\n"
            "2. Identifique os jogos mais aclamados, relevantes e premiados relacionados ao tema (incluindo The Last of Us Part II, Hades, Ghost of Tsushima, Animal Crossing: New Horizons, Doom Eternal).\n"
            "3. Estruture um roteiro completo para um vídeo no YouTube (8 a 12 minutos) dividido em:\n"
            "   - [INTRODUÇÃO & HOOK]: Gancho impactante nos primeiros 30 segundos, contexto do ano e por que ele foi inesquecível.\n"
            "   - [DESENVOLVIMENTO]: Análise profunda de cada um dos principais jogos, com detalhes de jogabilidade, impacto emocional, narrativa e sugestões de cenas/B-Roll.\n"
            "   - [CONCLUSÃO & CTA]: Reflexão sobre o legado desses jogos e chamada forte para inscrição, curtida e debate nos comentários."
        ),
        expected_output=(
            "Um roteiro completo em formato Markdown, altamente dinâmico, com marcações de locução [FALA], "
            "efeitos sonoros [SFX] e direção visual de tela [TELA/B-ROLL]."
        ),
        agent=agent,
    )


def create_thumbnail_task(agent, context_tasks=None) -> Task:
    """Tarefa 2: Produzir 3 opções de thumbnails e prompts visuais."""
    return Task(
        description=(
            "Com base no roteiro gerado para '{query}', crie exatamente 3 OPÇÕES DISTINTAS de thumbnails para o YouTube, "
            "planejadas para obter a mais alta taxa de clique (CTR):\n"
            "- Opção 1: Foco em Ação Épica e Confronto Mitológico/Combate (ex.: Zagreus em Hades ou Doom Slayer).\n"
            "- Opção 2: Foco em Narrativa Dramática e Expressão Emocional (ex.: Ellie em The Last of Us Part II).\n"
            "- Opção 3: Foco em Contraste Cultural / Mistura de Mundos (ex.: Acalento de Animal Crossing vs Honra Samurai de Ghost of Tsushima).\n\n"
            "Para CADA UMA das 3 opções, forneça:\n"
            "1. Título do Conceito\n"
            "2. Descrição Visual Detalhada (composição, personagens, expressão facial, iluminação e fundo)\n"
            "3. Cores Predominantes e Contraste\n"
            "4. Texto de Destaque na Thumbnail (máximo 3 a 4 palavras de forte impacto)\n"
            "5. Prompt em Inglês para geração de imagem com DALL-E 3 / Midjourney."
        ),
        expected_output=(
            "Documento estruturado em Markdown com as 3 opções completas de thumbnails, "
            "incluindo especificações visuais, teoria de cores e prompts para DALL-E 3."
        ),
        agent=agent,
        context=context_tasks or [],
    )


def create_review_task(agent, context_tasks=None) -> Task:
    """Tarefa 3: Revisar o roteiro, escolher a melhor thumbnail e gerar a versão final unificada."""
    return Task(
        description=(
            "1. Revise minuciosamente o texto do roteiro sobre '{query}', refinando o ritmo (pacing), fluidez verbal e apelo para retenção de audiência no YouTube.\n"
            "2. Analise criticamente as 3 opções de thumbnails criadas pelo designer.\n"
            "3. ESCOLHA UMA DESSAS THUMBNAILS como a principal (vencedora) e justifique a escolha com base em psicologia visual e estimativa de CTR.\n"
            "4. Produza o documento final integrado contendo:\n"
            "   - 3 Sugestões de Títulos Chamativos para o YouTube (otimizados para SEO e cliques);\n"
            "   - A Thumbnail Escolhida em Destaque com justificativa detalhada;\n"
            "   - As 2 Opções Alternativas de Thumbnails;\n"
            "   - O Roteiro Completo Revisado pronto para gravação."
        ),
        expected_output=(
            "Documento Markdown final unificado contendo sugestões de títulos para o YouTube, "
            "a thumbnail escolhida com justificativa, as opções alternativas e o roteiro completo revisado."
        ),
        agent=agent,
        context=context_tasks or [],
    )
