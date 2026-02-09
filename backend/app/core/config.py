from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/tableorder"
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 16
    aws_s3_bucket: str = "table-order-images"
    aws_region: str = "ap-northeast-2"
    debug: bool = True
    cors_origins: str = "*"

    class Config:
        env_file = ".env"


settings = Settings()
