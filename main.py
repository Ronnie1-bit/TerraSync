from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from database import get_db, init_db
from service import get_weather
from pydantic import Field, BaseModel
from typing import List
app = FastAPI(
    title="TerraSync Weather Engine",
    description="A high-performance asynchronous API for real-time weather analytics and student data management.",
    version="1.0.0",
    contact={
        "name": "Biplab Kumar Sethy",
        "url": "https://github.com/Ronnie1-bit",
    },
)
class StudentCurrentWeather(BaseModel):
    name : str = Field(..., min_length = 1, description = "Name Must Contain At least 1 letter")
    roll_no: int = Field(..., gt=0, description = "RollNo must be greater than 1")
    email: str = Field(..., max_length = 50, description = "Email (Max_length = 10)")
    city_name : str = Field(..., max_length =50, description = "City Name Must be Mentioned")
    state : str = Field(..., max_length = 50, description = "State Must be Mentioned")
    country: str = Field(..., max_length = 50, description = "Country Must be Mentioned")
    lat: float = Field(..., description="Latitude of the city")
    lon: float = Field(..., description="Longitude of the city")
@app.on_event("startup")
async def startup_event():
    await init_db()
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
@app.post("/weather/submit-name", status_code = status.HTTP_201_CREATED)
async def write(students: List[StudentCurrentWeather], db = Depends(get_db)):
    for s in students:
        await db.execute("INSERT OR IGNORE INTO Locations (City_Name, STATE, COUNTRY, LATITUDE, LONGITUDE) VALUES (?, ?, ?, ?, ?)",(s.city_name, s.state, s.country, s.lat, s.lon))
        cursor = await db.execute("SELECT SlNo FROM Locations WHERE City_Name = ?", (s.city_name,))
        city_row = await cursor.fetchone()
        city_id = city_row[0]
        await db.execute("INSERT INTO students (Name, ROLL, EMAIL, city_id) VALUES (?, ?, ?, ?)",(s.name, str(s.roll_no), s.email, city_id))
    await db.commit()
    return{"message": "Posted Successfully"}
@app.get("/weather/{name}", status_code = status.HTTP_200_OK)
async def read(name : str ,db = Depends(get_db)):
    cursor = await db.execute("SELECT Locations.CITY_NAME, students.Name, Locations.STATE,Locations.LATITUDE, Locations.LONGITUDE FROM students JOIN Locations ON students.CITY_ID = Locations.SlNo WHERE students.Name=?", (name,))
    rex = await cursor.fetchone()
    if rex is None:
        raise HTTPException(status_code= 404, detail= "Not Found")
    live_data = await get_weather(rex["LATITUDE"], rex["LONGITUDE"])
    return {"message": f"City Name: {rex[0]}, Student Name: {rex[1]}, State: {rex[2]}", "Weather_update": live_data}
@app.get("/weather/summary", status_code = status.HTTP_200_OK)
async def summary(db = Depends(get_db)):
    cursor = await db.execute("SELECT L.CITY_NAME, L.STATE, COUNT (S.SlNo) as Total_Students FROM Locations L LEFT JOIN students S ON L.SlNo = S.CITY_ID  GROUP BY L.CITY_NAME")
    rex = await cursor.fetchall()
    if not rex:
        raise HTTPException(status_code = 404, detail = "Not Found")
    return[{"analysis": f"According to the Analysis, city {row['City_Name']}","total_students": row['Total_Students']} for row in rex]
@app.put("/weather/update/{roll_no}", status_code = status.HTTP_200_OK)
async def updation(Student: StudentCurrentWeather,roll_no: int, db= Depends(get_db)):
    rex = await db.execute("SELECT 1 FROM students WHERE ROLL = ?",(str(roll_no),))
    result = await rex.fetchone()
    if result is None: 
        raise HTTPException(status_code = 404, detail = "NOT FOUND")
    await db.execute("UPDATE students SET NAME =?, EMAIL = ? WHERE ROLL = ? ",(Student.name ,Student.email,str(roll_no),))
    await db.commit()
    return{"message":"Update Successfully"}
@app.delete("/weather/delete/{name}")
async def delete(name: str, db = Depends(get_db)):
    await db.execute("DELETE FROM students WHERE Name=?",(name,))
    await db.commit()
    return{"message": "Deleted Successfully"}
