import json
import os
import requests
from flask import Flask
from flask import request
from flask import make_response
import pymongo
import datetime
import time

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://kusistantt:Av8zzmtP3uiCbj3p@cluster0.bkabe.mongodb.net")
mydb = myclient["userDB"]
mycol = mydb["users"]

userID = ''

bbCookie = ""
KUSISCookie = ""

'''
This is the connection between Dialogflow and Flutter application
'''


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    userID = int(req.get("session").split("/")[4])
    res = processRequest(req, userID)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req, userID):
    '''
    Posts request to the relevant API and processes the result.
    Req: JSON
    userID: Int
    Returns processed JSON
    '''
    userInfo = mycol.find_one({'id':userID})
    bbCookie = str(userInfo['bbCookie'])
    KUSISCookie = str(userInfo['kusisCookie'])
    if req.get("queryResult").get("action") == "coursegrade":
        result = req.get("queryResult")
        parameters = result.get("parameters")
        courseCode = parameters['course_code'].upper()
        URL = 'https://comp491.alkanakisu.repl.co/getCourseID'
        PARAMS = {'courseName':courseCode}
        HEADERS = {'Cookie':bbCookie}
        r = requests.get(url = URL, params = PARAMS, headers=HEADERS)
        data = r.json()
        res = getCourseGradeResult(data['courseId'], bbCookie)
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
    '''
    Processes JSON returned from weather API
    Data: JSON
    Returns max and min temperature as JSON
    '''
    maxTemp = data['daily']['temperature_2m_max'][0]
    minTemp = data['daily']['temperature_2m_min'][0]
    weatherData = f"Max Temp: {maxTemp} / Min Temp: {minTemp}"
    return {"fulfillmentText": weatherData}

def getGPA(data):
    '''
    Processes JSON from our Blackboard API to extract GPA
    Data: JSON
    Returns GPA as JSON
    '''
    GPA = data['gpa']
    print("Your gpa is: ", GPA)
    return {"fulfillmentText": f"Your GPA is {GPA}"}

def setBetweenDates():
    '''
    Returns a date range between now and next 14 days
    Returns time in millliseconds
    ''' 
    currTime = datetime.datetime.now()
    endTime = currTime + datetime.timedelta(days=14)
    return int(currTime.timestamp())*1000, int(endTime.timestamp())*1000

def getCalendarEvents(data):
    '''
    Processes JSON from our Blackboard API to extract upcoming events
    Data: JSON
    Returns JSON
    '''   
    results = []
    for event in data:
        dateAndTime = event['endDate'].split('T')[0] + " / " +(event['endDate'].split('T')[1]).split('.')[0]
        results.append(f"Course: {event['calendarId'].split('-')[0]}\nAssignment Name: {event['title']}\nDue Date: {dateAndTime}\n\n")
    result = "-> "+"-> ".join(results)
    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": [
            result
        ]
      }
    }
  ]
}



def getLetterGrade(data, courseCode):
    '''
    Processes JSON from our KUSIS API to extract letter grade of given course
    Data: JSON
    courseCode: String
    Returns letter grade as JSON
    '''    
    letterGrade = " "
    for course in data:
        if course['code'].replace(" ", "") == courseCode:
            letterGrade = course['grade']
    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": [
            f"Your letter grade for {courseCode} is {letterGrade}"
          ]
      }
    }
  ]
}

def getCourseGradeResult(courseId, bbCookie):
    '''
    Processes JSON from our Blackboard API to extract course number scores
    courseId: String
    bbCookie: String
    Returns numerical grades as JSON
    '''  
    URL = 'https://comp491.alkanakisu.repl.co/mygrades/'+str(courseId)
    HEADERS = {'Cookie':bbCookie}
    r = requests.get(url = URL, headers=HEADERS)
    data = r.json()
    gradeList = []
    for item in data:
        gradeList.append(f"{item['name']}: {item['grade']}/{item['maxGrade']}\n\n")
    result = "-> "+"-> ".join(gradeList)
    print(result)
    return {
  "fulfillmentMessages": [
    {
      "text": {
        "text": [
        result
        ]
      }
    }
  ]
}

@app.route('/test', methods=['GET'])
def test():
    return "Hello"

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
