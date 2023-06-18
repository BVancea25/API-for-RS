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
   ids=database.get_all_users_ids()
   for user_id in ids:
        database.build_user_profile(user_id)
   return jsonify({'message':'ceva'}),200


def get_recommendation():
    req=request.get_json()
    if 'user_id' in req:
        recomandare=database.best_recommendation_cb(req['user_id'])
        recomandare_embedding=database.best_recommendation_embbeding(recomandare['id'],req['user_id'])
        return jsonify({'best product for the user based on cb has the id ':recomandare['id'],'best product for the user based on embeddings has the id ':recomandare_embedding[0]})
    return jsonify({'error':'ceva'})

