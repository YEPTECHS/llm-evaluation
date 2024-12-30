from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    """
    A class to store global configuration parameters.

    Attributes:
        conversationProcessLimit: An integer representing the maximum number of conversations
        to process in a single run of the conversation processing pipeline.
    """

    conversationProcessLimit: int = 50
