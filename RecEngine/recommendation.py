from db_utils import DB_UTILS
import numpy as np
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class Recommendation(DB_UTILS):

    _uniqueValues=0

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
            embeddings=[]
            modified_result = []  # Store modified records here
            ids=[]
            for record in result:
                properties = dict(record["n"])  # Convert Record to a dictionary
                embeddings.append(properties["embedding"])
                del properties["embedding"]  # Remove the 'embedding' key
                del properties["profile"]
                ids.append(properties["id"])
                del properties["id"]
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
            #print(unique_values)
            self._uniqueValues=sum(len(values) for values in unique_values.values())+1
            

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
                
                
                encoded_vector.append(embeddings[index])
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
                    MATCH (u)-[r:saw|bought|review|wishlist]->(i:Item)
                    RETURN i.profile,r.weight
                    """
                result=self.session.run(query, user_id=user_id)
                result_list=list(result)
                user_profile=np.zeros(self._uniqueValues)
                print(self._uniqueValues)
                print(f"Acest utilizator a interactionat cu {len(result_list)} elemente")
                
                for x in result_list:#am facut asta in cazul in care avem mai multe relatii nu doar SAW si bought
                        i=0
                        print(f"Vectorul produsului cu numarul {i}")
                        
                        for index,value in enumerate(x["i.profile"]):#inmultim vectorul cu weightul corespunzator
                            i+=1
                            if value !=0 :
                                print(f"Caracterstica {x['i.profile'][index]} a vectorului {x['i.profile']} a fost inmultita cu {x['r.weight']}" )
                                if(i<self._uniqueValues):
                                    x["i.profile"][index]*=x["r.weight"]
                                    print(f"{i} din {10} valori")
                                print(f"Rezultatul este {x['i.profile'][index]}")
                                user_profile[index]+=x["i.profile"][index]#adunam valorile tuturor vectorilor
                                
                                print(f"Valoarea totala in profilul utilizatorului {user_profile[index]}")
                            """ elif value !=0 and index==len(result_list)-1:#nu dorim sa inmultim embedingul cu weightul
                                user_profile[index]+=x["i.profile"][index]
                                print(f"Adaugam embeding-ul in profil {user_profile[index]}")"""
                        print(f"Profil utilizator este {user_profile}\n")
                        
                        
                for i in range(len(user_profile)):#impartim rezultatul la numarul produselor
                    if user_profile[i]!=0:
                        user_profile[i]/=len(result_list)   
                
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
                WHERE NOT EXISTS((u)-[:saw|bought|review|wishlist]->(i))
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
    
    
    def principal_component_analysis(self,embedding):
        try:
            embedding_data = np.array(embedding)
            #embedding_data = embedding_data.reshape(1, -1)
            
            mean = np.mean(embedding_data, axis=0)
            
            centered_data = embedding_data - mean
            #print(centered_data)

                # Calculate the covariance matrix
            cov_matrix = np.cov(centered_data, rowvar=False)

                # Compute eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

                # Sort eigenvalues in descending order
            eigenvalue_indices = np.argsort(eigenvalues)[::-1]
            eigenvalues = eigenvalues[eigenvalue_indices]
            eigenvectors = eigenvectors[:, eigenvalue_indices]
                # Select the top N principal components
            N = 1  # Replace with the desired number of components
            selected_components = eigenvectors[:, :N]
            
                # Project the data onto the selected principal components
            projected_data = np.dot(centered_data, selected_components)
            return projected_data

            
        except Exception as e:
            print(f"Error occured while retreiving embedding recommendation:{str(e)}")
            return None
    
    def popular_products(self):
        try:
            query="""match (n:Item)-[r:bought]-(u:User)  return COUNT(r) as popularity,n.id as id"""
            result=self.session.run(query)
                 
            max=-1
            maxID=-1
            for record in result:
                if record["popularity"]>max:
                    max=record["popularity"]
                    maxID=record["id"]
            
            return maxID
                
        except Exception as e:
            print(f"Error occured while retreiving popular items:{str(e)}")
            return None
        
def cosine_distance(a, b):
    return 1 - cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))

