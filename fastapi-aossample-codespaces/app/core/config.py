from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "fastapi-aossample")
    env: str = os.getenv("APP_ENV", "dev")
    debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

settings = Settings()
