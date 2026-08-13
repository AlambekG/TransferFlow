from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/transferflow"

	class Config:
		env_prefix = ""
		env_file = ".env"

settings = Settings()
