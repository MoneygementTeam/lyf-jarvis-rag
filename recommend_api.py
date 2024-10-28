import os

import certifi
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from rag.service.ragService import ragService

MAPPING_EN2KO = {
    "hangover": "해장",
    "diet": "다이어트"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}

app = FastAPI()

username = 'danal'
password = 'ekskfakstp1!'
uri = f"mongodb+srv://{username}:{password}@cluster0.adxu3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.recommendations_db
collection = db.recommendations


@app.get("/health")
def health():
    return "OK"


@app.get("/recommend/{query_en}")
def recommend(query_en: str = "hangover"):
    query_ko = MAPPING_EN2KO[query_en]
    data = list(collection.find({"_id": query_ko}, {'_id': 0}))
    return data



class Command(BaseModel):
    command: str



@app.post("/openai")
def openai(command: Command):
    print(f"command ${command}!!!!!!")

    client = OpenAI(
        api_key=os.getenv("api_key"))

    completion = client.chat.completions.create(
        model='gpt-4o-2024-08-06',
        messages=[{'role': 'user', 'content': command.command}],
        temperature=0.0
    )
    return completion.choices[0].message.content



class Recommend(BaseModel):
    userId: str
    command: str
    latitude : float
    longitude: float
    weather: str



@app.post("/recommend")
def openaiFunction(request: Recommend):
    result = ragService(request)
    return result