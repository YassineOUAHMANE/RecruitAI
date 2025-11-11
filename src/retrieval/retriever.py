from langchain_core.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np
from embeddings.embedder import Embedder


class Retriever:


    def __init__(self, collection_name="ResumeVectorBase", model_name="all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.model_name = model_name
        self.client = QdrantClient(url="http://localhost:6333",prefer_grpc=True,grpc_port=6336,timeout=60.0)

        self.embedder = Embedder(model_embedding=self.model_name)



    def search(self, query: str, top_k: int = 5, category: str = None):
        """
        Recherche les CV les plus pertinents pour une description de poste donnée.
        Retourne une liste des meilleurs candidats trouvés.
        """

        query_vector = self.embedder.encodeText(query).astype(np.float32).tolist()

        # filtre par type
        qdrant_filter = None
        if category:
            qdrant_filter = Filter(
                must=[FieldCondition(key="category", match=MatchValue(value=category.upper()))]
            )

        # Recherche dans Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=qdrant_filter,
        )

        # Mise en forme simple
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
    """Recherche les CV les plus pertinents pour une description de poste donnée."""

    
    results = retriever.search(description_poste, top_k=top_k, category=category)

    if not results:
        return {"description_poste": description_poste, "top_profils": "Aucun CV trouvé."}

    profils_text = "\n".join([
        f"- [{r['category']}] (score={r['score']}) : {r['text_preview']}"
        for r in results
    ])

    return {
        "description_poste": description_poste,
        "top_profils": profils_text
    }