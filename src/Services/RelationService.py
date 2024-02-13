from neomodel import db
from RecEngine.review_sentiment import Sentiment_Analyzer

def add_relation_service(req):
    user_id=req.args.get('user_id')
    product_id=req.args.get('product_id')
    weight=float(req.args.get('weight'))
    action=req.args.get('action')
    
    
    query = (
        f"MATCH (u:User),(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} OPTIONAL MATCH (u)-[r]->(p) RETURN  u, p, r"
    )
     
    result=db.cypher_query(query)#obtain the requested nodes
    
    rel=result[0][0][2]
  
    if rel!=None:#check if there already is a relationship with a "higher" action
        
        
        
        if (rel['action']=="REVIEWED" or rel['weight']>=weight):
            return "Higher relation present"
        
        delete_query=(
            f"MATCH (u:User)-[r:HAS]->(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} DELETE r"
        )
        db.cypher_query(delete_query)
    
    
    if action=='REVIEWED':
        review=req.args.get("review")
        rating=req.args.get("rating")
        weight=useSentiment(review,rating)
        
        
    insert_query=(
            f"MATCH (u:User),(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} "
            f" CREATE (u)-[rel:HAS]->(p) SET rel.action='{action}', rel.weight={weight} "
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