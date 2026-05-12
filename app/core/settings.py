import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Default to local Ollama, can be overridden via .env
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-oss-20b")
    LAB_2_MODEL_PATH: str = os.getenv("LAB_2_MODEL_PATH", "./models/intent_model/checkpoint-157")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    class Config:
        env_file = ".env"

settings = Settings()

# Validate Ollama connection at startup
print(f"📡 Ollama URL configured: {settings.OLLAMA_BASE_URL}")
print(f"🤖 Model: {settings.MODEL_NAME}")
print(f"📁 Intent Model Path: {settings.LAB_2_MODEL_PATH}")
