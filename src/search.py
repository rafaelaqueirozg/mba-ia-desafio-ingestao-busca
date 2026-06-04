from dotenv import load_dotenv
from utils.env import require_env_vars
from utils.embedding import embedding_factory
from utils.llm import llm_factory

from langchain_postgres import PGVector

# Carrega as variáveis de ambiente
load_dotenv()

# Valida e recupera as variáveis de ambiente necessárias
env_vars = require_env_vars([
    "DATABASE_URL",
    "PG_VECTOR_COLLECTION_NAME"
])

# Template de prompt para a busca
PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_context(results):
    print(f"[search] ⏳​ Construindo o contexto para a resposta...")

    docs = []
    for item, (doc) in results:
        doc = item.page_content.strip()
        
        if doc:
            docs.append(doc)

    return "\n\n---\n\n".join(docs)

def search_prompt(question=None):
    print(f"[search] ▶️​ Iniciando processo de busca e resposta...")
    
    try:
        embeddings = embedding_factory()
        
        store = PGVector(
            embeddings=embeddings,
            collection_name=env_vars["PG_VECTOR_COLLECTION_NAME"],
            connection=env_vars["DATABASE_URL"],
            use_jsonb=True,
        )
        
        print(f"[search] 🔍 Realizando busca por similaridade no PGVector...")
        
        results = store.similarity_search_with_score(question, k=10)
        
        if not results:
            print(f"[search] ⚠️​ Nenhum resultado encontrado para a pergunta: {question}")
            return "Não tenho informações necessárias para responder sua pergunta."
        
        context = get_context(results)
        
        query = PROMPT_TEMPLATE.format(contexto=context, pergunta=question)
        
        llm = llm_factory()
        
        response = llm.invoke(query)
        print(f"[search] ✅ Resposta gerada com sucesso.")
        
        return response.content
    
    except Exception as e:
        print(f"[search] ❌ Erro durante o processo de busca: {str(e)}")
        raise SystemExit(1)