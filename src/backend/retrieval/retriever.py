from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np
from embeddings.embedder import Embedder
from config.settings import settings


class Retriever:

    def __init__(self, collection_name=settings.QDRANT_COLLECTION):
        self.collection_name = collection_name

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            prefer_grpc=True,
            grpc_port=settings.QDRANT_GRPC_PORT,
            timeout=60.0
        )

        # Nouvel encodeur ONNX
        self.embedder = Embedder()


    def search(self, query: str, top_k: int = 5, category: str = None):
        """
        Recherche les CV les plus pertinents pour une description de poste donnée.
        """

        #  AVANT : query_vector = [[...], [...]] → Qdrant ERROR
        #  MAINTENANT : vecteur 1D float64
        vector = self.embedder.encodeText(query)

        # Sécurité : convertir en list of float
        query_vector = vector.astype(float).tolist()

        # --- Filtre optionnel sur la catégorie ---
        qdrant_filter = None
        if category:
            qdrant_filter = Filter(
                must=[FieldCondition(
                    key="category",
                    match=MatchValue(value=category.upper())
                )]
            )

        # --- Recherche dans Qdrant ---
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=qdrant_filter,
        )

        # --- Mise en forme ---
        matches = []
        for r in results:
            payload = r.payload
            matches.append({
                "category": payload.get("category", "Inconnue"),
                "score": r.score,
                "text_preview": payload.get("text", "")[:250] + "..."
            })

        return matches



retriever = Retriever()


@tool
def rag(description_poste: str, top_k: int = 5, category: str = None):
    """
    Recherche les CV les plus pertinents pour une description de poste donnée.
    Utilisé comme outil du LLM.
    """

    results = retriever.search(description_poste, top_k=top_k, category=category)

    if not results:
        return {
            "description_poste": description_poste,
            "top_profils": "Aucun CV trouvé."
        }

    profils_text = "\n".join([
        f"- [{r['category']}] (score={round(r['score'],3)}) : {r['text_preview']}"
        for r in results
    ])

    return {
        "description_poste": description_poste,
        "top_profils": profils_text
    }
