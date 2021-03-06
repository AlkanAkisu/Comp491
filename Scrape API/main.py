from flask import Flask, request,make_response
from replit import web
from BlackBoardAPI import BlackBoardAPI
from KusisAPI import KusisAPI
import json
from urllib.request import urlopen


# Create a flask app
app = Flask(__name__)

@app.route('/')
def hello():
  return 'hello'
  
# Index page
@app.route('/allCourses')
def getAllCourses():
  '''
  Gets all courses from blackboard API
  Return all courses as JSON
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
  Gets the course ID of a certain course with arguments courseName and header Cookie
  Returns the course ID as JSON
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
  Gets the grade of a certain course id
  Returns the grade of a course as JSON
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
  It gets from and to values as headers and gets the cookie and creates calendar events
  Returns the calendar events as JSON
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
  It gets the letter grade of a certain course by taking the cookie as header
  Returns the letter grade as JSON
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
  It gets the GPA information of a student by taking the cookie as header
  Returns the GPA as JSON
  '''        
  cookie = request.headers.get('Cookie')
  records = KusisAPI(cookie).getGPA()
  json_string = json.dumps(records)
  r = make_response( json_string )
  r.mimetype = 'application/json'
  # print(json_string)
  return r
  
web.run(app)
