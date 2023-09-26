from flask import request,jsonify
from Config.db import database

def add_relation():
    req=request.get_json()
    if 'user_id' not in req:
        return jsonify({'message':'Missing user id field'}),400
    if 'product_id' not in req :
        return jsonify({'message':'Missing product id'}),400 
    if 'rel_type' not in req:
        return jsonify({'message':'Missing relation type'}),400 
    
    try:
        weight=0
        match req['rel_type']:
            case 'saw':
                weight=0.3
            case 'wishlist':
                weight=0.7
            case _:
                weight=1.0
        if(req['rel_type']=='review'):
            response=database.create_relationship(req['user_id'],req['product_id'],req['rel_type'],{"weight":weight,"text":req['text'],"rating":req['rating']})
        else: 
            response=database.create_relationship(req['user_id'],req['product_id'],req['rel_type'],{"weight":weight})
        match response:
            case 0:
                status_code=200
                message="Relation Created"
            case -1:
                status_code=400
                message="Error while creating relation"
        return jsonify({"message":message}),status_code
    except Exception as e:
        print(f"An error occurred while creating the relationship: {e}")
        return jsonify({"error":f"An error occurred while creating the relationship: {e}"}) ,400 