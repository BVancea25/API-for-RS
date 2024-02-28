from Models.Product import Product
from Models.User import User
from neomodel import db
import numpy as np
import traceback
from sklearn.metrics.pairwise import cosine_similarity

def calculate_product_profiles_service():
    try:
        products=Product.nodes.order_by('client_id').all()
        
        ids=[]
       
        unique_brands = set()
        unique_colors = set()
        unique_types = set()

        
        for product in products: #calculate number of unique values across all atributes
            ids.append(product.client_id)
            unique_brands.add(product.brand)      
            unique_colors.add(product.color)
            unique_types.add(product.type)
        
        
        brand_to_index = {brand: idx for idx, brand in enumerate(unique_brands)}
        color_to_index = {color: idx for idx, color in enumerate(unique_colors)}
        type_to_index = {type: idx for idx, type in enumerate(unique_types)}

        encoded_vector=[]
        index=0 #for appending the correct embedding in the product profile
        # One-hot encode products
        for product in products:
            # Create one-hot vectors
            brand_vector = [0] * len(unique_brands)
            brand_vector[brand_to_index[product.brand]] = 1

            color_vector = [0] * len(unique_colors)
            color_vector[color_to_index[product.color]] = 1

            type_vector = [0] * len(unique_types)
            type_vector[type_to_index[product.type]] = 1
            
            encoded_vector=brand_vector+color_vector+type_vector
            
            product_instance=Product.nodes.get(client_id=ids[index])
            product_instance.profile=encoded_vector
            product_instance.save()
            
            index+=1
        
        return "Profiles calculated!"
    except Exception as e:
         return f"Error in calculating product profiles: {e}"
     
def calculate_users_profiles_service():
    try:
        users=User.nodes.order_by('client_id').all()
        
        for user in users:
            get_rel_query=(
                f"MATCH (u:User) WHERE u.client_id = {user.client_id} MATCH (u)-[r:HAS]->(p:Product) RETURN p.profile, r.weight, p.embedding"
                        )
            results=db.cypher_query(get_rel_query)
            results=list(results)
            del results[1]
            
            user_profile,most_relevant_embedding=calculate_user_profile(results[0])
            user.profile=user_profile
            user.favorite_description=most_relevant_embedding
            user.save()
            
        
        return "Calculation of user profile successful"
    except Exception as e:
          return f"Calculation operation failed: {e}"
    
def calculate_user_profile(results):
    try:
        
        max_weight=0.0
        n_products=0
        user_profile=np.zeros(13)
        most_relevant_embedding=[]
        for result in results:
            
            product_profile=result[0]
            weight=result[1]
            embedding=result[2]
            
            if(weight>max_weight):
                most_relevant_embedding=embedding
                
            product_profile = [value * weight for value in product_profile]
            
            user_profile=[x+y for x,y in zip(user_profile,product_profile)]
            
            n_products+=1
                
        
        user_profile = [element / n_products if element != 0 else 0 for element in user_profile]
        
        return user_profile,most_relevant_embedding
    
    except Exception as e:
        traceback.print_exc()
        return f"Calculation operation failed: {e}"


def calculate_user_profile_pipeline(req):
    try:
        user_id=req['user_id']
        if(user_id=="none"):
            return "no user"
        else:
            user=User.nodes.get(client_id=user_id)
            get_rel_query=(
                    f"MATCH (u:User) WHERE u.client_id = {user.client_id} MATCH (u)-[r:HAS]->(p:Product) RETURN p.profile, r.weight, p.embedding"
                            )
            results=db.cypher_query(get_rel_query)
            results=list(results)
            del results[1]
                
            user_profile,most_relevant_embedding=calculate_user_profile(results[0])
            user.profile=user_profile
            user.favorite_description=most_relevant_embedding
            user.save()
                
            
            return "Calculation of user profile successful"
    except Exception as e:
        traceback.print_exc()
        return f"Calculation operation failed: {e}"
