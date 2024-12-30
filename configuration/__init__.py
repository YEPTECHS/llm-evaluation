from pydantic_settings import BaseSettings

from .global_config import GlobalConfig


class Config(BaseSettings):
    global_config: GlobalConfig = GlobalConfig()


config = Config()
