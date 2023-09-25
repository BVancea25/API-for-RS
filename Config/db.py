from dotenv import load_dotenv
from db_utils import DB_UTILS
from RecEngine.recommendation import Recommendation
import os

load_dotenv()
uri=os.getenv('NEO4J_URI')
user=os.getenv('NEO4J_USER')
password=os.getenv('NEO4J_PASS')

database=Recommendation(uri,user,password)
#database=DB_UTILS(uri,user,password)
