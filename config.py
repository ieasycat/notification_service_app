from pydantic import BaseSettings
import pytz


class Config(BaseSettings):
    DEBUG: bool
    SECRET_KEY: str
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    CELERY_URL: str
    TIME_ZONES: tuple = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    URL: str
    TOKEN: str

    class Config:
        env_file = '.env'

CONFIG = Config()
