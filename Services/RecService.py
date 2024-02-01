from neomodel import db
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy.linalg import norm
import traceback
import json
from Services.DataService import calculate_user_profile_pipeline
from Models.Product import Product

def popular_products():
        try:
            query=f"MATCH (p:Product)<-[r:HAS]-(u:User) WITH p, COUNT(r) AS popularity RETURN p, popularity ORDER BY popularity DESC LIMIT 1;"
            result=db.cypher_query(query)
            print(result[0][0][0])
            node=Product.inflate(result[0][0][0])
            return node.serialize()
                
        except Exception as e:
            traceback.print_exc()
            return f"Error occured while retreiving popular items:{str(e)}"
            



def get_initial_rec_service(req):
    try:
        user_id=req['user_id']
        
        query=(f"MATCH (u:User) where u.client_id={user_id} MATCH (products:Product) WHERE NOT (u)-[:HAS]->(products) RETURN products,u.profile,u.favorite_description;")
        results=db.cypher_query(query)
        
        results=list(results)
        
        del results[1]
        user_profile=results[0][0][1]
        print(user_profile)
        if(len(user_profile)==0):
            return popular_products()
        favorite_embedding=results[0][0][2]
        
        
        profile_similarities=[]
        description_similarities=[]
        for result in results[0]:
            
            product_profile=result[0]['profile']
            product_embedding=result[0]['embedding']
            
            description_similarities.append(cosine_similarity(favorite_embedding,product_embedding))
            profile_similarities.append(cosine_similarity(user_profile,product_profile))
        
        
        similarities=weighted_similarity(profile_similarities,description_similarities)
        
        index_of_product=similarities.index(max(similarities))
        
        
        
       
        node=Product.inflate(results[0][index_of_product][0])
          
        return json.dumps(node.serialize())
        
            
        
    except Exception as e:
            traceback.print_exc()
            return f"Error occured while getting recommendation:{str(e)}"
        
def cosine_similarity(a,b):
    
    
    if(len(a)!=len(b)):
        longer_list = a if len(a) >= len(b) else b
        shorter_list = b if len(a) >= len(b) else a

        # Pad the shorter list with zeros
        padding_length = len(longer_list) - len(shorter_list)
        shorter_list.extend([0] * padding_length)
        
    
    dot=np.inner(a,b)
    norm_a=norm(a)
    norm_b=norm(b)
    
    sim=dot/(norm_a*norm_b)
   
    return sim

def get_rec_service(req):
    
    calculate_user_profile_pipeline(req)
    
    return get_initial_rec_service(req)
    
    
        
def weighted_similarity(profile_similarities,description_similarities):
    
    similarities=[]
    i=0
    
    while(i<len(profile_similarities)):
        similarities.append((profile_similarities[i]*0.8+description_similarities[i]*0.2)/2)
        i+=1
        
    return similarities
    