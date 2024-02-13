from flask import request,jsonify
from Services.RelationService import add_relation_service
from Services.RecService import get_initial_rec_service,get_rec_service
def get_initial_rec():
    try:
        
        response=get_initial_rec_service(request)
    
        return response,200
    except Exception as e:
        return jsonify({'message':e}),400
    
def get_rec():
    try:
        add_relation_service(request)
        
        response=get_rec_service(request)
        return response,200
    except Exception as e:
        return jsonify({'message':e}),400