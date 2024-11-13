import requests
from datetime import datetime

def get_station_timetable(station_name: str, direction: str):

    #Get station ID from station_name
    response = requests.get(f"https://api.odpt.org/api/v4/odpt:Station?dc:title={station_name}&acl:consumerKey=")

    if response.status_code == 200:
        response  = response.json()[0]
        station_id = response.get("owl:sameAs")
    else:
        return {"error": "Invalid response for station name"}

    #Get station timetable from station_id
    timetable_response = requests.get(f"https://api.odpt.org/api/v4/odpt:StationTimetable?odpt:station={station_id}&acl:consumerKey=")

    if timetable_response.status_code == 200:
        timetable_response = timetable_response.json()
        if direction == "north":
            timetable = timetable_response[0].get("odpt:stationTimetableObject")
        else:
            timetable = timetable_response[1].get("odpt:stationTimetableObject")
    else:
        return {"error": "Invalid response for station timetable"}

    #Get next train time
    #Compare current and train time in minutes to get next train
    current_time         = datetime.now().strftime("%H:%M")
    hours                = current_time.split(":")[0]
    minutes              = current_time.split(":")[1]
    current_time_minutes = int(hours) * 60 + int(minutes)

    current_closest_time = 88888888
    for train in timetable:
        next_time         = train.get("odpt:departureTime")
        hours             = next_time.split(":")[0]
        minutes           = next_time.split(":")[1]
        next_time_minutes = int(hours) * 60 + int(minutes)
        time_difference   = abs(current_time_minutes - next_time_minutes)
        if time_difference < current_closest_time:
            current_closest_time = time_difference
            next_train_time = next_time



    result = {"next_train_time": next_train_time}
    return result