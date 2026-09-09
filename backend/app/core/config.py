from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = ""
    TRIBUTE_TOKEN: str = ""
    ADMIN_ID: int = 8707664475

    class Config:
        env_file = ".env"


settings = Settings()
