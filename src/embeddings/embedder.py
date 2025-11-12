from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config.settings import settings


class Embedder():
    def __init__(self, model_embedding = "all-MiniLM-L6-v2"):
        self.model_embedding = model_embedding
        self.sentence_transformer = SentenceTransformer(self.model_embedding)
        self.qdrant_client = QdrantClient(host= settings.QDRANT_HOST, port= settings.QDRANT_PORT)

    
    def encodeText(self, text):
        embedded_text = self.sentence_transformer.encode(text, convert_to_numpy = True)
        return embedded_text

    def encodeBatch(self, texts):
        embedded_texts = self.sentence_transformer.encode(texts, convert_to_numpy = True)
        return embedded_texts
