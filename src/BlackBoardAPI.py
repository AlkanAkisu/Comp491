import requests
import re
from bs4 import BeautifulSoup
import datetime
import json

'''
This is the BlackBoard API for the BlackBoard related requests such as calendar events and course grades
'''
class BlackBoardAPI:

    def __init__(self, cookie: str):
        self.cookie = cookie

    def getAllCourses(self):
        '''
        It gets the all courses from Blackboard and returns the courses as list
        
        :return: the courses list
        :rtype: list
        '''

        url = 'https://ku.blackboard.com/webapps/portal/execute/tabs/tabAction'

        payload = "action=refreshAjaxModule&modId=_22_1&tabId=_2_1&tab_tab_group_id=_2_1"
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'X-Prototype-Version': '1.7',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-GPC': '1',
            'Origin': 'https://ku.blackboard.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ku.blackboard.com/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_2_1',
            'Accept-Language': 'tr',
            'Cookie': self.cookie
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # self.cookie = response.cookies
        soup = BeautifulSoup(response.text[43:-18], 'html.parser')
        courses = []

        for link in soup.find_all('a'):
            course_re = re.search('(?<=Course&id=).*(?=&)', link.get('href'))
            if course_re == None:
                continue

            course_id = course_re[0]
            course_name = link.get_text()
            newCourse = Course(
                course_id.strip(),
                course_name.split(':')[1].strip(),
                course_name.split(':')[0].split('-')[0].strip(),
                course_name.split(':')[0].split('-')[1].strip(),
                course_name.split(':')[0].split('-')[2].strip(),
            )
            courses.append(newCourse)
        return courses

    def getGrades(self, courseID):
        '''
        It gets the grades of a certain course from Blackboard and returns the grades as list

        :param int courseID: The course id for the wanted course grade
        :return: the grade for given course id
        :rtype: int
        '''

        url = f"https://ku.blackboard.com/webapps/bb-mygrades-BB5f0295f0bb494/myGrades?course_id={courseID}&stream_name=mygrades"

        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-GPC': '1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://ku.blackboard.com/webapps/streamViewer/streamViewer?cmd=view&streamName=mygrades&globalNavigation=false',
            'Accept-Language': 'tr',
            'Cookie': self.cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.select('div[role=row]')

        grades = []
        for div in divs[1:-2]:
            contents = div.contents[2:]
            contentsTexts = [content.getText().strip()
                             for content in contents if content.getText().strip() != ""]

            texts = contentsTexts[0].split('\n')
            texts = [string.strip() for string in texts if string != ""]

            name = texts[0]
            due = texts[1][5:] if len(texts) > 2 else None
            type = texts[-1] if len(texts) >= 2 else None
            # print('Name:', name, 'Due', due, 'Type', type)

            if len(contentsTexts[1].split('\n')) == 1:
                [lastActivity, state] = [-1, contentsTexts[1]]
            else:
                [lastActivity, state] = contentsTexts[1].split('\n')

            if len(contentsTexts) == 3:
                # needs grading
                print(contentsTexts)
                [grade, maxGrade] = contentsTexts[2].split('/')
            else:
                [grade, maxGrade] = [-1, -1]

            # print(name, type, lastActivity, state, grade, '/', maxGrade)
            grades.append(Grade(name, type, due, state,
                          lastActivity, grade, maxGrade))
        return grades

    def getCalendarEvents(self, from_date_ms, to_date_ms):
        '''
        It gets the calendar events from Blackboard and returns the calendar events as JSON

        :param str from_date_ms: start date of calendar date interval
        :param str to_date_ms: end date of calendar date interval
        :return: the calendar events on the given interval
        :rtype: JSON
        '''

        url = f"https://ku.blackboard.com/webapps/calendar/calendarData/selectedCalendarEvents?start={from_date_ms}&end={to_date_ms}&mode=personal"
        # print(url)
        payload = {}
        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-GPC': '1',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ku.blackboard.com/webapps/calendar/viewPersonal',
            'Accept-Language': 'tr',
            'Cookie': self.cookie
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()


class Grade:
    def __init__(self, name, type, due, state, lastActivity, grade, maxGrade) -> None:
        self.name = name
        self.type = type
        self.due = due
        self.state = state
        self.lastActivity = lastActivity
        self.grade = grade
        self.maxGrade = maxGrade
        pass

    def __str__(self):
        return f'{self.name} TYPE:{self.type} DUE:{self.due} STATE:{self.state} LAST:{self.lastActivity} GRADE:{self.grade}/{self.maxGrade}'

    def print(self):
        print(f'{self.name} {self.type} {self.due} {self.state} {self.lastActivity} {self.grade}/{self.maxGrade}')


class Course:
    def __init__(self, courseID, courseName, courseCode, courseSemester, courseSection):
        self.courseID = courseID
        self.courseName = courseName
        self.courseCode = courseCode
        self.courseSemester = courseSemester
        self.courseSection = courseSection

    def __str__(self) -> str:
        return f'''
        ID: {self.courseID}
        Course Code - Section: {self.courseCode} - {self.courseSection}
        Name: {self.courseName}
        Semester: {self.courseSemester}
        '''
    
