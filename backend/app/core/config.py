from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://gymadmin:123456@localhost:5432/gym_db"
    SECRET_KEY: str = "cuonghackerman2026_gym_management_system_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    PROJECT_NAME: str = "Gym Management System"
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()