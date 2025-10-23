from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer, util
import pandas as pd

df = pd.read_csv("Resume.csv")

encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

client = QdrantClient(host="localhost", port=6333)

#client.delete_collection("cv_vectors")

"""if not client.collection_exists("cv_vectors"):
    client.create_collection(
        collection_name="cv_vectors",
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
        ),
    )"""

#vectors = [encoder.encode(text).tolist() for text in df["Resume_str"]]

"""client.upload_points(
    collection_name="cv_vectors",
    points=[
        models.PointStruct(
            id=int(row["ID"]), vector=vectors[idx], payload={
                "Resume_html": row["Resume_html"],
                "Category": row["Category"]
            }
        )
        for idx, row in df.iterrows()
    ],
)"""

offer = "We are looking for an Artificial Intelligence Engineer to design, develop, and deploy machine learning models for real-world applications. The candidate should have strong skills in Python, deep learning frameworks such as PyTorch or TensorFlow, experience with NLP or computer vision, and a good understanding of data pipelines and model optimization. Experience with cloud environments (AWS or Azure) and MLOps tools is a plus."

offer_vector = encoder.encode(offer).tolist()

hits = client.query_points(
    collection_name="cv_vectors",
    query=encoder.encode(offer).tolist(),
    limit=5
).points

for hit in hits:
    print(f"ID: {hit.id}, score: {hit.score}, category: {hit.payload.get('Category')}")