from qdrant_client import QdrantClient
import numpy as np
from qdrant_client.models import Distance, VectorParams ,PointStruct

class VectorStore:

    def __init__(self,type,dimension=None,model=None):
        self.type = type
        self.dimension = dimension
        self.client = None
        self.collection = None



        if(type == "qdrant"):
           
            print("on travaille avec Qdrant")

            coll_name = "ResumeVectorBase"
            http_port, grpc_port = 6338, 6336
            
            client = QdrantClient(
                url=f"http://localhost:{http_port}",
                prefer_grpc=True,
                grpc_port=grpc_port,
                timeout=60.0,    # 60s pour les grosses opérations
            )

            self.client = client
            self.collection_name = coll_name 

            # Vérifie si la collection existe déjà
            existing = [c.name for c in client.get_collections().collections]
            if coll_name not in existing:
                client.create_collection(
                    collection_name=coll_name,
                    vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
                )
                print(f"Collection '{coll_name}' créée.")
            else:
                print(f"Collection '{coll_name}' déjà existante.")

            self.collection = coll_name  # conserve juste le nom pour upsert plus loin

        else : 
            print("ERREUR   :: pas encore implémenté ce type de database !!")





    def add_vectors(self, data_items: list[dict], vectors: list[np.ndarray]):

        points = []

        for item, vector in zip(data_items, vectors):
            point = PointStruct(
                id=item["id"],
                vector=np.array(vector, dtype=np.float32).tolist(),
                payload={
                    "text": item["text"],
                    "category": item["category"]
                }
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
                wait=True
            )

        print(f"Total {len(points)} points upsertés avec succès dans '{collection_name}'.")



    def getType(self):
        return self.type

    

    def getDimension(self):
        return self.dimension
    
    def getClient(self):
        return self.client

    def getCollection(self):
        return self.collection

    def get_backend(self):   # À corriger
        return  self.client,self.collection
        

    def close(self):
        if self.getType() == "qdrant":
            self.client = None



    



        




