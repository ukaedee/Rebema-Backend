from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 環境設定
    ENVIRONMENT: str = "development"  # デフォルトは開発モード

    # JWT設定
    SECRET_KEY: str  # 必須
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24時間

    # データベース設定
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_SSL_MODE: str
    DATABASE_URL: Optional[str] = None

    # Azure Storage設定
    AZURE_STORAGE_CONNECTION_STRING: str
    AZURE_STORAGE_CONTAINER_NAME: str

    class Config:
        env_file = ".env"
        case_sensitive = False  # 環境変数名の大文字小文字を区別しない

settings = Settings() 