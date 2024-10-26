from fastapi import FastAPI, HTTPException
import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
uri = f"mongodb+srv://{username}:{password}@cluster0.adxu3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())

db = client.weather_database
collection = db.weather_data

app = FastAPI()


# Pydantic 모델 설정
class WeatherData(BaseModel):
    temp: float
    feels_like: float
    weather: str
    description: str
    humidity: int
    wind_speed: float
    wind_deg: int
    city: str
    country: str

    class Config:
        orm_mode = True


@app.post("/weather/")
async def save_weather_data(data: WeatherData):
    weather_dict = {}
    result = await collection.insert_one(weather_dict)

    if result.inserted_id:
        return {"message": "Weather data saved successfully", "id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to save weather data")


@app.get("/weather/{city}", response_model=List[WeatherData])
async def get_weather_data(city: str):
    weather_cursor = collection.find({"city": city})
    weather_data = await weather_cursor.to_list(length=100)

    if weather_data:
        return weather_data
    else:
        raise HTTPException(status_code=404, detail="Weather data not found for the given city")
