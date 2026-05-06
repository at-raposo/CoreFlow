from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CoreFlow API"
    VERSION: str = "0.1.0"
    DATABASE_URL: str = "postgresql://user:password@localhost/coreflow"
    
    GEMINI_API_KEY: Optional[str] = None
    QC_EMAIL: Optional[str] = None
    QC_PASSWORD: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
