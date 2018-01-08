#############################
# Name: Vanessa Kang
# Date started: September 30, 2017
# Purpose: Determine when a course is open or closed for enrollment and notify user of changes in course status (Open/Closed)
#############################

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook
import xlrd
import os.path
import os
from twilio.rest import Client
import myconfig as cfg


def getMosaicDetails(login_url, request_url, payload):
    #----------------------------------------------
    # This goes into Mosaic Enrollment Cart and creates a nested list out of each course
    #----------------------------------------------

    with requests.Session() as session:
        # Logs in using your credentials and creates a session where you stay logged in
        post = session.post(login_url, data=payload)

        # Navigate to McMaster Enrollment Cart Page
        enroll_page = session.get(request_url)

        # Getting Beautiful Soup to parse through the HTML content
        soup = BeautifulSoup(enroll_page.text, 'html.parser')

        mosaicCourseDetails = []
        # This looks for the Enrollment Table and parse values from there
        for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):

            # Parsing HTML to get course details
            courseName = ss.find(id=lambda value: value and value.startswith("P_CLASS_NAME$")).get_text(" ", strip=True)
            courseTime = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_SCHED_LONG$")).get_text("", strip=True)
            courseLocation = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_LOC_LONG$")).get_text("", strip=True)
            courseTeacher = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_INSTR_LONG$")).get_text("", strip=True)
            courseUnits = ss.find(id=lambda value: value and value.startswith("win0divSSR_REGFORM_VW_UNT_TAKEN$")).get_text("", strip=True)
            courseStatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')

            onemosaicCourseDetails = [courseName, courseTime, courseLocation, courseTeacher, courseUnits, courseStatus]
            # Creates a nested array of each course
            mosaicCourseDetails.append(onemosaicCourseDetails)

    return mosaicCourseDetails


def creatingCourseLog(mosaicCourseDetails):
    #----------------------------------------------
    # Creates an Excel file (courselogger.xls) that logs all course details from Mosaic Enrollment Cart
    # This is usually ran when the program is initially ran or
    #    if the person wants to update their log file (has to delete courselogger.xls in their directory first)
    #----------------------------------------------

    wb = Workbook()
    sheet1 = wb.add_sheet("Courses")
    attribute = ["Course", "Time", "Room Number", "Teacher", "Units", "Status"]
    for i in range(0, 6):
        sheet1.col(i).width = 7000
        sheet1.write(1, i, attribute[i])

    # Initialize first row as 2 since the first row is taken up by Headers in the courselogger.xls
    eachrow = 2

    # Writes each courses detail in the enrollment cart into a excel file
    for row in mosaicCourseDetails:
        eachcol = 0
        for col in row:
            sheet1.write(eachrow, eachcol, col)
            eachcol += 1
        eachrow += 1

    wb.save("courselog.xls")


def courseChecker(mosaicCourseDetails):
    #----------------------------------------------
    # Checks courses in logged excel file (courselogger.xls) has changed status by checking against Mosaic Enrollment Cart Status
    # If there are any changes in status (Open -> Closed) or (Closed -> Open), then text messages TO BE SENT will be returned
    #----------------------------------------------

    # Opens and read from Courses Sheet in Excel File (courselogger.xls)
    book = xlrd.open_workbook("courselog.xls")
    courseSheet = book.sheet_by_index(0)

    # Checks the number of rows and columns in courselogger.xls
    rowNumber = courseSheet.nrows
    colNumber = courseSheet.ncols

    # Create a nested list of course details from excel file (courselogger.xls)
    # NOTE: Course details from Mosaic Enrollment Cart is __ALSO__ a nested list
    loggedCourseDetails = []
    for i in range(2, rowNumber):
        loggedCourseDetails.append(courseSheet.row_values(i))

    # Text messages to be sent will be logged into this array
    twilioMessage = []

    # Compares course details in logged file (courselog.xls) with Mosaic Enrollment Cart course statuses
    for j in range(0, rowNumber - 2):
        # Checks if logged COURSENAME (in courselog.xls) is in Mosaic Shopping Cart nested list (mosaicCourseDetails)
        if any(loggedCourseDetails[j][0] in item for item in mosaicCourseDetails):
            # Once COURSENAME is found, check the status of it on Mosaic to the logged file
            if loggedCourseDetails[j][5] == mosaicCourseDetails[j][5]:
                # Send no text message if status has not changed
                continue
            else:
                # Send Status to twilio message
                twilioMessage.append("Course: %s has changed status from [%s] to [%s]" % (loggedCourseDetails[j][0], loggedCourseDetails[j][5], mosaicCourseDetails[j][5]))
                # [Make Sure to implement in the future] change logged file status once recognized
        else:
            twilioMessage.append("[Course: %s] that was previously logged is no longer in your Enrollment Cart" % (loggedCourseDetails[j][0]))

    # If nothing has been added to the TwilioMessage array from previous for loop, then nothing about course status has changed
    if len(twilioMessage) == 0:
        twilioMessage.append("There is no changes to your course status")

    return twilioMessage


def sendTwilio(twilioMessage):
    #----------------------------------------------
    # Send out Message of course change using Twilio API
    #----------------------------------------------

    # Initialze Twilio account, token and number (this has to be generated from user)
    TWILIO_ACCOUNT_SID = cfg.twilio['ACCOUNT_SID']
    TWILIO_AUTH_TOKEN = cfg.twilio['AUTH_TOKEN']
    TWILIO_FROM_NUM = cfg.twilio['FROM_NUM']
    my_number = cfg.twilio['MY_NUM']

    # Initlize Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Create String from TO BE SENT messages (twiliomessage list)
    stringTwilioMessage = "\n".join(twilioMessage)

    # Send message from Twilio account to Cell phone (in this case its mine)
    client.messages.create(
        to=my_number,
        from_=TWILIO_FROM_NUM,
        body=stringTwilioMessage
    )


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

    # This contains all details of a course from Mosaic Shopping Shopping Cart
    mosaicCourseDetails = getMosaicDetails(login_url, request_url, payload)

    # This array will log all text messages TO BE SENT by twilio API
    twilioMessage = []

    # To see if program was run for first time or if user wants to change log file by checking if Log File Exists (courselog.xls)
    # If it exists, This program will check for the status of courses from Mosaic to status from courselog.xls
    if os.path.isfile("courselog.xls"):
        twilioMessage = courseChecker(mosaicCourseDetails)
        sendTwilio(twilioMessage)
    else:
        creatingCourseLog(mosaicCourseDetails)
        twilioMessage.append("Your Enrollment cart is now been logged.You will receive a text message if anything changes")
        sendTwilio(twilioMessage)
