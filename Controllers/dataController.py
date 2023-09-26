from flask import request,jsonify
from Config.db import database
from RecEngine.recommendation import Recommendation



def encode():
   database.one_hot_encode_product_properties()
   ids=database.get_all_users_ids()
   unique_ids=set(ids)
   unique_list=list(unique_ids)
   for user_id in unique_list: 
        database.build_user_profile(user_id)
   return jsonify({'message':'ceva'}),200

def get_recommendation():

    if 'Content-Length' in request.headers and int(request.headers['Content-Length']) > 0:
        req=request.get_json()
        if 'user_id' in req:
            recomandare=database.best_recommendation_cb(req['user_id'])
            
            return jsonify({'best product for the user based on cb has the id ':recomandare['id']})
        else :
            return jsonify({"message":"Missing user_id"}),400
    else:
            recomandare=database.popular_products()
            return jsonify({"best product for the user based on popularity has the id:":recomandare})
    

