from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
client = QdrantClient(host="localhost", port=6333)

collection_name = "cv_vectors"

# Exemple d'offre
offer = """We are looking for an Artificial Intelligence Engineer to design,
develop, and deploy machine learning models for real-world applications.
The candidate should have strong skills in Python, deep learning frameworks,
experience with NLP or computer vision, and a good understanding of data pipelines."""

offer_vector = encoder.encode(offer).tolist()

hits = client.query_points(
    collection_name=collection_name,
    query=offer_vector,
    limit=5
).points

for hit in hits:
    print(f"ID: {hit.id}, score: {hit.score:.4f}, file: {hit.payload.get('filename')}")
