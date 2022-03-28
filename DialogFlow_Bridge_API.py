import json
import os
import requests
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)
bbCookie = 'JSESSIONID=50C8210A1AA7B9676838C0FB487A9815; BbClientCalenderTimeZone=Europe/Istanbul; _ga=GA1.2.2058180768.1642191272; COOKIE_CONSENT_ACCEPTED=true; _gid=GA1.2.469442000.1645955476; samlSessionId=DE9078FAA635BB3E70FE88A28953DB77; web_client_cache_guid=be22ac8e-e5a6-4c96-85c3-809287b62c36; AWSELB=15930FCF147AB7005D5D43BA193A723698D0BF514AB1E79504837DF78E4FC59F65368580D5EA5667473A3DE24CA98FC7EEA8F9F5D71A55E22CCD148F78C5CDA88E2943CB0F; AWSELBCORS=15930FCF147AB7005D5D43BA193A723698D0BF514AB1E79504837DF78E4FC59F65368580D5EA5667473A3DE24CA98FC7EEA8F9F5D71A55E22CCD148F78C5CDA88E2943CB0F; _gat=1; BbRouter=expires:1647275060,id:8D521038310A31C5A303A828E81F6A7E,signature:216aeef1df7bcad7a0188078334ae7eeb53d9a4195f0e7ec8cf3b1a3254ab4f0,site:e0b7bb72-ae0a-4562-b29a-33d3752d1b8c,timeout:10800,user:4e43a1e4e37c4d61ae4ab93f27953744,v:2,xsrf:fb194562-65b5-4a18-988d-332e3aee58e3'

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
        courseCode = parameters['course_code']
        courseCode = courseCode.upper()
        URL = 'https://psa-demo.alkanakisu.repl.co/getCourseID'
        PARAMS = {'courseName':courseCode}
        HEADERS = {'Cookie':bbCookie}
        r = requests.get(url = URL, params = PARAMS, headers=HEADERS)
        data = r.json()
        res = getCourseGradeResult(data['courseId'])
        return res
    if req.get("queryResult").get("action") == "campus_weather":
        r = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=41.205&lon=29.072&appid=281ea0b2304d240d44844f9a2e3f3440")
        data = r.json()
        return data['weather']['main'] + data['main']['temp']
    print("Please check the action in DialogFlow")
    return {}



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
