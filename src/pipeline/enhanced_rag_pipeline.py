"""
Enhanced RAG Pipeline with CV Classification.

Flow:
1. Parse CVs from data folders
2. Generate embeddings for each CV
3. Build classifier with category centroids
4. Enhance vector store with classification metadata
"""

from ingestion.parser import ResumeParser
from embeddings.embedder import Embedder
from storage.vector_store import VectorStore
from classification.classifier import CVClassifier
from config.settings import settings
import numpy as np


class EnhancedRAGPipeline:
    """
    RAG Pipeline with integrated CV classification.
    
    Architecture:
    - Parser: Extracts CV text and category from folder structure
    - Embedder: Converts text to vectors (384-dim, all-MiniLM-L6-v2)
    - Classifier: Builds category centroids and classifies each CV
    - VectorStore: Stores embeddings with classification metadata
    """

    def __init__(
        self,
        base_path: str = "/home/moussaoui/langchain-chatbot/data/data",
        model_embedding: str = "all-MiniLM-L6-v2",
        vector_db: str = "qdrant",
        num_centroids_per_category: int = 3,
    ):
        self.base_path = base_path
        self.model_embedding = model_embedding
        self.vector_db = vector_db
        self.num_centroids_per_category = num_centroids_per_category

        # Initialize components
        self.parser = ResumeParser(base_path=self.base_path)
        self.embedder = Embedder(model_embedding=self.model_embedding)
        self.classifier = CVClassifier(
            model_name=self.model_embedding,
            num_centroids_per_category=num_centroids_per_category,
        )
        self.store = VectorStore(type=self.vector_db, dimension=384)

    def run(self) -> dict:
        """
        Execute the full pipeline: parse → embed → classify → store.
        
        Returns:
            dict with statistics about the pipeline execution
        """
        print("\n" + "=" * 60)
        print(" Starting Enhanced RAG Pipeline with Classification")
        print("=" * 60)

        # Step 1: Parse CVs
        print("\n[Step 1/4] Parsing CVs from data folders...")
        data = self.parser.parse()
        print(f" Parsed {len(data)} CVs")

        # Step 2: Generate embeddings
        print("\n[Step 2/4] Generating embeddings...")
        texts = [item["text"] for item in data]
        vectors = self.embedder.encodeBatch(texts)
        print(f" Generated {len(vectors)} embeddings (384-dim)")

        # Step 3: Build classifier with centroids
        print("\n[Step 3/4] Building classifier and computing centroids...")
        for item, vector in zip(data, vectors):
            category = item["category"]
            self.classifier.add_cv_to_category(category, vector)

        self.classifier.compute_centroids()
        print(f" Classifier ready with {len(self.classifier.centroids)} categories")

        # Step 4: Classify each CV and add metadata
        print("\n[Step 4/4] Classifying CVs and storing with metadata...")
        enhanced_data = []

        for item, vector in zip(data, vectors):
            # Get classification predictions
            classifications = self.classifier.classify(vector, top_k=3)

            # Enhance data with classification metadata
            enhanced_item = {
                **item,
                "embedding": vector,
                "classifications": classifications,
                "primary_classification": classifications[0] if classifications else None,
            }
            enhanced_data.append(enhanced_item)

        # Store in vector database with enriched metadata
        self._store_enhanced_data(enhanced_data)

        # Save classifier state
        classifier_path = settings.get("CLASSIFIER_PATH", "src/classification/models/classifier.pkl")
        self.classifier.save(classifier_path)

        print("\n" + "=" * 60)
        print(f" Pipeline completed successfully!")
        print(f"   - Total CVs: {len(enhanced_data)}")
        print(f"   - Categories: {len(self.classifier.centroids)}")
        print(f"   - Centroids per category: {self.num_centroids_per_category}")
        print("=" * 60 + "\n")

        return {
            "total_cvs": len(enhanced_data),
            "num_categories": len(self.classifier.centroids),
            "embeddings_dimension": 384,
            "centroids_per_category": self.num_centroids_per_category,
        }

    def _store_enhanced_data(self, enhanced_data: list):
        """
        Store enhanced data in vector database with classification metadata.
        
        Each stored point includes:
        - text: original CV text
        - category: source category from folder
        - primary_classification: top classification result
        - all_classifications: top-3 classifications
        """
        points = []

        for item in enhanced_data:
            # Create payload with all metadata
            payload = {
                "text": item["text"],
                "category": item["category"],
                "primary_classification": item["primary_classification"]["category"]
                if item["primary_classification"]
                else None,
                "primary_classification_score": item["primary_classification"]["similarity"]
                if item["primary_classification"]
                else 0.0,
            }

            # Add top-3 classifications as individual fields
            for idx, clf in enumerate(item["classifications"]):
                payload[f"classification_{idx + 1}_category"] = clf["category"]
                payload[f"classification_{idx + 1}_score"] = clf["similarity"]

            point_data = {
                "id": item["id"],
                "vector": item["embedding"],
                "payload": payload,
            }
            points.append(point_data)

        # Store all points in vector database
        vectors_only = [p["vector"] for p in points]
        data_for_store = [
            {
                "id": p["id"],
                "text": p["payload"]["text"],
                "category": p["payload"]["category"],
            }
            for p in points
        ]

        self.store.add_vectors(data_for_store, vectors_only)

        # Store payload metadata separately (for retrieval enrichment)
        for p in points:
            self.store.add_metadata(p["id"], p["payload"])

        print(f" Stored {len(points)} points in vector database with metadata")
