from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    chat_model: str = "gemma-3-1b"
    embedding_model: str = "nomic-embed-text-v1.5"


settings = Settings()
