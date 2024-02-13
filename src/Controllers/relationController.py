from flask import request,jsonify
from Services.RelationService import add_relation_service

def add_relation():
    response=add_relation_service(request)
    if(response=="Relationship created !"):
         return jsonify({'message':'Relation created successfuly'}),200
    else:
        return jsonify({'message':response}),400