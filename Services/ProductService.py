from Models.Product import Product
from RecEngine.regex import extract_characteristics,extract_description


def add_product_service(req):
    try:
        from index import vectorizer #avoid circular import because of the dependency of index file
        
        #description=extract_description(req['html'])
        
        #data=extract_characteristics(req['html'])
        print(req['description'])
        embedding=vectorizer.get_embedding(req['description'])
        print(embedding)
        Product(name=req['name'],embedding=embedding,profile=[],color=req['color'],type=req['type'],brand=req['brand'],client_id=req['id']).save()
        
        return "Saved product!"
    except Exception as e:
         return f"Create product operation failed: {e}"
     
def delete_product_service(req):
    try:
        product_to_delete=Product.nodes.get(client_id=req['id'])
        product_to_delete.delete()
        return "Product deletion successful!"
    except Exception as e:
        return f"Delete operation failed: {e}"