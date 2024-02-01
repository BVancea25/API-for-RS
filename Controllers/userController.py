from flask import request,jsonify
from Services.UserService import add_user_service,delete_user_service
from Services.DataService import calculate_users_profiles_service

def delete_user():
    req=request.get_json()
    response=delete_user_service(req)
    if(response=="Successful deletion!"):
        return jsonify({'message':'Deletion successful'}),200
    else:
        return jsonify({'message':response}),400
    
    
def add_user():
    
    req=request.get_json()
    response=add_user_service(req)
    
    if(response=="Save successful"):
         return jsonify({'message':'Save successful'}),200
    else:
        return jsonify({'message':response}),400
    

def calculate_users_profiles():
    response=calculate_users_profiles_service()
    
    if(response=="Calculation of user profile successful"):
         return jsonify({'message':response}),200
    else:
        return jsonify({'message':response}),400