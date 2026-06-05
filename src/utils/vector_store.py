from dotenv import load_dotenv
from utils.embedding import embedding_factory
from utils.env import require_env_vars

from langchain_postgres import PGVector

load_dotenv()

def create_pgvector_store(embeddings=None) -> PGVector:
    env_vars = require_env_vars([
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
    ])

    if embeddings is None:
        embeddings = embedding_factory()

    return PGVector(
        embeddings=embeddings,
        collection_name=env_vars["PG_VECTOR_COLLECTION_NAME"],
        connection=env_vars["DATABASE_URL"],
        use_jsonb=True,
    )