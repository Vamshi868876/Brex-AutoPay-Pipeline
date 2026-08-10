from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Brex Settings
    BREX_USER_TOKEN: str = "your_brex_user_token_here"
    BREX_BASE_URL: str = "https://platform.brexapis.com"
    TEST_MODE: bool = False
    
    # Gmail Settings
    EMAIL_ACCOUNT: str = ""
    EMAIL_PASSWORD: str = ""
    
    # AI Settings
    OPENAI_API_KEY: str = ""
    
    # Database Settings
    DATABASE_URL: str = "postgresql://admin:adminpassword@localhost:5432/brex_autopay"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
