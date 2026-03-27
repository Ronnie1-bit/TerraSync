# 🛰️ TerraSync: Context-Aware Weather Engine

**Developer:** Biplab Kumar Sethy (CSBS, PMEC)  
**Status:** v1.0 Production-Ready 

## 📌 Project Overview
**TerraSync** is a high-performance, asynchronous FastAPI backend engine designed to bridge the gap between static student records and real-time environmental data. By linking a relational SQLite database with the Open-Meteo Global API, the engine provides live weather updates based on the specific coordinates of a student's city.

### Key Features
* **Relational Architecture:** Optimized `JOIN` queries linking Students to Geo-Locations.
* **Asynchronous Core:** Built with `httpx` and `aiosqlite` for high-concurrency, non-blocking I/O.
* **Real-Time Integration:** Live temperature and wind speed fetching from Open-Meteo.
* **Automated Validation:** Strict data typing and serialization via Pydantic v2.
* **Environment Security:** Secure credential management using `.env` configurations.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** SQLite (Async via aiosqlite)
* **API Client:** HTTPX
* **Testing:** Pytest & TestClient

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/biplab-sethy/terra-sync.git
cd terra-sync
pip install -r requirements.txt
2. Environment Configuration
Create a .env file in the root directory (refer to .env.example):

Plaintext
DATABASE_URL=WeatherDatabase.db
WEATHER_API_URL=https://api.open-meteo.com/v1/forecast
3. Run the Engine
Bash
uvicorn main:app --reload
Navigate to http://127.0.0.1:8000/docs for the Interactive Swagger UI.

📊 API Endpoints
Method	|   Endpoint	           |   Description
POST	|/weather/submit-name      |  Register students and city coordinates
GET	    |/weather/{name}	       |  Fetch student info + live weather data
GET	    |/weather/summary	       |  Statistical breakdown of students per city
PUT	    |/weather/update/{roll_no} |  Update student Name/Email
DELETE	|/weather/delete/{name}    |  Remove a student record
🧪 Testing
Run the automated test suite to verify endpoint integrity:
pytest test_main.py
Developed by Biplab Kumar Sethy as a high-performance backend solution.
