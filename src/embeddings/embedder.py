"""
Embedder module - Converts text to embedding vectors.
Uses Sentence Transformers for semantic embeddings.
"""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    """
    Converts text to embedding vectors using Sentence Transformers.
    
    Default model: all-MiniLM-L6-v2 (384-dimensional vectors)
    - Lightweight and fast
    - Good semantic understanding
    - 384 dimensions (compared to 768 for larger models)
    """

    def __init__(self, model_embedding: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a specific model.
        
        Args:
            model_embedding: Name of the Sentence Transformers model
        """
        self.model_name = model_embedding
        self.model = SentenceTransformer(model_embedding)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

    def encode(self, text: str) -> np.ndarray:
        """
        Encode a single text to embedding.
        
        Args:
            text: Text to encode
            
        Returns:
            Embedding vector as numpy array (384-dim)
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding

    def encodeBatch(self, texts: List[str]) -> List[np.ndarray]:
        """
        Encode multiple texts efficiently.
        
        Args:
            texts: List of texts to encode
            
        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return [emb for emb in embeddings]

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.embedding_dim
