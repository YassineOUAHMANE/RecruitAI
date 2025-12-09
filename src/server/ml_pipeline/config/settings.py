from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = os.getenv("QDRANT_PORT", 6333)
    QDRANT_GRPC_PORT = os.getenv("QDRANT_GRPC_PORT", 6334)
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ResumeVectorBase")
    DATA_PATH = os.getenv("DATA_PATH")

settings = Settings()