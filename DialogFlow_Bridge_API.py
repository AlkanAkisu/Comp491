import json
import os
import requests
from flask import Flask
from flask import request
from flask import make_response
import datetime

app = Flask(__name__)
bbCookie = 'JSESSIONID=6062A666CC74622AB6D0F0C33C9CB9AC; COOKIE_CONSENT_ACCEPTED=true; BbClientCalenderTimeZone=Europe/Istanbul; web_client_cache_guid=db9091ea-4617-4b47-85f3-772053d54ef4; AWSELB=15930FCF147AB7005D5D43BA193A723698D0BF514A91AD1BB6A0053E8D959D1B2F8484A3D5EA5667473A3DE24CA98FC7EEA8F9F5D78460FF040B8F5F6362FBB4B396EB1EDB; AWSELBCORS=15930FCF147AB7005D5D43BA193A723698D0BF514A91AD1BB6A0053E8D959D1B2F8484A3D5EA5667473A3DE24CA98FC7EEA8F9F5D78460FF040B8F5F6362FBB4B396EB1EDB; BbRouter=expires:1648487835,id:D8AC054E8812AC5EADD1C5618FAF0155,signature:1e9699311241491c62f55c639890fcbde6bacbdbcc73ffabb243fceeadfe0c84,site:e0b7bb72-ae0a-4562-b29a-33d3752d1b8c,timeout:10800,user:ce75b4b84ccb415e9fbaff1cb9487bc6,v:2,xsrf:41e443c1-22f6-4fac-8523-33ad78abaedd'
KUSISCookie = 'kusis=3893499052.64544.0000; PS_TokenSite=https://kusis.ku.edu.tr/psc/ps/?KUSIS-58-PORTAL-PSJSESSIONID; SignOnDefault=; HPTabName=DEFAULT; HPTabNameRemote=; LastActiveTab=DEFAULT; https%3a%2f%2fkusis.ku.edu.tr%2fpsp%2fps%2femployee%2fsa%2frefresh=list:%3ftab%3dremoteunifieddashboard%7c%3frp%3dremoteunifieddashboard%7c%3fcmd%3dgetcachedpglt%26pageletname%3dadmn_ku_todo_pagelet_hmpg%26tab%3ddefault|%3ftab%3ddefault|%3frp%3ddefault; KUSIS-58-PORTAL-PSJSESSIONID=m37RTotEFpTInQpHY-TLNGn7I_15bNPB!66283370!1648484059972; PS_LOGINLIST=https://kusis.ku.edu.tr/ps; ps_theme=node:SA portal:EMPLOYEE theme_id:KU_THEME_TANGERINE accessibility:N formfactor:3 piamode:2; PS_TOKEN=qQAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4AcQg4AC4AMQAwABSN9qEHHH919m9+BErV6hA7FC6Qy2kAAAAFAFNkYXRhXXicHYtLCoAwEEOfH1yKF7Fo/WCXRVREEEFdewbv5+EMzcDLkJAXSJM4iuRfTFDh8WysnNzUOLKJnYX8UDJz8TDqay0VVlfKG9EyBFqMZo3YaWzUdsocLT38omcL2w==; ExpirePage=https://kusis.ku.edu.tr/psp/ps/; PS_LASTSITE=https://kusis.ku.edu.tr/psp/ps/; PS_DEVICEFEATURES=width:1512 height:982 pixelratio:2 touch:0 geolocation:1 websockets:1 webworkers:1 datepicker:1 dtpicker:1 timepicker:1 dnd:1 sessionstorage:1 localstorage:1 history:1 canvas:1 svg:1 postmessage:1 hc:0 maf:0; psback=%22%22url%22%3A%22https%3A%2F%2Fkusis.ku.edu.tr%2Fpsp%2Fps%2FEMPLOYEE%2FSA%2Fc%2FSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL%3FFolderPath%3DPORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL%26IsFolder%3Dfalse%26IgnoreParamTempl%3DFolderPath%252cIsFolder%22%20%22label%22%3A%22My%20Course%20History%22%20%22origin%22%3A%22PIA%22%20%22layout%22%3A%220%22%20%22refurl%22%3A%22https%3A%2F%2Fkusis.ku.edu.tr%2Fpsc%2Fps%2FEMPLOYEE%2FSA%22%22; PS_TOKENEXPIRE=28_Mar_2022_16:15:04_GMT'

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
        URL = 'https://psa-demo.alkanakisu.repl.co/getCourseID'
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
        URL = 'https://psa-demo.alkanakisu.repl.co/letterGrades'
        HEADERS = {'Cookie':KUSISCookie}
        r = requests.get(url = URL, headers=HEADERS)
        data = r.json()
        res = getLetterGrade(data, courseCode)
        return res
    elif req.get("queryResult").get("action") == "calendarevents":
        URL = 'https://psa-demo.alkanakisu.repl.co/calendarEvents'
        HEADERS = {'Cookie':bbCookie}
        currTime, endTime = setBetweenDates()
        PARAMS = {'from':currTime, 'to':endTime}
        r = requests.get(url = URL, params=PARAMS, headers=HEADERS)
        data = r.json()
        res = getCalendarEvents(data)
        return res
    elif req.get("queryResult").get("action") == "getgpa":
        URL = 'https://psa-demo.alkanakisu.repl.co/gpa'
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
    weatherData = f"{maxTemp} / {minTemp}"
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
    URL = 'https://psa-demo.alkanakisu.repl.co/mygrades/'+str(courseId)
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
