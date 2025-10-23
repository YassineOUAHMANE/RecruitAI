import os
import fitz
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# Extraction du texte des PDF
def extract_text_from_pdfs(folder_path):
    pdf_texts = {}
    for file in os.listdir(folder_path):
        if file.lower().endswith(".pdf"):
            doc = fitz.open(os.path.join(folder_path, file))
            text = " ".join(page.get_text("text") for page in doc)
            pdf_texts[file] = text
    return pdf_texts

cv_texts = extract_text_from_pdfs("data/data/ENGINEERING")

#print(cv_texts)

# Initialisation de l’encodeur et du client Qdrant
encoder = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
client = QdrantClient(host="localhost", port=6333)

# Création de la collection si elle n’existe pas
collection_name = "cv_vectors"

#client.delete_collection(collection_name)

if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE,
        ),
    )

# Vectorisation
texts = list(cv_texts.values())
filenames = list(cv_texts.keys())
vectors = encoder.encode(texts, batch_size=16, show_progress_bar=True).tolist()

# Envoi dans Qdrant
client.upload_points(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=i,
            vector=vectors[i],
            payload={"filename": filenames[i], "text": texts[i]},
        )
        for i in range(len(filenames))
    ],
)