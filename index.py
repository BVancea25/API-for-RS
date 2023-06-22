from flask import Flask
from flask import request
app=Flask(__name__)
from Controllers.dataController import encode,get_recommendation
from Controllers.userController import add_user
from Controllers.productController import add_product
from Controllers.orderController import add_order
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

@app.route('/order',methods=['POST'])
def post_order():
    response=add_order()
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