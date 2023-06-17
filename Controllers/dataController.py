from flask import request,jsonify
from Config.db import database
from RecEngine.recommendation import Recommendation

def handle_data():
    req=request.get_json()
    print(req)
    if 'users' not in req :
        return jsonify({'message':'Users header missing'}),400
    if 'products' not in req:
        return jsonify({'message':'Products header missing'}),400
    if 'orders' not in req:
        return jsonify({'message':'Order header missing'}),400


    for user in req['users']:
        database.create_node("User",{"nume":user['nume'], "id":user['id'],"profil":[]})

   

    return jsonify({'message':'Data added'}),201

def encode():
    database.one_hot_encode_product_properties()
    return jsonify({'message':'ceva'}),200


