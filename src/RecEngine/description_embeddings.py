from sentence_transformers import SentenceTransformer
import numpy as np
from nltk.tokenize import sent_tokenize


class Embedding:
    _instance = None   
    model = None  # Initialize the model once

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.model = SentenceTransformer('all-mpnet-base-v2')
          

    def get_embedding(self, text):
        sentences = sent_tokenize(text)
        embedding = self.model.encode(sentences, convert_to_numpy=True,normalize_embeddings=True)
        
        means=[]
        for entry in embedding:
            means.append(self.mean(entry))
        print(means)
        
        
        return means

   
    
    def mean(self,embedding):
        mean=np.mean(embedding)
        return mean
    
    