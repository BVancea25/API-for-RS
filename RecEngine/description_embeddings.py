from sentence_transformers import SentenceTransformer

class Embedding:
    _instance = None   
    model = SentenceTransformer('all-mpnet-base-v2')  # Initialize the model once

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass  

    def get_embedding(self, text):
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding
