from neomodel import db
from RecEngine.review_sentiment import Sentiment_Analyzer

def add_relation_service(req):
    
    query = (
        f"MATCH (u:User),(p:Product) WHERE u.client_id={req['user_id']} AND p.client_id={req['product_id']} OPTIONAL MATCH (u)-[r]->(p) RETURN  u, p, r"
    )
     
    result=db.cypher_query(query)#obtain the requested nodes
    print(result)
    rel=result[0][0][2]
    
    if rel!=None:#check if there already is a relationship with a "higher" action
        
        if (rel['action']=="REVIEWED" or rel['weight']>=req['weight']):
            return "Relationship not created. Higher or equal relationship already exists."
        
        delete_query=(
            f"MATCH (u:User)-[r:HAS]->(p:Product) WHERE u.client_id={req['user_id']} AND p.client_id={req['product_id']} DELETE r"
        )
        db.cypher_query(delete_query)
    
    
    if req['action']=='REVIEWED':
        req['weight']=useSentiment(req['review'],req['rating'])
        
        
    insert_query=(
            f"MATCH (u:User),(p:Product) WHERE u.client_id={req['user_id']} AND p.client_id={req['product_id']} "
            f" CREATE (u)-[rel:HAS]->(p) SET rel.action='{req['action']}', rel.weight={req['weight']} "
        )
    
    db.cypher_query(insert_query)
    
    
    return "Relationship created !"


def useSentiment(text,rating):
            
            analyzer=Sentiment_Analyzer(text)
            sentiment=analyzer.getSentiment()
            if sentiment=='Positive':
                    rating+=2
            elif sentiment=='Negative':
                    rating=2

            if rating>5:
                    rating=5
            elif rating<=0:
                    rating=1
            
            
            match rating:
                case 1:
                    weight=0.1
                case 2:
                    weight=0.2
                case 4:
                    weight=0.7
                case 5:
                    weight=0.8

            return weight