from dotenv import load_dotenv
import os

load_dotenv()
uri=os.getenv('NEO4J_URI')
user=os.getenv('NEO4J_USER')
password=os.getenv('NEO4J_PASS')

database_url=f'neo4j+s://{user}:{password}@{uri}'

#database=Recommendation(uri,user,password)
#database=DB_UTILS(uri,user,password)
