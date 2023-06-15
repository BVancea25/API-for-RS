from dotenv import load_dotenv
from db_utils import DB_UTILS
import os

load_dotenv()
uri=os.getenv('NEO4J_URI')
user=os.getenv('NEO4J_USER')
password=os.getenv('NEO4J_PASS')
database=DB_UTILS(uri,user,password)
