import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import pdfplumber
import os
import glob

from src.config.settings import settings


class Embedder():
    def __init__(self):
        self.sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
        self.qdrant_client = QdrantClient(host= settings.QDRANT_HOST, port= settings.QDRANT_PORT)

    def initiate_qdrant_collection(self):
        # initiate collection if not exist
        collections = self.qdrant_client.get_collections().collections
        existing_collection_names = [c.name for c in collections]
        if settings.QDRANT_COLLECTION not in existing_collection_names:
            try:
                self.qdrant_client.create_collection(
                    collection_name=settings.QDRANT_COLLECTION,
                    vectors_config=VectorParams(
                        size=self.sentence_transformer.get_sentence_embedding_dimension(),
                        distance=Distance.COSINE,
                    ),
                )
            except Exception as e:
                print(f"Error creating collection: {e}")

    def extract_text_from_pdf(self, file_path) -> str:
        text_pages = []
        try:

            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text_pages.append(page_text)
        except Exception as e:
            print(f"Erreur while opening file path {file_path} : {e}")
        text = "\n".join(text_pages)
        return text


    def simple_chunking(self, text, max_chars=1000, overlap=200) -> list[str]:
        chunks = []
        start = 0
        length = len(text)

        while start < length:
            end = start + max_chars
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks

    def index_single_cv(self, pdf_path):
        pdf_path = Path(pdf_path)
        cv_id = pdf_path.name

        print(f" Indexation du CVfdfd : {pdf_path} (cv_id={cv_id})")

        cv_text : str = self.extract_text_from_pdf(pdf_path)

        chunks_list : list[str] = self.simple_chunking(cv_text)


        # create a list of metadonne par chunk
        payloads_list = []

        for chunk_index, chunk in enumerate(chunks_list):
            # Payload = métadonnées
            payload = {
                "cv_id": cv_id,
                "chunk_index": chunk_index,
                "text": chunk,
            }
            payloads_list.append(payload)



        embedded_chunks = self.sentence_transformer.encode(chunks_list, convert_to_numpy=True)


        points = []
        for i, (vec, payload) in enumerate(zip(embedded_chunks, payloads_list)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vec.tolist(),  # Qdrant attend une liste Python
                payload=payload,
            )
            points.append(point)

        try:
            self.qdrant_client.upsert(
                collection_name=settings.QDRANT_COLLECTION,
                points=points,
            )
        except Exception as e:
            print(f"Erreur during upsert to Qdrant for cv {cv_id} : {e}")
            return
        print("insertion dans Qdrant reussi pour cv {cv_id} avec {len(points)} chunks")

    def index_all_cvs_in_directory(self, directory_path):
        pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in directory {directory_path}")

        for idx, pdf_file in enumerate(pdf_files):
            try:
                self.index_single_cv(pdf_file)
            except Exception as e:
                print(f"Error indexing file {pdf_file}: {e}")
                continue
            print(f"Successfully indexed {idx} files over {len(pdf_files)} ")

    def perform_query(self, query_text, top_k=5):
        query_vector = self.sentence_transformer.encode([query_text], convert_to_numpy=True)

        try:
            search_result = self.qdrant_client.search(
                collection_name=settings.QDRANT_COLLECTION,
                query_vector=query_vector.tolist()[0],
                limit=top_k,
            )
        except Exception as e:
            print(f"Error during Qdrant search: {e}")
            return []

        results = []
        for hit in search_result:
            result = {
                "cv_id": hit.payload.get("cv_id"),
                "chunk_index": hit.payload.get("chunk_index"),
                "text": hit.payload.get("text"),
                "score": hit.score,
            }
            results.append(result)

        return results















