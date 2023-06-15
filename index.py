from flask import Flask
from flask import request
app=Flask(__name__)

from Controllers.dataController import handle_data
from Controllers.userController import add_user
from Config.db import database


database.connect()

@app.route('/data',methods=['POST'])
def data_modeling():
    response=handle_data()
    return response

@app.route('/adduser',methods=['POST'])
def post_user():
    response=add_user()
    return response
if __name__=='__main__':
    app.run()