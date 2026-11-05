import os
import sys
import argparse
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

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
from generator import generate_demo_output


def build_crew():
    """Constrói a equipe CrewAI com os 3 agentes e 3 tarefas configuradas."""
    from crewai import Crew, Process

    scriptwriter = create_video_scriptwriter()
    thumbnail_creator = create_thumbnail_creator()
    reviewer = create_reviewer()

    task_script = create_script_task(scriptwriter)
    task_thumbnail = create_thumbnail_task(thumbnail_creator, context_tasks=[task_script])
    task_review = create_review_task(reviewer, context_tasks=[task_script, task_thumbnail])

    crew = Crew(
        agents=[scriptwriter, thumbnail_creator, reviewer],
        tasks=[task_script, task_thumbnail, task_review],
        verbose=True,
        process=Process.sequential,
    )
    return crew


def execute_pipeline(query: str = "Melhores jogos de 2020", force_demo: bool = False) -> str:
    """
    Executa o pipeline completo de agentes.
    Se a OPENAI_API_KEY estiver configurada e force_demo for False, utiliza o CrewAI com a API.
    Caso contrário, executa em modo demonstrativo com o gerador estruturado.
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    use_live_api = bool(openai_key and not openai_key.startswith("sua_chave") and not force_demo)

    print("\n" + "=" * 60)
    print("🎮 SISTEMA DE AGENTES IA — ROTEIROS & THUMBNAILS DE GAMES")
    print(f"📌 Tema selecionado: '{query}'")
    print(f"⚙️  Modo de execução: {'CrewAI Live API' if use_live_api else 'Modo Demonstrativo Resiliente'}")
    print("=" * 60 + "\n")

    if use_live_api:
        try:
            print("🚀 Iniciando execução com a Crew de Agentes...")
            crew = build_crew()
            result = crew.kickoff(inputs={"query": query})
            final_content = str(result)
        except Exception as e:
            print(f"⚠️  Aviso: Erro ao executar via API externa ({e}).")
            print("🔄 Ativando modo de geração demonstrativa de alta qualidade...")
            final_content = generate_demo_output(query)
    else:
        print("ℹ️  Executando agentes e gerando roteiro estruturado com thumbnails...")
        final_content = generate_demo_output(query)

    output_path = os.path.join(os.path.dirname(__file__), "roteiro_final.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"\n✅ Concluído com sucesso! Arquivo gerado em: {output_path}\n")
    return final_content


def main():
    parser = argparse.ArgumentParser(description="Sistema de Agentes IA para Geração de Roteiros e Thumbnails de Games")
    parser.add_argument("--query", "-q", type=str, default="Melhores jogos de 2020", help="Tema do vídeo no YouTube")
    parser.add_argument("--demo", action="store_true", help="Força a execução no modo demonstrativo sem chamada de API")

    args = parser.parse_args()
    content = execute_pipeline(query=args.query, force_demo=args.demo)
    # Exibe resumo do resultado no terminal
    print("--- PRÉVIA DO RESULTADO GERADO ---")
    lines = content.strip().split("\n")
    print("\n".join(lines[:35]))
    if len(lines) > 35:
        print(f"\n... [{len(lines) - 35} linhas adicionais salvas em roteiro_final.md] ...")


if __name__ == "__main__":
    main()

