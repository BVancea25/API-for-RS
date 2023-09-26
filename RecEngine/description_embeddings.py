from sentence_transformers import SentenceTransformer
import nltk
from nltk.tokenize import sent_tokenize
from Config.db import database
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
        sentences = sent_tokenize(text)
        embedding = self.model.encode(sentences, convert_to_numpy=True,normalize_embeddings=True)
        pca=database.principal_component_analysis(embedding)
        aggregated_pca = sum(pca[i][0] for i in range(len(pca)))
        min_pca = min(pca[i][0] for i in range(len(pca)))  # Minimum PCA value
        max_pca = max(pca[i][0] for i in range(len(pca)))
        
        return self.min_max_scaling(aggregated_pca,min_pca,max_pca)

    def min_max_scaling(self,value, min_val, max_val):
        return (value - min_val) / (max_val - min_val)