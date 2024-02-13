import requests, uuid, json
from dotenv import load_dotenv
import os
load_dotenv()


class Translator:
    _instance = None   
    constructed_url=None
    params=None
    headers=None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        translator_key=os.getenv('TRANSLATOR_KEY')
        key = translator_key
        endpoint = "https://api.cognitive.microsofttranslator.com"
        location = "uksouth"
        path = '/translate'
        self.constructed_url = endpoint + path
        self.params = {
            'api-version': '3.0',
            'from': 'ro',
            'to': 'en'
        }
        self.headers = {
            'Ocp-Apim-Subscription-Key': key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

    def translate(self,text):
        body = [{
            'text': text
        }]

        request = requests.post(self.constructed_url, params=self.params, headers=self.headers, json=body)
        response = request.json()

        translated_text=response[0]['translations'][0]['text']
        
        return translated_text