from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    To read the .env variable with Settings declaration
    """
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    db_connection_str: str
