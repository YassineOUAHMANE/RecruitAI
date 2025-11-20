from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
    QDRANT_GRPC_PORT = int(os.getenv("QDRANT_GRPC_PORT", 6334))
    QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "ResumeVectorBase")
    DATA_PATH = os.getenv("DATA_PATH")
    CLASSIFIER_PATH = os.getenv("CLASSIFIER_PATH", "src/classification/models/classifier.pkl")

    def get(self, key: str, default=None):
        """Get configuration value dynamically."""
        return getattr(self, key, default)

settings = Settings()
