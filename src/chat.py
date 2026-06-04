from search import search_prompt

def main():
    print("=" * 100)
    print("Desafio RAG - Ingestão e Busca")
    print("=" * 100)
    print("Digite 'sair' para encerrar")
    print("=" * 100)
    
    print(f"\n[chat] ▶️ Iniciando o sistema")
    
    while True:
        try:
            question = input("\nFaça sua pergunta: ").strip()
            
            if question.lower() in ["sair", "exit", "quit"]:
                print("[chat] 👋 Encerrando o sistema. Até mais!")
                break
            
            if not question:
                print("[chat] ⚠️ Por favor, digite uma pergunta válida.")
                continue
            
            print("[chat] ⏳ Processando...")
          
            response = search_prompt(question)
            
            print(f"\n{'=' * 50}")
            print(f"PERGUNTA: {question}")
            print("=" * 50)
            print(f"RESPOSTA:\n{response}")
            print("=" * 50)
            
        except Exception as e:
            print(f"[chat] ❌ Ocorreu um erro: {str(e)}")
            print("[chat] Tente novamente.")

if __name__ == "__main__":
    main()