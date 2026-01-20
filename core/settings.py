from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_url: str = "http://localhost:8000"
    database_url: str = "postgresql+psycopg2://app:app@localhost:5432/app"
    app_username: str = "demo"
    app_password: str = "demo"

settings = Settings()
