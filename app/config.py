from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    database_username: str
    database_password: str
    database_host: str
    database_port: int  # because of URL builder from SQLAlchemy
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()