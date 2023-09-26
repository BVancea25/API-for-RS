from flask import Flask
from flask import request
app=Flask(__name__)
from Controllers.dataController import encode,get_recommendation
from Controllers.userController import add_user
from Controllers.productController import add_product
from Controllers.relationController import add_relation
from Config.db import database


database.connect()


@app.route('/user',methods=['POST'])
def post_user():
    response=add_user()
    return response

@app.route('/product',methods=['POST'])
def post_product():  
    response=add_product()
    return response

@app.route('/relation',methods=['POST'])
def post_relation():
    response=add_relation()
    return response

@app.route('/rec',methods=['POST'])
def initialize_vectors():
    response=encode()
    return response

@app.route('/rec',methods=['GET'])
def get_rec():
    response=get_recommendation()
    return response



if __name__=='__main__':
    app.run()