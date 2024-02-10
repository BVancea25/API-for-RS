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
            query=f"MATCH (p:Product)<-[r:HAS]-(u:User) WITH p, COUNT(r) AS popularity ORDER BY popularity DESC LIMIT 3 RETURN p;"
            result=db.cypher_query(query)
            print("Sent popular data!!!")
            
            data=[]
            for node in result[0]:
                inflated_node=Product.inflate(node[0])
                data.append(inflated_node.serialize())
            
            return data
                
        except Exception as e:
            traceback.print_exc()
            return f"Error occured while retreiving popular items:{str(e)}"
            



def get_initial_rec_service(req):
    try:
        
        user_id=req.args.get('user_id')
        print(user_id)
        if(user_id=="none"): #utilizator neautentificat
            return popular_products()
        query=(f"MATCH (u:User) where u.client_id={user_id} MATCH (products:Product) WHERE NOT (u)-[:HAS]->(products) RETURN products,u.profile,u.favorite_description;")
        results=db.cypher_query(query)
        
        results=list(results)
        
        del results[1]
        print(results[0])
        if not results[0]:#daca utilizatorul a interactionat cu toate produsele
            return popular_products()
        
        
        user_profile=results[0][0][1]
       
        if(len(user_profile)==0):#daca utilziatorul nu a interactionat cu nici un produs
            return popular_products()
        
        favorite_embedding=results[0][0][2]
        
        
        profile_similarities=[]
        description_similarities=[]
        for result in results[0]:
            
            product_profile=result[0]['profile']
            product_embedding=result[0]['embedding']
            
            description_similarities.append(cosine_similarity(favorite_embedding,product_embedding))
            profile_similarities.append(cosine_similarity(user_profile,product_profile))
        
        recommendations=[]
        similarities=weighted_similarity(profile_similarities,description_similarities)
        
        
        # Sort the list indices based on the corresponding values
        sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)

        # Get the indices of the three largest values
        top_3_indices = sorted_indices[:3]

        for index in top_3_indices:
            inflated_node=Product.inflate(results[0][index][0])
            recommendations.append(inflated_node.serialize())
        
        print(recommendations)
          
        return recommendations
        
            
        
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
    
    res=calculate_user_profile_pipeline(req)
    if(res=="no user"):
        return popular_products()
    return get_initial_rec_service(req)
    
    
        
def weighted_similarity(profile_similarities,description_similarities):
    
    similarities=[]
    i=0
    
    while(i<len(profile_similarities)):
        similarities.append((profile_similarities[i]*0.8+description_similarities[i]*0.2)/2)
        i+=1
        
    return similarities
    