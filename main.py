from fastapi import FastAPI
from helpers.get_station_timetable import get_station_timetable

app = FastAPI()

@app.get("/{station}")
async def root(station: str, direction: str):
    return get_station_timetable(station, "north")