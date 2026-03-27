import os
from dotenv import load_dotenv
import aiosqlite

load_dotenv()
DB_NAME = os.getenv("DATABASE_URL")
async def init_db():
		async with aiosqlite.connect(DB_NAME) as db:
			await db.execute("CREATE TABLE IF NOT EXISTS Locations(SlNo INTEGER PRIMARY KEY AUTOINCREMENT, City_Name TEXT UNIQUE NOT NULL, STATE TEXT, COUNTRY TEXT, LATITUDE FLOAT, LONGITUDE FLOAT,TEMPERATURE FLOAT, WINDSPEED FLOAT)")
			await db.execute("CREATE TABLE IF NOT EXISTS students(SlNo INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, ROLL TEXT UNIQUE NOT NULL, EMAIL TEXT UNIQUE, CITY_ID NUMBER, FOREIGN KEY (CITY_ID) REFERENCES Locations (SlNo))")
			await db.commit()
async def get_db():
	db = await aiosqlite.connect(DB_NAME)
	db.row_factory = aiosqlite.Row
	try:	
		yield db
	finally:
		await db.close()
