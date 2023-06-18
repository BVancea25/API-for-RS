from db_utils import DB_UTILS
import numpy as np
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity


class Recommendation(DB_UTILS):

    def __init__(self, uri, username, password):
        super().__init__(uri, username, password)

    def update_product_vector(self, product_id, vector):
        try:
            query = """
                MATCH (n:Item)
                WHERE n.id = $product_id
                SET n.profile = $vector
            """              
            self.session.run(query, product_id=product_id, vector=vector)
            return "Vector updated!"
        except Exception as e:
            # Log the error message or handle the exception as appropriate for your application
            print(f"An error occurred while updating the shoe vector: {str(e)}")
            return None    


    def one_hot_encode_product_properties(self):
        try:
            query = "MATCH (n:Item) RETURN n {.*}"
            result = self.session.run(query)
            #result_list=list(result)
            
            modified_result = []  # Store modified records here
            ids=[]
            for record in result:
                properties = dict(record["n"])  # Convert Record to a dictionary
                del properties["embedding"]  # Remove the 'embedding' key
                del properties["profile"]
                ids.append(properties["id"])
                del properties["id"]
                print(properties)
                modified_result.append(properties)  # Add mo
            
            #print(modified_result)
            # Extract unique attribute values from the data
            unique_values = {}
            for item in modified_result:
                for key, value in item.items():
                    if key not in unique_values:
                        unique_values[key] = set(value)
                    else:
                        unique_values[key] |= set(value)

            
            # Create an empty list to store encoded data
            encoded_data = []

            # One-hot encode each item and append to encoded_data list
            # !!! Daca ordinea caracteristicilor nu este consistenta vectorii vor fi afectati !!!
            index=0
            for item in modified_result:
                encoded_item = {}
                encoded_vector=[]
                for key, value in item.items():
                    encoded_values = np.zeros(len(unique_values[key]), dtype=int)
                    for v in value:
                        encoded_values[list(unique_values[key]).index(v)] = 1
                    encoded_item[key] = encoded_values
                    encoded_vector.extend(encoded_values)
                self.update_product_vector(ids[index],encoded_vector)
                index+=1
                                
        except Exception as e:
            print(f"An error occurred while one hot encoding:{str(e)}")
            return None
    
        #construim profilul userului cu ajutorul profilelor produselor    
    def build_user_profile(self,user_id):
            try: 
                #returneaza vectorii papucilor alaturi de weightul relatiei
                query = """ 
                    MATCH (u:User)
                    WHERE u.id = $user_id
                    MATCH (u)-[r:SAW|bought|REVIEW]->(i:Item)
                    RETURN i.profile,r.weight
                    """
                result=self.session.run(query, user_id=user_id)
                result_list=list(result)
                user_profile=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                for x in result_list:      #am facut asta in cazul in care avem mai multe relatii nu doar SAW si bought
                    #if x["r.weight"]!=1:    
                        for index,value in enumerate(x["i.profile"]):#inmultim vectorul cu weightul corespunzator
                            if value !=0:
                                x["i.profile"][index]*=x["r.weight"]
                                user_profile[index]+=x["i.profile"][index]#adunam valorile tuturor vectorilor

                for i in range(len(user_profile)):#impartim rezultatul la numarul papucilor
                    if user_profile[i]!=0:
                        user_profile[i]/=len(result_list)   
                print(user_profile)
                query=""" 
                    MATCH (u:User) WHERE u.id=$user_id
                    SET u.profile=$user_profile
                """
                self.session.run(query,user_id=user_id,user_profile=user_profile)
            except Exception as e:
                print(f"Error while calculating user profile:{str(e)}")
                return None
        
    def best_recommendation_cb(self,user_id):
    
        try:
        #returneaza profilul userului target, profilul tuturor papucilor cu care acesta nu a interactionat si idurile acestora
            query = """
                MATCH (u:User)
                WHERE u.id = $user_id
                MATCH (i:Item)
                WHERE NOT EXISTS((u)-[:SAW|bought]->(i))
                RETURN u.profile AS user_profile, COLLECT(i.profile) AS item_profiles, COLLECT(i.id) AS ids
                """
            result=self.session.run(query,user_id=user_id)
            result_list=list(result)
            
            user_profile=np.array(result_list[0][0])
            item_profiles=np.array(result_list[0][1])
            
            cos_sim=np.dot(item_profiles,user_profile)/(norm(item_profiles,axis=1)*norm(user_profile))#calculam similaritatea cosinus
            
            return self.get_product(result_list[0][2][np.argmax(cos_sim)])#returnam papucul cu similaritatea cea mai mare
        except Exception as e:
            print(f"Error occured while retreiving recommendation:{str(e)}")
            return None
        
    def best_recommendation_embbeding(self,product_id,user_id):
    
        try:
        
            query = """
                MATCH (i:Item) where
                i.id=$product_id
                RETURN i.embedding
                """
            result=self.session.run(query,product_id=product_id)
            node=list(result)
            target_embedding=np.array(node[0][0])
            
            query="""
                MATCH (u:User)
                WHERE u.id = $user_id
                MATCH (i:Item)
                WHERE NOT EXISTS((u)-[:SAW|bought]->(i))
                RETURN i.embedding, COLLECT(i.id) as ids
            """
            result=self.session.run(query,user_id=user_id)
            result_list=list(result)
            embeddings = [np.array(record["i.embedding"]) for record in result_list]
            ids = [record["ids"] for record in result_list]

            distances=[]
            for embedding in embeddings:
                
                distances.append(cosine_distance(target_embedding,embedding))

            return ids[np.argmin(distances)]
            

            
        except Exception as e:
            print(f"Error occured while retreiving recommendation:{str(e)}")
            return None
    
def cosine_distance(a, b):
    return 1 - cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))