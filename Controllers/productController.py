from flask import request,jsonify
from Config.db import database
from RecEngine.regex import extract_characteristics,extract_description
from RecEngine.translator import Translator
from dotenv import load_dotenv
import os

load_dotenv()
translator_key=os.getenv('TRANSLATOR_KEY')
import numpy as np
from RecEngine.description_embeddings import Embedding

def add_product():
   vectorizer=Embedding()#initializam clasa Embedding
   translator=Translator()
   req=request.get_json()
   if 'id' not in req :
      return jsonify({'message':'Missing id'}),400
   if 'html' not in req :
      return jsonify({'message':'Missing html'}),400
   try:
      description=extract_description(req['html'])#extragem descrierea
      
      translated_description=translator.translate(description)#traducem descrierea
      
      data=extract_characteristics(req['html'])#extragem caracteristicile
      
      embedding=vectorizer.get_embedding(translated_description)#vectorizam descrierea
      data['embedding']=embedding
      data['id']=req['id']
      data['profile']=[]
      
      database.create_node("Item",data)
      return jsonify({'message':'ceva'}),200
   except Exception as e:
            print(f"An error occurred while creating the node: {e}")
            return jsonify({"error":f"An error occurred while creating the node: {e}"}),400

