from pathlib import Path
import joblib

from ml_pipeline.ingestion.parser import ResumeParser
from ml_pipeline.embeddings.embedder import Embedder
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from ml_pipeline.config.settings import settings


class SingleCVIngestor:

    def __init__(self):
        self.parser = ResumeParser()
        self.embedder = Embedder()

        models_dir = Path("/app/backend/models")  
        
        self.clf = joblib.load(models_dir / "svm.joblib")
        self.vectorizer = joblib.load(models_dir / "tfidf.joblib")
        self.encoder = joblib.load(models_dir / "labels.joblib")

        print("Modèle TF-IDF + SVM chargé")

        # -------- Qdrant client --------
        self.qdrant = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            prefer_grpc=True,
            grpc_port=settings.QDRANT_GRPC_PORT
        )

    def _predict_category(self, text: str) -> str:

        text = (text or "").lower().strip()
        if not text:
            return "UNKNOWN"

        X = self.vectorizer.transform([text])
        pred = self.clf.predict(X)[0]
        return self.encoder.inverse_transform([pred])[0]

    def ingest_one(self, file_id: int, pdf_path: str):

        parsed = self.parser.parse_one(file_id, pdf_path)
        if parsed is None or not parsed["text"]:
            print(f"Aucun texte détecté dans {pdf_path}")
            return False

        text = parsed["text"]

        category = self._predict_category(text)

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

        print(f"CV {file_id} inséré dans Qdrant | category={category}")
        return True
