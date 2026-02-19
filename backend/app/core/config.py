from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret_key:str
    database_url:str
    access_token_expiry_minutes:int=30
    jwt_algorithm:str='HS256'

    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()