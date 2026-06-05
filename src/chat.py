from search import search_prompt


def render_header():
    print("=" * 100)
    print("Desafio RAG - Ingestão e Busca")
    print("=" * 100)
    print("Digite 'sair' para encerrar")
    print("=" * 100)


def exit_requested(question):
    return question.lower() in ["sair", "exit", "quit"]


def display_response(question, response):
    print(f"\n{'=' * 100}")
    print(f"PERGUNTA: {question}")
    print("=" * 100)
    print(f"RESPOSTA:\n{response}")
    print("=" * 100)


def main():
    render_header()

    print(f"\n[chat] ▶️ Iniciando o sistema")
    
    while True:
        try:
            question = input("\n[chat] Digite sua pergunta (ou 'sair' para encerrar): ").strip()
            
            if exit_requested(question):
                print("[chat] 👋 Encerrando o sistema. Até mais!")
                break
            
            if not question:
                print("[chat] ⚠️ Por favor, digite uma pergunta válida.")
                continue
            
            print("[chat] ⏳ Processando...")
          
            response = search_prompt(question)
            display_response(question, response)
            
        except Exception as e:
            print(f"[chat] ❌ Ocorreu um erro: {str(e)}")
            print("[chat] Tente novamente.")

if __name__ == "__main__":
    main()