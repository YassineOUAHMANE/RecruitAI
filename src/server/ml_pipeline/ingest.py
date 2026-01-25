import os
from pathlib import Path
from PyPDF2 import PdfReader

from backend.config import get_db
from backend.dao.files_dao import FilesDAO
from ml_pipeline.embeddings.embedder import Embedder
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from ml_pipeline.config.settings import settings




DATA_PATH = settings.DATA_PATH


def extract_text(pdf_path):
    try:
        reader = PdfReader(str(pdf_path))
        text = " ".join([page.extract_text() or "" for page in reader.pages])
        return text.strip()
    except:
        print(f"Erreur lecture PDF : {pdf_path}")
        return ""

from qdrant_client.models import VectorParams

def ingest():
    print("Démarrage de l’ingestion...")
    base = Path(DATA_PATH)

    files_dao = FilesDAO(get_db)
    files_dao.get(1)
    embedder = Embedder()

    qdrant = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
        prefer_grpc=True,
        grpc_port=settings.QDRANT_GRPC_PORT
    )
    
    
    
    
    

    if qdrant.collection_exists(settings.QDRANT_COLLECTION):
        print("Collection déjà existante → STOP (pas d’ingestion)")
        return

    print("Collection inexistante → création...")
    qdrant.create_collection(
        collection_name=settings.QDRANT_COLLECTION,
        vectors_config=VectorParams(size=384, distance="Cosine")
    )

    points = []
    counter = 0

    for category_dir in sorted(base.iterdir()):
        if not category_dir.is_dir():
            continue

        category = category_dir.name.upper()
        print(f" Catégorie : {category}")

        for pdf_file in category_dir.glob("*.pdf"):

            file_id = files_dao.save(str(pdf_file))

            text = extract_text(pdf_file)
            if not text:
                continue

            vector = embedder.encodeText(text).astype(float).tolist()

            points.append(
                PointStruct(
                    id=file_id,
                    vector=vector,
                    payload={
                        "file_id": file_id,
                        "category": category,
                        "text": text
                    }
                )
            )

            counter += 1

            if counter % 50 == 0:
                qdrant.upsert(settings.QDRANT_COLLECTION, points)
                print(f"✓ {counter} CV insérés…")
                points = []

    if points:
        qdrant.upsert(settings.QDRANT_COLLECTION, points)

    print(f" Ingestion terminée : {counter} CV insérés !")

# if __name__ == "__main__":
#     ingest()
