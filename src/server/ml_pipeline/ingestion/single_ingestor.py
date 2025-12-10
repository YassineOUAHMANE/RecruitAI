from ml_pipeline.ingestion.parser import ResumeParser
from ml_pipeline.embeddings.embedder import Embedder
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from ml_pipeline.config.settings import settings


class SingleCVIngestor:

    def __init__(self):
        self.parser = ResumeParser()
        self.embedder = Embedder()

        # Qdrant client
        self.qdrant = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            prefer_grpc=True,
            grpc_port=settings.QDRANT_GRPC_PORT
        )

    def ingest_one(self, file_id: int, pdf_path: str):

        parsed = self.parser.parse_one(file_id, pdf_path)
        if parsed is None or not parsed["text"]:
            print(f"Aucun texte détecté dans {pdf_path}")
            return False

        text = parsed["text"]
        category = "unkown"

        vector = self.embedder.encodeText(text).astype(float).tolist()

        point = PointStruct(
            id=file_id,  
            vector=vector,
            payload={
                "file_id": file_id,
                "category": category,
                "text": text
            }
        )

        self.qdrant.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[point]
        )

        print(f"CV {file_id} inséré dans Qdrant.")
        return True
