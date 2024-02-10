from flask import Flask
from flask import request
from neomodel import config
from flask_cors import CORS
app=Flask(__name__)
from RecEngine.description_embeddings import Embedding
vectorizer=Embedding()
from Controllers.userController import add_user,delete_user,calculate_users_profiles
from Config.db import database_url
from Controllers.productController import add_product,delete_product
from Controllers.dataController import calculate_product_profiles
from Controllers.relationController import add_relation
from Controllers.recController import get_initial_rec,get_rec
config.DATABASE_URL=database_url
print(config.DATABASE_URL)


CORS(app)

@app.route('/user',methods=['POST'])
def post_user():
    response=add_user()
    return response

@app.route('/user',methods=['DELETE'])
def del_user():
    response=delete_user()
    return response

@app.route('/user',methods=['PUT'])
def put_user_profiles():
    response=calculate_users_profiles()
    return response

@app.route('/product',methods=['POST'])
def post_product():  
    response=add_product()
    return response

@app.route('/product',methods=['DELETE'])
def del_product():  
    response=delete_product()
    return response

@app.route('/data',methods=['PUT'])
def put_product_profiles():
    response=calculate_product_profiles()
    return response

@app.route('/relation',methods=['POST'])
def post_relation():
    response=add_relation()
    return response

@app.route('/rec',methods=['GET'])
def get_first_rec():
    response=get_initial_rec()
    return response

@app.route('/rec/service',methods=['GET'])
def get_rec_pipeline():
    response=get_rec()
    return response


if __name__=='__main__':
    app.run()