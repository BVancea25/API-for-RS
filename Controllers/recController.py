from flask import request,jsonify
from Services.RelationService import add_relation_service
from Services.RecService import get_initial_rec_service,get_rec_service
def get_initial_rec():
    try:
        req=request.get_json()
        response=get_initial_rec_service(req)
    
        return response
    except Exception as e:
        return jsonify({'message':e}),400
    
def get_rec():
    try:
        req=request.get_json()
        add_relation_service(req)
        response=get_rec_service(req)
        return response
    except Exception as e:
        return jsonify({'message':e}),400