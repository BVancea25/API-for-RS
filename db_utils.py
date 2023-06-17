from neo4j import GraphDatabase
from RecEngine.review_sentiment import Sentiment_Analyzer

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
            self.driver=GraphDatabase.driver(uri, auth=(username, password))
            self.session=None
    
    def connect(self):
        if self.session is None:
            self.session = self.driver.session()

    def close(self):
         if self.driver is not None:
            self.driver.close()
            self.driver = None
            self.session = None

    def create_node(self, label, properties):
        try:
            query = f"CREATE (n:{label} $props) RETURN n"
            result = self.session.run(query, props=properties)
            node = result.single()[0]
            return node
        except Exception as e:
            print(f"An error occurred while creating the node: {e}")
            return None
    
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
            print(f"An error occurred while deleting the node: {e}")
            return None
            
    
    def create_relationship(self, from_id, to_id, rel_type, properties={}):
        try:
            if(rel_type!="REVIEW"):
                query = "MATCH (u:User), (i:Item) WHERE u.id = $from_id AND i.id = $to_id CREATE (u)-[rel:" + rel_type + "]->(i) SET rel += $properties RETURN rel"
                result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                rel = result.single()[0]
                return rel
            else:
                query="MATCH (u:User) where u.id=$from_id match (u)-[r:bought]->(i:Item) where i.id=$to_id return r"
                result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                result_list=list(result)
                if not result_list:
                    return "User didn't buy this item!!!"
                else:
                    properties=self.__useSentiment(properties)
                    query="MATCH (u:User) where id(u)=$from_id match (u)-[r:bought]->(i:Item) where id(i)=$to_id CREATE (u)-[new_r:REVIEW]->(i) SET new_r +=$properties DELETE r RETURN new_r"
                    result = self.session.run(query, from_id=from_id, to_id=to_id, properties=properties)
                    rel=result.single()[0]
                    return rel
        except Exception as e:
            print(f"An error occurred while creating the relationship: {e}")
            return None
        
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
            analyzer=Sentiment_Analyzer(properties["text"])
            sentiment=analyzer.getSentiment()
            
            if sentiment=='Positive':
                    properties["rating"]+=2
            elif sentiment=='Negative':
                    properties["rating"]-=2

            if properties["rating"]>5:
                    properties["rating"]=5
            elif sentiment["rating"]<0:
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

    
   