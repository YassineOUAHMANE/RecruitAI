from ingestion.parser import ResumeParser
from embeddings.embedder import Embedder
from storage.vector_store import VectorStore


class RAGPipeline:

    def __init__(self, base_path="/home/moussaoui/langchain-chatbot/data/data", model_name="all-MiniLM-L6-v2", vector_db="qdrant"):
        self.base_path = base_path
        self.model_name = model_name
        self.vector_db = vector_db

        self.parser = ResumeParser(base_path=self.base_path)
        self.embedder = Embedder(model_embedding=self.model_name)
        self.store = VectorStore(type=self.vector_db, dimension=384)

    def run(self):
        data = self.parser.parse()

        texts = [item["text"] for item in data]
        vectors = self.embedder.encodeBach(texts)

        self.store.add_vectors(data, vectors)


    