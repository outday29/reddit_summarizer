from pydantic import BaseSettings


class AppSettings(BaseSettings):
    personal_use_script: str
    client_secret: str
    user_agent: str
    username: str
    password: str
    openai_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = AppSettings()
