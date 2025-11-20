"""
Classifier module for CV classification using centroid-based approach.
Each category has multiple centroid vectors in the embedding space.
"""

import numpy as np
from typing import List, Dict, Tuple
from embeddings.embedder import Embedder
import pickle
from pathlib import Path


class CVClassifier:
    """
    Classifies CVs into skill/job categories using centroid-based clustering.
    
    Architecture:
    - Each category (e.g., "DATA SCIENTIST") has multiple centroid vectors
    - These centroids represent different aspects/skills within that category
    - When classifying a CV, we find the nearest centroids across all categories
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", num_centroids_per_category: int = 3):
        """
        Initialize the classifier.
        
        Args:
            model_name: Embedding model name
            num_centroids_per_category: Number of centroid vectors per job category
        """
        self.model_name = model_name
        self.embedder = Embedder(model_embedding=model_name)
        self.num_centroids_per_category = num_centroids_per_category
        
        # category_name -> List[centroid_vectors]
        self.centroids: Dict[str, np.ndarray] = {}
        
        # For tracking which CVs belong to which category for centroid computation
        self.category_embeddings: Dict[str, List[np.ndarray]] = {}


    def add_cv_to_category(self, category: str, cv_embedding: np.ndarray):
        """
        Add a CV embedding to a category for later centroid computation.
        
        Args:
            category: Job category (e.g., "DATA-SCIENTIST")
            cv_embedding: Embedding vector of the CV
        """
        if category not in self.category_embeddings:
            self.category_embeddings[category] = []
        
        self.category_embeddings[category].append(cv_embedding)


    def compute_centroids(self):
        """
        Compute centroid vectors for each category using K-means clustering.
        Each category gets multiple centroids representing different skill profiles.
        """
        from sklearn.cluster import KMeans
        
        print("\nComputing centroids for each category...")
        
        for category, embeddings in self.category_embeddings.items():
            if len(embeddings) == 0:
                print(f"Category '{category}' has no CVs, skipping...")
                continue
            
            embeddings_array = np.array(embeddings)
            
            # Number of clusters = min(num_centroids_per_category, number of CVs)
            n_clusters = min(self.num_centroids_per_category, len(embeddings))
            
            if n_clusters == 1:
                # If only 1 CV or 1 centroid, use the mean
                centroid = np.mean(embeddings_array, axis=0)
                self.centroids[category] = np.array([centroid])
            else:
                # K-means clustering
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                kmeans.fit(embeddings_array)
                self.centroids[category] = kmeans.cluster_centers_
            
            print(f"   {category}: {n_clusters} centroids computed from {len(embeddings)} CVs")


    def classify(self, cv_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        """
        Classify a CV embedding to the top-k most similar categories.
        
        Args:
            cv_embedding: Embedding vector of the CV
            top_k: Number of top categories to return
            
        Returns:
            List of dicts with format:
            {
                "category": str,
                "similarity": float,
                "nearest_centroid_index": int,
                "description": str
            }
        """
        if not self.centroids:
            raise ValueError("Centroids not computed yet. Call compute_centroids() first.")
        
        results = []
        
        # For each category, find the nearest centroid
        for category, centroids_array in self.centroids.items():
            # Compute cosine similarity between CV and all centroids of this category
            similarities = []
            for i, centroid in enumerate(centroids_array):
                similarity = self._cosine_similarity(cv_embedding, centroid)
                similarities.append((similarity, i))
            
            # Get the best match (highest similarity) for this category
            best_similarity, best_centroid_idx = max(similarities)
            
            results.append({
                "category": category,
                "similarity": float(best_similarity),
                "nearest_centroid_index": int(best_centroid_idx),
                "description": f"{category} (centroid #{best_centroid_idx + 1})"
            })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


    def classify_text(self, text: str, top_k: int = 3) -> List[Dict]:
        """
        Classify a text (CV content) directly.
        
        Args:
            text: Raw text content of the CV
            top_k: Number of top categories to return
            
        Returns:
            List of classification results
        """
        embedding = self.embedder.encode(text)
        return self.classify(embedding, top_k=top_k)


    @staticmethod
    def _cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return np.dot(vec1, vec2) / (norm1 * norm2)


    def save(self, filepath: str):
        """Save classifier state (centroids) to disk."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            "centroids": self.centroids,
            "num_centroids_per_category": self.num_centroids_per_category,
            "model_name": self.model_name,
        }
        
        with open(filepath, "wb") as f:
            pickle.dump(state, f)
        
        print(f" Classifier saved to {filepath}")


    def load(self, filepath: str):
        """Load classifier state (centroids) from disk."""
        with open(filepath, "rb") as f:
            state = pickle.load(f)
        
        self.centroids = state["centroids"]
        self.num_centroids_per_category = state["num_centroids_per_category"]
        self.model_name = state["model_name"]
        
        print(f" Classifier loaded from {filepath}")
