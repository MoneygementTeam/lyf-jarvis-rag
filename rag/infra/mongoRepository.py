import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

username = 'danal'
password = 'ekskfakstp1!'
uri = f"mongodb+srv://{username}:{password}@cluster0.adxu3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.recommendations_db
collection = db.recommendations

def findByQuery(command: str):
    data = list(collection.find({}))
    return data

