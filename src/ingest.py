from dotenv import load_dotenv
from utils.env import require_env_vars
from utils.embedding import embedding_factory

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector

# Carrega as variáveis de ambiente
load_dotenv()

# Valida e recupera as variáveis de ambiente necessárias
env_vars = require_env_vars([
    "DATABASE_URL",
    "PG_VECTOR_COLLECTION_NAME",
    "PDF_PATH"
])

PDF_PATH = env_vars["PDF_PATH"]


def load_pdf(pdf_path):
    print(f"[ingest] ⏳​ Carregando o PDF: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print(f"[ingest] ✅ PDF carregado com sucesso. Total de páginas: {len(docs)}")
    return docs


def split_docs(docs):
    print(f"[ingest] ✂️​ Dividindo o PDF em partes menores para processamento...")

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    ).split_documents(docs)

    print(f"[ingest] ✅ PDF dividido em {len(splits)} partes.")
    return splits


def create_pgvector_store(embeddings):
    print(f"[ingest] ⏳​ Criando a coleção no PGVector e adicionando os documentos...")

    return PGVector(
        embeddings=embeddings,
        collection_name=env_vars["PG_VECTOR_COLLECTION_NAME"],
        connection=env_vars["DATABASE_URL"],
        use_jsonb=True,
    )

def ingest_pdf():
    print(f"[ingest] ▶️​ Iniciando ingestão do PDF")
    
    try:
        docs = load_pdf(PDF_PATH)
        splits = split_docs(docs)
        
        if not splits:
            print("⚠️​ Nenhum conteúdo encontrado no PDF para processar.")
            raise SystemExit(0)
        
        print(f"[ingest] 🔍 Enriquecendo os documentos com metadados...")
        
        embeddings = embedding_factory()
        store = create_pgvector_store(embeddings)
        store.add_documents(documents=splits)
        
        print(f"[ingest] ✅ Documentos adicionados à coleção {env_vars['PG_VECTOR_COLLECTION_NAME']} com sucesso.")
    
    except Exception as e:
        print(f"[ingest] ❌ Erro ao carregar o PDF: {str(e)}")
        raise SystemExit(1)

if __name__ == "__main__":
    ingest_pdf()