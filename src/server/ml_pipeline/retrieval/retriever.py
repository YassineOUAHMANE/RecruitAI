from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from ml_pipeline.embeddings.embedder import Embedder
from ml_pipeline.config.settings import settings



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

        self.embedder = Embedder()

    def search(self, query: str, top_k: int = 5, category: str = None):
        """
        Recherche les CV les plus pertinents dans Qdrant.
        """

        vector = self.embedder.encodeText(query).astype(float).tolist()

        qdrant_filter = None
        if category:
            qdrant_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category.upper())
                    )
                ]
            )

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=top_k,
            query_filter=qdrant_filter
        )
        matches = []
        for r in results.points:
            matches.append({
                "id": r.id,   
                "category": r.payload.get("category"),
                "score": r.score,
                "text_preview": r.payload.get("text")[:250] + "..."
            })


        


        return matches


retriever = Retriever()


@tool
def rag(description_poste: str, top_k: int = 5, category: str = None, message_id: str = None):
    """
    Recherche les CV les plus pertinents pour une description de poste.
    Utilisé par le LLM via LangChain.
    Quand tu appelles la fonction `rag`, tu DOIS inclure le champ `message_id`.
    La valeur du message_id doit être exactement celle fournie dans le message system sous la forme `message_id=<valeur>`.

    """

    results = retriever.search(description_poste, top_k=top_k, category=category)

    if not results:
        return {
            "description_poste": description_poste,
            "top_profils": "Aucun CV trouvé."
        }

    profils_text = "\n".join([
        f"- [{r['category']}] (score={round(r['score'], 3)}) : {r['text_preview']}"
        for r in results
    ])

    return {
        "message_id": message_id,
        "cv_ids": [r["id"] for r in results],
        "description_poste": description_poste,
        "top_profils": profils_text
    }
