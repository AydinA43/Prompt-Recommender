from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    AWS_ACCESS_KEY_ID: str = None
    AWS_SECRET_ACCESS_KEY: str = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = None

    class Config:
        env_file = ".env"

settings = Settings()