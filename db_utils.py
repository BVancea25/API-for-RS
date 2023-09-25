from neo4j import GraphDatabase
from RecEngine.review_sentiment import Sentiment_Analyzer
import logging
import sys
from RecEngine.translator import Translator

class DB_UTILS:
    _instance=None
    driver=None
    session=None

    def __new__(cls,*args,**kwargs):
        if not cls._instance:
            cls._instance=super().__new__(cls)
        return cls._instance
    


    def __init__(self,uri,username,password):
        if self.driver is None:
            try:
                #handler = logging.StreamHandler(sys.stdout)
                #handler.setLevel(logging.DEBUG)
                #logging.getLogger("neo4j").addHandler(handler)
                #logging.getLogger("neo4j").setLevel(logging.DEBUG)            
                self.driver=GraphDatabase.driver(uri, auth=(username, password))
                self.session=None
                print("Driver initialized")
            except Exception as e:
                print(f"An error occurred while initializing the DB driver: {e}")
                return None
            
    
    def connect(self):
        if self.session is None:
            try:
                self.session = self.driver.session()
                print("Connected to DB")
            except Exception as e:
                print(f"An error occurred while initializing the DB session: {e}")

    def close(self):
         if self.driver is not None:
            self.driver.close()
            self.driver = None
            self.session = None

    def create_node(self, label, properties):
        try:
           
            query = f"CREATE (n:{label} $props) RETURN n"
            print("ceva1")
            result = self.session.run(query, props=properties)
            print("ceva2")
            node = result.single()[0]
            return node
        except Exception as e:
            print(f"An error occurred while creating the node: {e}")
            return e
    
    def get_product(self, product_id):
        try:
            query = "MATCH (n:Item) WHERE n.id = $node_id RETURN n"
            result = self.session.run(query, node_id=product_id)
            node = result.single()[0]
            properties = dict(node)
            del properties["profile"]
            return properties
        except Exception as e:
            print(f"An error occurred while getting the shoe: {e}")
            return None
    
    def get_all_users_ids(self):
        try:
            query = "MATCH (n:User) RETURN n.id"
            result = self.session.run(query)
            ids=[record["n.id"] for record in result]
            return ids
        except Exception as e:
            print(f"An error occurred while getting the shoe: {e}")
            return None
    
    def delete_node(self, node_id):
        try:
            query = "MATCH (n) WHERE id(n) = $node_id DETACH DELETE n"
            self.session.run(query, node_id=node_id)
            return "Node deleted!"
        except Exception as e:
            print(f"An error occurred while deleting the node: {e}")
            return None
        
    def check_user(self,user_id):
        try:
            query="MATCH (n:User) where n.id=$user_id return n"
            result=self.session.run(query,user_id=user_id)
            user=result.single()[0]
            if(user):
                return -1
            return user
        except Exception as e:
            print(f"An error occurred while verifing the existance of the node: {e}")
            return None
            
    
    def create_relationship(self, from_id, to_id, rel_type, properties={}):
        try:
            if(rel_type!="review"):
                print(rel_type)
                query = "MATCH (u:User), (i:Item) WHERE u.id = $from_id AND i.id = $to_id CREATE (u)-[rel:" + rel_type + "]->(i) SET rel += $properties RETURN rel"
                result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                rel = result.single()[0]
                return 0
            else: #verificam daca utilizatorul a cumparat produsul inainte de a crea o relatie review
                print("altceva")
                query="MATCH (u:User) where u.id=$from_id match (u)-[r:bought]->(i:Item) where i.id=$to_id return r"
                result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                result_list=list(result)
                if not result_list:
                    return -1
                else:
                    properties=self.__useSentiment(properties)
                    print("ceva1")
                    query="MATCH (u:User) where u.id=$from_id match (u)-[r:bought]->(i:Item) where i.id=$to_id CREATE (u)-[new_r:review]->(i) SET new_r +=$properties DELETE r RETURN new_r"
                    print("ceva2")
                    result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                    print("ceva3")
                    rel=result.single()[0]
                    print(rel)
                    return 0
        except Exception as e:
            print(f"An error occurred while saving the relationship in the database: {e}")
            return -1
        
    def delete_relationship(self, from_id, to_id, rel_type):
        try:
            
            query = "match (u:User)-[r:"+rel_type+"]-(i:Item) where u.id=$from_id and i.id=$to_id delete r"
            result = self.session.run(query, from_id=from_id, to_id=to_id)
            rel = result.single()[0]
            return rel
          
        except Exception as e:
            print(f"An error occurred while creating the relationship: {e}")
            return None
    
    def __useSentiment(self,properties={}):
            translator=Translator()
            properties["text"]=translator.translate(properties["text"])
            analyzer=Sentiment_Analyzer(properties["text"])
            sentiment=analyzer.getSentiment()
            if sentiment=='Positive':
                    properties["rating"]+=2
            elif sentiment=='Negative':
                    properties["rating"]-=2


            if properties["rating"]>5:
                    properties["rating"]=5
            elif properties["rating"]<=0:
                    properties["rating"]=1
            
            
            match properties["rating"]:
                case 1:
                    properties["weight"]=0.1
                case 2:
                    properties["weight"]=0.2
                case 4:
                    properties["weight"]=1.3
                case 5:
                    properties["weight"]=1.5

            return properties

    
   