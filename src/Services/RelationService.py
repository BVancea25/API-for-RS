from neomodel import db
from RecEngine.review_sentiment import sentiment_analyzer

def add_relation_service(req):
    try:
        user_id=req['user_id']
        product_id=req['product_id']
        weight=float(req['weight'])
        action=str(req['action'])
        
        
        query = (
            f"MATCH (u:User),(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} OPTIONAL MATCH (u)-[r]->(p) RETURN  u, p, r"
        )
        
        result=db.cypher_query(query)#obtain the requested nodes
        
        
        
    
        if (len(result[0])!=0):#check if there already is a relationship with a "higher" action
            
            rel=result[0][0][2]
            
            if (rel['action']=="REVIEWED" or rel['weight']>=weight):
                return "Higher relation present"
            
            delete_query=(
                f"MATCH (u:User)-[r:HAS]->(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} DELETE r"
            )
            db.cypher_query(delete_query)
        
        print(action)
        if action=="REVIEWED":
            print("teset2")
            review=req["review"]
            rating=int(req["rating"])
            weight=use_sentiment(review,rating)
            print(weight)
            
            
        insert_query=(
                f"MATCH (u:User),(p:Product) WHERE u.client_id={user_id} AND p.client_id={product_id} "
                f" CREATE (u)-[rel:HAS]->(p) SET rel.action='{action}', rel.weight={weight} "
            )
        
        db.cypher_query(insert_query)
        
        
        return "Relationship created !"
    except Exception as e:
        return "Error while creating relation :"+str(e)


def use_sentiment(text,rating):
            
            analyzer=sentiment_analyzer(text)
            sentiment=analyzer.get_sentiment()
            print(sentiment)
            if sentiment=='Positive':
                    rating+=1
            elif sentiment=='Negative':
                    rating-=1

            if rating>5:
                    rating=5
            elif rating<=0:
                    rating=1
            
            
            match rating:
                case 1:
                    weight=0.1
                case 2:
                    weight=0.2
                case 3:
                    weight=0.3
                case 4:
                    weight=0.7
                case 5:
                    weight=0.8

            return weight