import json
import os
import requests
from flask import Flask
from flask import request
from flask import make_response
import pymongo
import datetime
from replit import web

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://kusistantt:Av8zzmtP3uiCbj3p@cluster0.bkabe.mongodb.net")
mydb = myclient["userDB"]
mycol = mydb["users"]

userID = 0

userInfo = mycol.find_one({'id':3094})

print(userInfo)

bbCookie = str(userInfo['bbCookie'])
KUSISCookie = str(userInfo['kusisCookie'])

print(bbCookie)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("queryResult").get("action") == "coursegrade":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        courseCode = parameters['course_code'].upper()
        URL = 'https://comp491.alkanakisu.repl.co/getCourseID'
        PARAMS = {'courseName':courseCode}
        HEADERS = {'Cookie':bbCookie}
        r = requests.get(url = URL, params = PARAMS, headers=HEADERS)
        data = r.json()
        res = getCourseGradeResult(data['courseId'])
        return res
    elif req.get("queryResult").get("action") == "lettergrade":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        courseCode = parameters['course_code'].upper()
        URL = 'https://comp491.alkanakisu.repl.co/letterGrades'
        HEADERS = {'Cookie':KUSISCookie}
        r = requests.get(url = URL, headers=HEADERS)
        data = r.json()
        res = getLetterGrade(data, courseCode)
        return res
    elif req.get("queryResult").get("action") == "calendarevents":
        URL = 'https://comp491.alkanakisu.repl.co/calendarEvents'
        HEADERS = {'Cookie':bbCookie}
        currTime, endTime = setBetweenDates()
        PARAMS = {'from':currTime, 'to':endTime}
        r = requests.get(url = URL, params=PARAMS, headers=HEADERS)
        data = r.json()
        res = getCalendarEvents(data)
        return res
    elif req.get("queryResult").get("action") == "getgpa":
        URL = 'https://comp491.alkanakisu.repl.co/gpa'
        HEADERS = {'Cookie':KUSISCookie}
        r = requests.get(url = URL, headers=HEADERS)
        data = r.json()
        print(data)
        res = getGPA(data)
        return res
    elif req.get("queryResult").get("action") == "campus_weather":
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=41.205&longitude=29.072&daily=temperature_2m_max,temperature_2m_min&timezone=Europe%2FMoscow")
        data = r.json()
        res = getWeatherInfo(data)
        return res

    print("Please check the action in DialogFlow")
    return {}

def getWeatherInfo(data):
    maxTemp = data['daily']['temperature_2m_max'][0]
    minTemp = data['daily']['temperature_2m_min'][0]
    weatherData = f"Max Temp: {maxTemp} / Min Temp: {minTemp}"
    return {"fulfillmentText": weatherData}

def getGPA(data):
    GPA = data['gpa']
    print("Your gpa is: ", GPA)
    return {"fulfillmentText": GPA}

def setBetweenDates():
    currTime = datetime.datetime.now()
    endTime = currTime + datetime.timedelta(days=14)
    return int(currTime.timestamp())*1000, int(endTime.timestamp())*1000

def getCalendarEvents(data):
    results = []
    for event in data:
        dateAndTime = event['endDate'].split('T')[0] + " / " +(event['endDate'].split('T')[1]).split('.')[0]
        results.append(f"Course: {event['calendarId'].split('-')[0]}<\br>Assignment Name: {event['title']}<\br>Due Date: {dateAndTime}")
    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": results
      }
    }
  ]
}



def getLetterGrade(data, courseCode):
    letterGrade = " "
    for course in data:
        if course['code'].replace(" ", "") == courseCode:
            letterGrade = course['grade']
    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": [
            letterGrade
          ]
      }
    }
  ]
}

def getCourseGradeResult(courseId):
    URL = 'https://comp491.alkanakisu.repl.co/mygrades/'+str(courseId)
    HEADERS = {'Cookie':bbCookie}
    r = requests.get(url = URL, headers=HEADERS)
    data = r.json()
    gradeList = []
    for item in data:
        gradeList.append(f"{item['name']}: {item['grade']}/{item['maxGrade']}\n")

    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": gradeList
      }
    }
  ]
}

@app.route('/test', methods=['GET'])
def test():
    return "Hello"


web.run(app)
