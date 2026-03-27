import os
from dotenv import load_dotenv
import httpx
load_dotenv()
BASE_URL = os.getenv("WEATHER_API_URL")
async def get_weather(lat: float, lon: float):
    url = f"{BASE_URL}?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code== 200:
            data = response.json()
            temp= data["current_weather"]["temperature"]
            wind = data["current_weather"]["windspeed"] 
            return{"Temperature":f"{temp}degrees","Wind Speed": f"{wind}km/h"}
        else:
            return {"ERROR": "Data was not fetched"}