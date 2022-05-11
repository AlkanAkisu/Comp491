import json
import requests
from bs4 import BeautifulSoup


class KusisAPI:

    def __init__(self, cookie) -> None:
        self.cookie = cookie

    def getLetterGrades(self):

        url = "https://kusis.ku.edu.tr/psc/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&PortalContentURL=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&PortalContentProvider=SA&PortalCRefLabel=My%20Course%20History&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fkusis.ku.edu.tr%2fpsp%2fps%2f&PortalURI=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2f&PortalHostNode=SA&NoCrumbs=yes&PortalKeyStruct=yes"

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
            'Referer': 'https://kusis.ku.edu.tr/psp/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder',
            'Accept-Language': 'tr',
            'Cookie': self.cookie
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select('.PSLEVEL1GRIDWBO')[-1]
        courses = table.select('[valign]')
        coursesData = []
        for course in courses:
            courseData = []
            for td in course.select('td'):
                cleanStr = td.text.replace('\n', '')
                if cleanStr == '':
                    continue
                courseData.append(cleanStr)
            coursesData.append(courseData)

        records = []
        for data in coursesData:
            code, name, semester, grade, credits, *other = data
            record = AcademicRecord(code, name, semester, grade, credits)
            records.append(record)
            
        return records
        # json_string = json.dumps([record.__dict__ for record in records])
        # print(json_string)

        # //*[@id="trCRSE_HIST$0_row6"]
    def getGPA(self):

        url = "https://kusis.ku.edu.tr/psc/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&PortalContentURL=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2fEMPLOYEE%2fSA%2fc%2fSA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL&PortalContentProvider=SA&PortalCRefLabel=My%20Course%20History&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2fkusis.ku.edu.tr%2fpsp%2fps%2f&PortalURI=https%3a%2f%2fkusis.ku.edu.tr%2fpsc%2fps%2f&PortalHostNode=SA&NoCrumbs=yes&PortalKeyStruct=yes"

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
            'Referer': 'https://kusis.ku.edu.tr/psp/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HCCC_ACADEMIC_RECORDS.HC_SSS_MY_CRSEHIST_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder',
            'Accept-Language': 'tr',
            'Cookie': self.cookie
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.select('#win0divKU_AH_EDHIST_VW\\$0')[0]
        gpa = table.findChildren('tr')[-1].findChildren('td')[-1].text.strip()
        return {'gpa': gpa}
        

class AcademicRecord:
    def __init__(self, code, name, semester, grade, credits) -> None:
        self.code = code
        self.name = name
        self.semster = semester
        self.grade = grade
        self.credits = credits
