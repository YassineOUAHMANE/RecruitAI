from qdrant_client import QdrantClient
import numpy as np
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import settings

class VectorStore:

    def __init__(self, type, dimension=None, model=None):
        self.type = type
        self.dimension = dimension
        self.client = None
        self.collection = None
        self.metadata_store = {}  # In-memory metadata storage

        if type == "qdrant":
            print("on travaille avec Qdrant")

            coll_name = settings.QDRANT_COLLECTION

            client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                prefer_grpc=True,
                grpc_port=settings.QDRANT_GRPC_PORT,
                timeout=60.0,
            )

            self.client = client
            self.collection_name = coll_name

            # Vérifie si la collection existe déjà
            existing = [c.name for c in client.get_collections().collections]
            if coll_name not in existing:
                client.create_collection(
                    collection_name=coll_name,
                    vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
                )
                print(f"Collection '{coll_name}' créée.")
            else:
                print(f"Collection '{coll_name}' déjà existante.")

            self.collection = coll_name

        else:
            print("ERREUR :: pas encore implémenté ce type de database !!")

    def add_vectors(self, data_items: list[dict], vectors: list[np.ndarray]):
        """Add vectors to the database."""
        points = []

        for idx, (item, vector) in enumerate(zip(data_items, vectors)):
            # Use simple sequential ID to avoid UUID range issues with Qdrant
            # Qdrant requires 64-bit unsigned integer IDs
            point_id = idx + 1  # Start from 1 instead of 0
            
            point = PointStruct(
                id=point_id,
                vector=np.array(vector, dtype=np.float32).tolist(),
                payload={
                    "text": item["text"],
                    "category": item["category"],
                    "item_id": str(item["id"]),  # Store original id in payload
                },
            )
            points.append(point)

        print(f"{len(points)} points préparés pour insertion dans Qdrant.")

        client, collection_name = self.get_backend()

        batch_size = 200
        for start in range(0, len(points), batch_size):
            end = start + batch_size
            batch = points[start:end]
            client.upsert(
                collection_name=collection_name,
                points=batch,
                wait=True,
            )

        print(f"Total {len(points)} points upsertés avec succès dans '{collection_name}'.")

    def add_metadata(self, point_id: str, metadata: dict):
        """Store additional metadata for a point (for classification support)."""
        self.metadata_store[point_id] = metadata

    def get_metadata(self, point_id: str) -> dict:
        """Retrieve metadata for a point."""
        return self.metadata_store.get(point_id, {})

    def getType(self):
        return self.type

    def getDimension(self):
        return self.dimension

    def getClient(self):
        return self.client

    def getCollection(self):
        return self.collection

    def get_backend(self):
        return self.client, self.collection

    def close(self):
        if self.getType() == "qdrant":
            self.client = None
