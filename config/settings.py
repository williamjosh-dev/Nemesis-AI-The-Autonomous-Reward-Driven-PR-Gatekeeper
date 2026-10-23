import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Nemesis AI Gateway"
    API_V1_STR: str = "/api/v1"
    
    # Nebius / NVIDIA Nemotron Settings
    NEBIUS_API_KEY: str = os.getenv("NEBIUS_API_KEY", "")
    NEBIUS_BASE_URL: str = os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.ai/v1/") # Replace with actual Nebius endpoint if different
    
    # GitHub Settings
    GITHUB_WEBHOOK_SECRET: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

settings = Settings()