from flask import request,jsonify
from Config.db import database

def add_order():
    req=request.get_json()
    if 'user_id' not in req:
        return jsonify({'message':'Missing user id field'}),400
    if 'product_id' not in req :
        return jsonify({'message':'Missing product id'}),400    
    
    try:
        database.create_relationship(req['user_id'],req['product_id'],"bought",{"weight":1})
        return jsonify({"message":"Relationship created"}),201
    except Exception as e:
        print(f"An error occurred while creating the relationship: {e}")
        return jsonify({"error":f"An error occurred while creating the relationship: {e}"}) ,400 