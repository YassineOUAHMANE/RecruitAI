from pipeline.rag_pipeline import RAGPipeline
from config.settings import settings
import os

def init_vector_db():
    print("🚀 Initialisation de la base vectorielle...")

    data_path = settings.DATA_PATH
    if not os.path.exists(data_path):
        raise Exception(f"❌ DATA_PATH introuvable : {data_path}")

    pipeline = RAGPipeline(base_path=data_path, vector_db="qdrant")
    pipeline.run()

    print("🎉 Vector store construit avec succès !")

if __name__ == "__main__":
    init_vector_db()
