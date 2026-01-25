from ml_pipeline.ingestion.parser import ResumeParser
from ml_pipeline.embeddings.embedder import Embedder
from ml_pipeline.storage.vector_store import VectorStore

from backend.config import get_db
from backend.dao.files_dao import FilesDAO
class RAGPipeline:

    def __init__(self, base_path="/app/data", vector_db="qdrant"):
        self.base_path = base_path
        self.vector_db = vector_db
        self.files_dao = FilesDAO(get_db)   

        self.parser = ResumeParser(base_path=self.base_path)
        self.embedder = Embedder()
        self.store = VectorStore(type=self.vector_db, dimension=384)

    def run(self):
        data = self.parser.parse()

        texts = [item["text"] for item in data]
        vectors = self.embedder.encodeBatch(texts)

        self.store.add_vectors(data, vectors)

    def add_file(self,id,path):
        data = self.parser.parse_one(id,path)

        text = [data["text"]]
        vectors = self.embedder.encodeBatch(text)

        self.store.add_vector(data, vectors[0])


    