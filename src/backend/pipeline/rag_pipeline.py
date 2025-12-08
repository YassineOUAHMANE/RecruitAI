from ingestion.parser import ResumeParser
from embeddings.embedder import Embedder
from storage.vector_store import VectorStore
import os


class RAGPipeline:

    def __init__(self, base_path="/app/data", vector_db="qdrant"):
        self.base_path = base_path
        self.vector_db = vector_db

        # Parser
        self.parser = ResumeParser(base_path=self.base_path)

        # Embedder ONNX (aucun argument !)
        self.embedder = Embedder()

        # Dimension du modèle ONNX (384 si MiniLM)
        self.store = VectorStore(type=self.vector_db, dimension=384)


    def run(self):
        print("📄 Lecture des fichiers CV...")
        data = self.parser.parse()

        print(f"Extraction terminée : {len(data)} CVs trouvés.")

        batch_size = 200  # ← Taille raisonnable
        all_vectors = []

        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            texts = [item["text"] for item in batch]

            print(f"🔢 Encodage batch {i} → {i+len(batch)}...")
            vectors = self.embedder.encodeBatch(texts)

            print("💾 Insertion dans Qdrant...")
            self.store.add_vectors(batch, vectors)

        print("🎉 Vector store construit avec succès !")

