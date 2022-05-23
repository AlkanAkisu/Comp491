from flask import Flask, request,make_response
from replit import web
from BlackBoardAPI import BlackBoardAPI
from KusisAPI import KusisAPI
import json
from urllib.request import urlopen

'''
This is the main code for the request handling of KUSIS and BlackBoard APIs
'''

# Create a flask app
app = Flask(__name__)

@app.route('/')
def hello():
  return 'hello'
  
# Index page
@app.route('/allCourses')
def getAllCourses():
  '''
  It gets the all courses from Blackboard and returns the courses

  :return: the courses list
  :rtype: JSON
  '''
  cookie = request.headers.get('Cookie')
  bb_API = BlackBoardAPI(cookie)
  courses = bb_API.getAllCourses()
  json_string = json.dumps([ob.__dict__ for ob in courses])
  r = make_response( json_string )
  r.mimetype = 'application/json'
  return r

@app.route('/getCourseID')
def getCourseID():
  '''
  It gets the course ID of a certain course from Blackboard and returns it

  :return: the dictionary element mapped to course id
  :rtype: dict
  '''  
    
  courseCode = request.args.get('courseName')
  cookie = request.headers.get('Cookie')
  bb_API = BlackBoardAPI(cookie)
  courses = bb_API.getAllCourses()
  foundCourse = None
  for course in courses:
    if course.courseCode == courseCode:
      if course.courseSection.isdigit():
        foundCourse = course
        break
  if foundCourse == None:
    return {
      "courseId": -1
    }
  return {
    "courseId": foundCourse.courseID
  } 
  
@app.route('/mygrades/<course_id>')
def getGrade(course_id):
  '''
  It gets the grades of a certain course from Blackboard and returns the grades

  :param int courseID: The course id for the wanted course grade
  :return: the grade for given course id
  :rtype: JSON
  '''   
  cookie = request.headers.get('Cookie')
  bb_API = BlackBoardAPI(cookie)
  grades = bb_API.getGrades(course_id)
  
  json_string = json.dumps([ob.__dict__ for ob in grades])
  
  r = make_response( json_string )
  r.mimetype = 'application/json'
  return r
  
@app.route('/calendarEvents')
def getCalendarEvent():
  '''
  It gets the calendar events from Blackboard and returns the calendar events

  :return: the calendar events on the given interval
  :rtype: JSON
  '''      
  cookie = request.headers.get('Cookie')
  
  from_ms = request.args.get('from')
  to_ms = request.args.get('to')
  
  bb_API = BlackBoardAPI(cookie)
  events = bb_API.getCalendarEvents(from_ms, to_ms)
  json_string = json.dumps(events)
  r = make_response( json_string )
  r.mimetype = 'application/json'
  return r
  
@app.route('/letterGrades')
def getLetterGrades():
  '''
  It gets the letter grades of a certain course from KUSIS and returns the grades

  :return: the grade for given course id
  :rtype: JSON
  '''      
  cookie = request.headers.get('Cookie')
  records = KusisAPI(cookie).getLetterGrades()
  json_string = json.dumps([record.__dict__ for record in records])
  r = make_response( json_string )
  r.mimetype = 'application/json'
  return r
  
@app.route('/gpa')
def getGPA():
  '''
  It gets the GPA from KUSIS and returns it

  :return: the GPA
  :rtype: JSON
  '''         
  cookie = request.headers.get('Cookie')
  records = KusisAPI(cookie).getGPA()
  json_string = json.dumps(records)
  r = make_response( json_string )
  r.mimetype = 'application/json'
  # print(json_string)
  return r
  
web.run(app)
