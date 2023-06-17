from flask import request,jsonify
from Config.db import database
from RecEngine.regex import extract_characteristics,extract_description
from googletrans import Translator
import numpy as np
from RecEngine.description_embeddings import Embedding

def add_product():
   vectorizer=Embedding()#initializam clasa Embedding
   req=request.get_json()
   if 'id' not in req :
      return jsonify({'message':'Missing id'}),400
   if 'html' not in req :
      return jsonify({'message':'Missing html'}),400
   try:
      description=extract_description(req['html'])#extragem descrierea
      print("Ceva")
      translated_description=translate_text(description,"en")#traducem descrierea
      print("Ceva")
      data=extract_characteristics(req['html'])#extragem caracteristicile
      print("Ceva")
      embedding=vectorizer.get_embedding(translated_description)#vectorizam descrierea
      print("Ceva")
      embedding.tolist()
      print("Ceva")
      flattened_embedding = [item for sublist in embedding for item in sublist]#transformam lista de liste intr-o lista
      print("Ceva")
      data['embedding']=flattened_embedding
      data['id']=req['id']
      data['profile']=[]
      print(data)
      database.create_node("Item",data)
      return jsonify({'message':'ceva'}),200
   except Exception as e:
            print(f"An error occurred while creating the node: {e}")
            return jsonify({"error":f"An error occurred while creating the node: {e}"}),400

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text