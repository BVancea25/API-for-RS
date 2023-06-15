from flask import request,jsonify
from Config.db import database

def add_user():
    req=request.get_json()
    if 'name' not in req :
        return jsonify({'message':'Missing name'}),400
    if 'id' not in req :
        return jsonify({'message':'Missing id'}),400
    if(database.check_user(req['id'])==-1):
        return jsonify({'message':'User already exists'}),403

    database.create_node("User",{"name":req['name'], "id":req['id'],"profile":[]})
    return jsonify({'message':'User added'}),201

