import os
import pytest
from agents import (
    create_video_scriptwriter,
    create_thumbnail_creator,
    create_reviewer,
)
from tasks import (
    create_script_task,
    create_thumbnail_task,
    create_review_task,
)
from tools import game_search_tool, thumbnail_visual_planner
from main import build_crew, execute_pipeline


def test_game_search_tool():
    """Testa se a ferramenta de busca de jogos retorna dados consistentes."""
    result = game_search_tool.run("Melhores jogos de 2020")
    assert result is not None
    assert len(result) > 50
    assert "Hades" in result or "Last of Us" in result or "Animal Crossing" in result


def test_thumbnail_visual_planner_tool():
    """Testa a ferramenta de planejamento de thumbnail."""
    result = thumbnail_visual_planner.run("Guerreiro mitológico com espada em chamas")
    assert result is not None
    assert "DALL-E" in result or "Thumbnail" in result


def test_agents_creation():
    """Testa a criação e os papéis dos 3 agentes definidos no desafio."""
    scriptwriter = create_video_scriptwriter()
    thumbnail_creator = create_thumbnail_creator()
    reviewer = create_reviewer()

    assert scriptwriter.role == "Roteirista de Vídeo Especialista em Games"
    assert thumbnail_creator.role == "Criador de Thumbnails e Designer Visual para YouTube"
    assert reviewer.role == "Revisor e Produtor Executivo de Conteúdo"

    assert len(scriptwriter.tools) >= 1
    assert len(thumbnail_creator.tools) >= 1


def test_tasks_creation():
    """Testa a criação das tarefas e vínculo com os agentes."""
    scriptwriter = create_video_scriptwriter()
    thumbnail_creator = create_thumbnail_creator()
    reviewer = create_reviewer()

    task1 = create_script_task(scriptwriter)
    task2 = create_thumbnail_task(thumbnail_creator, context_tasks=[task1])
    task3 = create_review_task(reviewer, context_tasks=[task1, task2])

    assert task1.agent == scriptwriter
    assert task2.agent == thumbnail_creator
    assert task3.agent == reviewer
    assert len(task2.context) == 1
    assert len(task3.context) == 2


def test_build_crew():
    """Testa se a Crew é montada com 3 agentes e 3 tarefas."""
    crew = build_crew()
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3


def test_pipeline_execution():
    """Testa a execução do pipeline e a geração do arquivo final markdown."""
    query = "Melhores jogos de 2020"
    content = execute_pipeline(query=query, force_demo=True)
    assert content is not None
    assert "Hades" in content
    assert "Animal Crossing" in content
    assert "The Last of Us" in content
    assert "Thumbnails" in content

    output_path = os.path.join(os.path.dirname(__file__), "roteiro_final.md")
    assert os.path.exists(output_path)
    with open(output_path, "r", encoding="utf-8") as f:
        saved_content = f.read()
    assert len(saved_content) > 500
