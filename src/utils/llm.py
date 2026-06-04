from utils.env import require_env_vars

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

def llm_factory():
    envs = require_env_vars(["MODEL_PROVIDER"])
    provider = envs["MODEL_PROVIDER"].lower()

    match provider:
        case "gemini":
            gemini_vars = require_env_vars([
                "GOOGLE_API_KEY",
                "GOOGLE_CHAT_MODEL"
            ])

            return ChatGoogleGenerativeAI(
                model=gemini_vars["GOOGLE_CHAT_MODEL"]
            )

        case "openai":
            openai_vars = require_env_vars([
                "OPENAI_API_KEY",
                "OPENAI_CHAT_MODEL"
            ])

            return ChatOpenAI(
                model=openai_vars["OPENAI_CHAT_MODEL"]
            )

        case _:
            raise ValueError(
                f"MODEL_PROVIDER não suportado: '{provider}'. "
                "Providers suportados: gemini, openai"
            )