from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/transferflow"

	# Redis settings
	redis_host: str = "redis"
	redis_port: int = 6379
	redis_ttl: int = 300

	# Retry behaviour defaults for external calls
	retry_retries: int = 3
	retry_delay: float = 0.5

	# Mock/delay defaults used by demo external services
	mock_delay: float = 0.3

	# Cache key prefix
	cache_prefix: str = "client"

	class Config:
		env_prefix = ""
		env_file = ".env"

settings = Settings()
