#central place for all app settings
'''
Things that change per environment:
DATABASE_URL
SECRET_KEY
TOKEN_EXPIRY_MINUTES


JWT algorithm
token expiry


App constants
Anything global:
project name
API prefix
debug mode
'''
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret_key:str
    database_url:str
    access_token_expiry_minutes:int=30
    jwt_algorithm:str='HS256'

    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
    
# important -> In your current code, jwt_secret_key will not automatically find JWT_SECRET_KEY unless they are almost identical in name. Pydantic's default matching is case-insensitive, but it cannot guess "shorthand" or entirely different names.
#if we have differnet names, we can use-> jwt_secret_key: str | None = Field(None, validation_alias="SECRET_KEY_FOR_JWT")


