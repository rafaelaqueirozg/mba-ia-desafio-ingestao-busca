from utils.env import require_env_vars

from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def embedding_factory():
    envs = require_env_vars(["MODEL_PROVIDER"])
    provider = envs["MODEL_PROVIDER"].lower()
    
    match provider:
        case "gemini":
            gemini_vars = require_env_vars([
                "GOOGLE_API_KEY",
                "GOOGLE_EMBEDDING_MODEL"
            ])

            return GoogleGenerativeAIEmbeddings(
                model=gemini_vars["GOOGLE_EMBEDDING_MODEL"],
                google_api_key=gemini_vars["GOOGLE_API_KEY"]
            )

        case "openai":
            openai_vars = require_env_vars([
                "OPENAI_API_KEY",
                "OPENAI_EMBEDDING_MODEL"
            ])

            return OpenAIEmbeddings(
                model=openai_vars["OPENAI_EMBEDDING_MODEL"]
            )

        case _:
            raise ValueError(f"MODEL_PROVIDER não suportado: {provider}")