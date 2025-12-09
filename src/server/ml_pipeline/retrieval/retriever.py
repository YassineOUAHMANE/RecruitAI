from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import numpy as np
from ml_pipeline.embeddings.embedder import Embedder
from ml_pipeline.config.settings import settings


class Retriever:


    def __init__(self, collection_name= settings.QDRANT_COLLECTION, model_name="all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.model_name = model_name
        self.client = QdrantClient(
            host = settings.QDRANT_HOST,
            port = settings.QDRANT_PORT,
            prefer_grpc = True, 
            grpc_port = settings.QDRANT_GRPC_PORT, 
            timeout = 60.0
            )

        self.embedder = Embedder(model_embedding=self.model_name)



    def search(self, query: str, top_k: int = 5, category: str = None):
        """
        Recherche les CV les plus pertinents pour une description de poste donnée.
        Retourne une liste des meilleurs candidats trouvés.
        """

        query_vector = self.embedder.encodeText(query).tolist()

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
    """Recherche les CV les plus pertinents pour une description de poste donnée.

    Args:
        description_poste: description de l'offre d'emploi ou du poste
        top_k: nombre de CV renvoyés, par défaut 5 si la personne ne le précise pas
        category: la catégorie visée par l'offre
    """
    
    #print("appel de Rag \n")

    #print(description_poste, "\n")
    #print(top_k, "\n")
    #print(category, "\n")

    results = retriever.search(description_poste, top_k=top_k, category=category)

    if not results:
        return {"description_poste": description_poste, "top_profils": "Aucun CV trouvé."}

    profils_text = "\n".join([
        f"- [{r['category']}] (score={r['score']}) : {r['text_preview']}"
        for r in results
    ])

    #print("profile texts :", profils_text, "\n")

    return {
        "cv_ids": [r["id"] for r in results],
        "description_poste": description_poste,
        "top_profils": profils_text
    }