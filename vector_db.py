import numpy as np 

class VectorDatabase:

    def __init__(self,vector_dim):
        self.vector_dim = vector_dim
        self.vectors = np.empty((0,vector_dim))
        self.ids = []
        self.metadata = []

    def add_vector(self,vector,vector_id,meta=None):
        if len(vector)!=self.vector_dim:
            raise ValueError(f"Vector should be pf dimension {self.vector_dim}")
        self.vector = np.vstack([self.vectors,vector])
        self.ids.append(vector_id)
        self.metadata.append(meta)

        