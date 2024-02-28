from flask import Flask
from flask import request,jsonify
from neomodel import config
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect,generate_csrf
app=Flask(__name__)
from RecEngine.description_embeddings import Embedding
vectorizer=Embedding()
from Controllers.userController import add_user,delete_user,calculate_users_profiles
from Config.db import database_url
from Controllers.productController import add_product,delete_product
from Controllers.dataController import calculate_product_profiles
from Controllers.relationController import add_relation
from Controllers.recController import get_initial_rec,get_rec
from dotenv import load_dotenv


config.DATABASE_URL=database_url


app.config['SECRET_KEY']='73eeac3fa1a0ce48f381ca1e6d71f077'
#csrf=CSRFProtect(app)
CORS(app,resources={r"/*":{"origins":["http://localhost:3000","http://localhost:8080"],"send_wildcard":"False"}},supports_credentials=True)


@app.route('/csrf-token',methods=['GET'])
def csrf_token():
    csrf_token=generate_csrf()
    return jsonify({'csrf_token': csrf_token}), 200

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

@app.route('/rec',methods=['POST'])
def get_first_rec():
    response=get_initial_rec()
    return response

@app.route('/rec/service',methods=['POST'])
def get_rec_pipeline():
    response=get_rec()
    return response


if __name__=='__main__':
    app.run()