import numpy as np 

class VectorDatabase:

    def __init__(self,vector_dim):
        self.vector_dim = vector_dim
        self.vectors = np.empty((0,vector_dim))
        self.ids = []
        self.metadata = []

    def add_vector(self,vector,vector_id,meta=None):
        if len(vector)!=self.vector_dim:
            raise ValueError(f"Vector should be of dimension {self.vector_dim}")
        self.vector = np.vstack([self.vectors,vector])
        self.ids.append(vector_id)
        self.metadata.append(meta)

    def update_vector(self,vector_id,new_vector=None,new_meta=None):
        if new_vector is not None and len(new_vector)!=self.vector_dim:
            raise ValueError(f"Vector should be of dimension{self.vector_dim}")
        try:
            idx = self.ids.index(vector_id)
            if new_vector is not None:
                self.vector[idx] = new_vector
            if new_meta is not None:
                self.metadata[idx]=new_meta
        except ValueError:
            raise ValueError(f"Vector with ID{vector_id} not found")

    def query(self,query_vector,k=1):
        if len(query_vector)!=self.vector_dim:
            raise ValueError(f"Query vector should be of dimension {self.vector_dim}")
        distances = np.linalg.norm(self.vectors - query_vector,axis=1)
        nearest_indices = np.argpartition(distances,k)[:k]
        nearest_indices = nearest_indices[np.argsort(distances[nearest_inidices])]
        return [(self.ids[idx],distances[idx],self.metadata[idx]) for idx in nearest_indices]
    
    def delete_vector(self,vector_id):
        try:
            idx = self.ids.index(vector_id)
            self.vectors = np.delete(self.vectors,idx,axis=0)
            self.ids.pop(idx)
            self.metadata.pop(idx)
        except ValueError:
            raise ValueError(f"Vector with ID {vector_id} not found")

    def save(self,file_path):
        with h5py.File(file_path,'w') as f:
            f.create_dataset('vectors',data=self.vectors)
            f.create_dataset('ids',data=np.string_(self.ids))
            f.create_dataset('metadata',data=np.string_(self.metadata))

    def load(self,file_path,query_vector=None,k=1):
        with h5py.File(file_path,'r') as f:
            self.vectors = f['vectors'][:]
            self.ids = [x.decode() for x in f['ids'][:]]
            self.metadata = [x.decode() for x in f['metadata'][:]]
        if query_vector is not None:
            return self.query(query_vector,k=k)
        return None        