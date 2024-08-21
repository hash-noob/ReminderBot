import requests
import pytz
from datetime import datetime


class event:
    def __init__(self,title,time,duration,starts_in,url):
        self.title = title
        self.time = time
        self.duration = duration
        self.starts_in = starts_in
        self.url = url

class active_event:
    def __init__(self,title,duration,url,endsAt):
        self.title = title
        self.duration = duration
        self.url = url
        self.endsAt = endsAt

def convertTimetoLocal(date_str):
    date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    utc_timezone = pytz.utc
    date_object_utc = utc_timezone.localize(date_object)

    ist_timezone = pytz.timezone("Asia/Kolkata")
    date_object_ist = date_object_utc.astimezone(ist_timezone)

    formatted_date_ist = date_object_ist.strftime("%d-%m-%Y %A %I:%M:%S %p")

    return formatted_date_ist

def upcomingContest():
    extracted_data = requests.get("https://smartinterviews.in/api/contest/getContestsList")
    if extracted_data.status_code == 200:
        data = extracted_data.json()["data"]
        ongoingContests = data["ongoingContestsList"]
        upcomingContest = data["upcomingContestsList"]

        upc_contests=[]
        ong_contests=[]

        for contest in upcomingContest:
            c = event(contest["host"]+" "+contest["title"]
                    ,convertTimetoLocal(contest["startTime"])
                    ,contest["duration"]
                    ,contest["startsIn"]
                    ,contest["url"])
            if "days" in c.starts_in and int(c.starts_in.split("days")[0])>7:
                break
            upc_contests.append(c)
        
        for contest in ongoingContests:
            c = active_event(contest["host"]+" "+contest["title"]
                            ,contest["duration"]
                            ,contest["url"]
                            ,convertTimetoLocal(contest["endTime"]))
            ong_contests.append(c)
        
        return [upc_contests,ong_contests]
    else:
        return "Unable to fetch the data"





