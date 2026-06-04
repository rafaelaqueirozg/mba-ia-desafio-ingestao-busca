import os

# Função para validar a presença de variáveis de ambiente necessárias e retornar seus valores
def require_env_vars(required_vars: list[str]) -> dict[str, str]:
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing_vars)}"
        )

    return {var: os.environ[var] for var in required_vars}