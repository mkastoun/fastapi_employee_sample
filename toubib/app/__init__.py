from os import getenv

from dotenv import load_dotenv

from toubib.app.core.config import Settings

"""
The loading of the .env to settings on the application initialisation
"""
load_dotenv(getenv("ENV_FILE"))

settings = Settings()
