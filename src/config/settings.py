
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_PORT = os.getenv("QDRANT_PORT")
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")

settings = Settings()