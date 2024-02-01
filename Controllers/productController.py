from Services.ProductService import add_product_service,delete_product_service
from flask import request,jsonify


def add_product():
    req=request.get_json()
    response=add_product_service(req)
    
    if(response=="Saved product!"):
       return jsonify({'message':'Save successful'}),200
    else:
        return jsonify({'message':response}),400
    
def delete_product():
    req=request.get_json()
    response=delete_product_service(req)
    if(response=="Product deletion successful!"):
        return jsonify({'message':'Deletion successful'}),200
    else:
        return jsonify({'message':response}),400