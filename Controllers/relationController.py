from flask import request,jsonify
from Services.RelationService import add_relation_service


def add_relation():
    req=request.get_json()
    response=add_relation_service(req)
    if(response=="Relationship created !"):
         return jsonify({'message':'Relation created successfuly'}),200
    else:
        return jsonify({'message':response}),400