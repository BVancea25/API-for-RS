from flask import request,jsonify
from Services.DataService import calculate_product_profiles_service
def calculate_product_profiles():
    response=calculate_product_profiles_service()
    
    if(response=="Profiles calculated!"):
       return jsonify({'message':'Profiles calculated'}),200
    else:
        return jsonify({'message':response}),400