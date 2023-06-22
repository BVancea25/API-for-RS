from flask import request,jsonify
from Config.db import database
from RecEngine.recommendation import Recommendation



def encode():
   database.one_hot_encode_product_properties()
   ids=database.get_all_users_ids()
   for user_id in ids:
        database.build_user_profile(user_id)
   return jsonify({'message':'ceva'}),200


def get_recommendation():

    if 'Content-Length' in request.headers and int(request.headers['Content-Length']) > 0:
        req=request.get_json()
        if 'user_id' in req:
            recomandare=database.best_recommendation_cb(req['user_id'])
            recomandare_embedding=database.best_recommendation_embbeding(recomandare['id'],req['user_id'])
            return jsonify({'best product for the user based on cb has the id ':recomandare['id'],'best product for the user based on embeddings has the id ':recomandare_embedding[0]})
        else :
            return jsonify({"Missing user_id"})
    else:
            recomandare=database.popular_products()
            return jsonify({"best product for the user based on popularity has the id:":recomandare})
    

