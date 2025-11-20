"""
Enhanced Retriever with Classification support.

Features:
- Semantic search with vector similarity
- Classification-aware filtering
- Combined retrieval from multiple category centroids
"""

from langchain.tools import tool
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, HasIdCondition
import numpy as np
from embeddings.embedder import Embedder
from classification.classifier import CVClassifier
from config.settings import settings
from typing import List, Dict, Optional


class ClassificationAwareRetriever:
    """
    Enhanced retriever that leverages CV classifications.
    
    When searching, it can:
    1. Find semantically similar CVs (traditional RAG)
    2. Filter by classified job categories
    3. Return classification metadata with results
    """

    def __init__(
        self,
        collection_name: str = settings.QDRANT_COLLECTION,
        model_name: str = "all-MiniLM-L6-v2",
        classifier: Optional[CVClassifier] = None,
    ):
        self.collection_name = collection_name
        self.model_name = model_name
        self.embedder = Embedder(model_embedding=self.model_name)
        self.classifier = classifier

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            prefer_grpc=True,
            grpc_port=settings.QDRANT_GRPC_PORT,
            timeout=60.0,
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        category: Optional[str] = None,
        classified_category: Optional[str] = None,
        min_similarity: float = 0.0,
    ) -> List[Dict]:
        """
        Search for relevant CVs using semantic similarity and optional classification.
        
        Args:
            query: Job description or search query
            top_k: Number of top results to return
            category: Original category filter (from folder structure)
            classified_category: Classified job category filter (from classifier)
            min_similarity: Minimum similarity score threshold
            
        Returns:
            List of matching CVs with scores and metadata
        """
        # 1. Classify the query to understand what job profile we're looking for
        query_classifications = None
        if self.classifier:
            query_classifications = self.classifier.classify_text(query, top_k=3)
            print(f"\n Query classified as:")
            for clf in query_classifications:
                print(
                    f"   - {clf['category']}: {clf['similarity']:.3f}"
                )

        # 2. Generate embedding for semantic search
        query_vector = self.embedder.encode(query).tolist()

        # 3. Build Qdrant filter
        qdrant_filter = self._build_filter(category, classified_category)

        # 4. Search in Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k * 2,  # Get more candidates to filter
            query_filter=qdrant_filter,
        )

        # 5. Format results and filter by similarity
        matches = []
        for r in results:
            if r.score < min_similarity:
                continue

            payload = r.payload
            match_info = {
                "id": r.id,
                "source_category": payload.get("category", "Inconnue"),
                "similarity_score": round(r.score, 4),
                "text_preview": payload.get("text", "")[:300] + "...",
            }

            # Add classification metadata if available
            if payload.get("primary_classification"):
                match_info["primary_classification"] = payload.get(
                    "primary_classification"
                )
                match_info["classification_score"] = round(
                    payload.get("primary_classification_score", 0.0), 4
                )

            matches.append(match_info)

        # 6. Return top_k matches
        return matches[:top_k], query_classifications

    def _build_filter(
        self, category: Optional[str] = None, classified_category: Optional[str] = None
    ) -> Optional[Filter]:
        """
        Build Qdrant filter based on category constraints.
        """
        conditions = []

        if category:
            conditions.append(
                FieldCondition(key="category", match=MatchValue(value=category.upper()))
            )

        if classified_category:
            conditions.append(
                FieldCondition(
                    key="primary_classification",
                    match=MatchValue(value=classified_category.upper()),
                )
            )

        if not conditions:
            return None

        return Filter(must=conditions)

    def search_by_classification(
        self, job_profile: str, top_k: int = 5
    ) -> List[Dict]:
        """
        Search for CVs matching a specific job classification.
        
        This method first classifies the job profile, then searches for CVs
        classified in that category.
        
        Args:
            job_profile: Description of the job
            top_k: Number of results
            
        Returns:
            List of matching CVs classified as this job type
        """
        if not self.classifier:
            raise ValueError("Classifier not available")

        # Classify the job profile
        classifications = self.classifier.classify_text(job_profile, top_k=1)
        target_category = classifications[0]["category"]

        print(f"\n Searching for CVs classified as: {target_category}")

        # Search using classified category filter
        results, _ = self.search(
            job_profile, top_k=top_k, classified_category=target_category
        )

        return results

    def get_classification_insights(self, cv_id: str) -> Dict:
        """
        Get detailed classification information about a specific CV.
        """
        # Retrieve the point from Qdrant
        try:
            points = self.client.retrieve(
                collection_name=self.collection_name, ids=[cv_id]
            )
            if not points:
                return {"error": f"CV with id {cv_id} not found"}

            payload = points[0].payload

            return {
                "cv_id": cv_id,
                "source_category": payload.get("category"),
                "primary_classification": payload.get("primary_classification"),
                "primary_classification_score": payload.get(
                    "primary_classification_score"
                ),
                "all_classifications": [
                    {
                        "category": payload.get(f"classification_{i}_category"),
                        "score": payload.get(f"classification_{i}_score"),
                    }
                    for i in range(1, 4)
                    if payload.get(f"classification_{i}_category")
                ],
            }
        except Exception as e:
            return {"error": str(e)}


# Create global instance (for direct usage)
retriever = ClassificationAwareRetriever()


@tool
def rag_with_classification(
    description_poste: str, top_k: int = 5, category: str = None
):
    """
    Search for CVs using semantic + classification-aware retrieval.
    
    This tool combines:
    1. Semantic similarity matching
    2. CV classification metadata
    3. Category filtering

    Args:
        description_poste: Description of the job opening or candidate profile
        top_k: Number of CVs to return (default 5)
        category: Optional category filter (accountant, data-scientist, engineer, etc.)
    """
    results, query_classifications = retriever.search(
        description_poste, top_k=top_k, category=category
    )

    if not results:
        return {
            "description_poste": description_poste,
            "top_profils": "Aucun CV trouvé.",
            "query_classifications": None,
        }

    # Format results with classification info
    profils_text = "\n".join(
        [
            f"- [{r['source_category']}] (sim={r['similarity_score']}) "
            f"[classified: {r.get('primary_classification', 'N/A')}] : {r['text_preview']}"
            for r in results
        ]
    )

    return {
        "description_poste": description_poste,
        "top_profils": profils_text,
        "query_classifications": query_classifications,
        "num_results": len(results),
    }


# Keep original rag tool for backward compatibility
@tool
def rag(description_poste: str, top_k: int = 5, category: str = None):
    """Recherche les CV les plus pertinents pour une description de poste donnée.

    Args:
        description_poste: description de l'offre d'emploi ou du poste
        top_k: nombre de CV renvoyés, par défaut 5 si la personne ne le précise pas
        category: la catégorie visée par l'offre
    """
    results, _ = retriever.search(description_poste, top_k=top_k, category=category)

    if not results:
        return {
            "description_poste": description_poste,
            "top_profils": "Aucun CV trouvé.",
        }

    profils_text = "\n".join(
        [
            f"- [{r['source_category']}] (score={r['similarity_score']}) : {r['text_preview']}"
            for r in results
        ]
    )

    return {
        "description_poste": description_poste,
        "top_profils": profils_text,
    }

