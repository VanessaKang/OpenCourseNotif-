#############################
# Name: Vanessa Kang
# Date started: September 30, 2017
# Purpose: Determine when a course is open or closed for enrollment and notify user when the course is availiable for Enrollment
# Version: 4
#############################

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import xlrd
import os.path


# This goes into Mosaic and gets a list of courses as a array


def getCourseDetails(login_url, request_url, payload):
    with requests.Session() as session:
        # Logs in using your credentials and creates a session where you stay logged in
        post = session.post(login_url, data=payload)

        # Navigate to McMaster Enrollment Cart Page
        enroll_page = session.get(request_url)

        # Getting Beautiful Soup to parse through the HTML content
        soup = BeautifulSoup(enroll_page.text, 'html.parser')

        courseDetails = []
        # This looks for the Enrollment Table and parse values from there
        for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):

            # Parsing HTML to get course details
            courseName = ss.find(id=lambda value: value and value.startswith("P_CLASS_NAME$")).get_text(" ", strip=True)
            courseTime = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_SCHED_LONG$")).get_text("", strip=True)
            courseLocation = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_LOC_LONG$")).get_text("", strip=True)
            courseTeacher = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_INSTR_LONG$")).get_text("", strip=True)
            courseUnits = ss.find(id=lambda value: value and value.startswith("win0divSSR_REGFORM_VW_UNT_TAKEN$")).get_text("", strip=True)
            courseStatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')

            oneCourse = [courseName, courseTime, courseLocation, courseTeacher, courseUnits, courseStatus]
            # Creates a nested array of each course
            courseDetails.append(oneCourse)

    return courseDetails

# Excel Initialization


def excelInitialization(courseDetails):
    wb = Workbook()
    sheet1 = wb.add_sheet("Courses")
    attribute = ["Course", "Time", "Room Number", "Teacher", "Units", "Status"]
    for i in range(0, 6):
        sheet1.col(i).width = 7000
        sheet1.write(1, i, attribute[i])

    # Initialize first row as 2 since the first row is taken up by Headers in the CourseTracker.xls
    eachrow = 2

    # Writes each courses detail in the enrollment cart into a excel file
    for row in courseDetails:
        eachcol = 0
        for col in row:
            sheet1.write(eachrow, eachcol, col)
            eachcol += 1
        eachrow += 1

    wb.save("coursetracker.xls")


def courseChecker(courseDetails):

    # Opens and read from Courses Sheet in Excel File (coursetracker.xls)
    book = xlrd.open_workbook("coursetracker.xls")
    courseSheet = book.sheet_by_index(0)

    # Checks the number of rows and columns in Coursetracker.xls
    rowNumber = courseSheet.nrows
    colNumber = courseSheet.ncols

    # Create a nested list of course details from excel file (coursetracker.xls)
    # Note: Course details from Mosaic Enrollment Cart is also a nested list
    sheetDetails = []
    for i in range(2, rowNumber):
        sheetDetails.append(courseSheet.row_values(i))

    # Compares course details in logged file (coursetracker.xls) with Mosaic Enrollment Cart
    for j in range(0, rowNumber - 2):

        # Checks if logged COURSENAME is in Mosaic Shopping Cart nested list
        if any(sheetDetails[j][0] in item for item in courseDetails):

            # Once COURSENAME is found, check the status of it on Mosaic to the logged file
            if sheetDetails[j][5] == courseDetails[j][5]:

                # Send no text message if status has not changed
                print("Nothing Changed")

            else:
                # Send text message that status of course has changed
                print("Something Changed")

        else:
            print("Course: %s , that was previously logged is no longer in your Shopping Cart" % (sheetDetails[j][0]))


if __name__ == "__main__":
    # Ask User for Credentials Here
    macid = input("What is your MacID?: ")
    password = input("What is your password?: ")
    studentnumber = input("Student Number (exclude leading zeros): ")

    # This is the login url needed to get onto Mosaic
    login_url = "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG"

    # This is the url of the enrollment shopping cart Winter 2018 (Frame Source)
    request_url = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UGRD&EMPLID=" + str(studentnumber) + "&INSTITUTION=MCMST&STRM=2181&TargetFrameName=None"

    # This includes the name and password to get onto the site
    payload = {'userid': macid, 'pwd': password}

    courseDetails = getCourseDetails(login_url, request_url, payload)

    if os.path.isfile("coursetracker.xls"):
        courseChecker(courseDetails)
    else:
        excelInitialization(courseDetails)
        print("\nYour Enrollment cart is now been logged.\nYou will receive a text message if anything changes\n")
