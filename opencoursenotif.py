#############################
# Name: Vanessa Kang
# Date started: September 30, 2017
# Purpose: Determine when a course is open or closed for enrollment and notify user when the course is availiable for Enrollment
# Version: 4
#############################

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

# Credentials here
# macid = input("What is your MacID?: ")
# password = input("What is your password?: ")
# studentnumber = input("Student Number (exclude leading zeros): ")


# This is the login url needed to get onto Mosaic
login_url = "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG"

# This is the url of the enrollment shopping cart Winter 2018 (Frame Source)
request_url = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UGRD&EMPLID=" + str(studentnumber) + "&INSTITUTION=MCMST&STRM=2181&TargetFrameName=None"

# This includes the name and password to get onto the site
payload = {'userid': macid, 'pwd': password}

# Excel Initialization
wb = Workbook()
sheet1 = wb.add_sheet("Courses")
attribute = ["Course", "Time", "Room Number", "Teacher", "Units", "Status"]
for i in range(0, 6):
    sheet1.col(i).width = 7000
    sheet1.write(1, i, attribute[i])


with requests.Session() as session:
    # Logs in using your credentials and creates a session where you stay logged in
    post = session.post(login_url, data=payload)

    # Navigate to McMaster Enrollment Cart Page
    enroll_page = session.get(request_url)

    # Getting Beautiful Soup to parse through the HTML content
    soup = BeautifulSoup(enroll_page.text, 'html.parser')

    # Initialize first row as 2 since the first row is taken up by Headers in the CourseTracker.xls
    eachrow = 2
    eachcol = 0

    # This looks for the Enrollment Table and parse values from there

    courseDetails = []
    for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):

        # Parsing HTML to get course details
        courseName = ss.find(id=lambda value: value and value.startswith("P_CLASS_NAME$")).get_text(" ", strip=True)
        courseTime = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_SCHED_LONG$")).get_text("", strip=True)
        courseLocation = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_MTG_LOC_LONG$")).get_text("", strip=True)
        courseTeacher = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_INSTR_LONG$")).get_text("", strip=True)
        courseUnits = ss.find(id=lambda value: value and value.startswith("win0divSSR_REGFORM_VW_UNT_TAKEN$")).get_text("", strip=True)
        courseStatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')

        oneCourse = [courseName, courseTime, courseLocation, courseTeacher, courseUnits, courseStatus]
        courseDetails.append(oneCourse)

        # This is a way to get all course details for each class in one line but poses some errors if McMaster has incomplete data
        # coursedetails = ss.get_text("|", strip=True)

        # add all variables to a array
        # each time it iterates, I will create a tuple of stuff

        # Checks if cousetracker is in directory
        # if in directory, go to course checker
        # Take course name and run its status
        # double check if status in file == status in array
        # if not, send text message
        # check if there are new courses, (count rows and count array)
        # ask User if they want to add
        # if not in directory (running this first time), create course checker file
        # Closed Courses Noted - Output a message saying file created, its will check ___ am

        # eachcol = 0
        # if (courseStatus == "Closed") | (courseStatus == "Open"):
        #     # Print Course Details (Title, Code, Time, Room, Teacher, Units) to a row divided by columns
        #     for string in ss.stripped_strings:
        #         sheet1.write(eachrow, eachcol, string)
        #         eachcol += 1
        #     sheet1.write(eachrow, 5, courseStatus)
        #     eachcol += 1
        #     eachrow = eachrow + 1

    print(courseDetails)


wb.save("coursetracker.xls")


#------------Version 2-----------------------------------------------------------------------------

# I know how to iterate through the rows, lets test parsing from one row first
# row1 =  soup.find(id = "trSSR_REGFORM_VW$0_row1")
# print " %s ---------------------------------------------------" %(ss)

# for status in soup.find_all(id = 'win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1'):
# print status.img.get('alt')

# Parse through all links in a HTML document and title beside it
# for link in soup.find_all("a"):
# print "Link: '%s' //// %s" %(link.get("href"), link.text)

#-----------Version 3- Just getting it to print out courses--------------------------------------------

# Find all rows of classes that are in the enrollement cart
# for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):
##
# Obtain all the course details including Course Code,Course Number, Schedule (Date and Time), Room Number, Teacher, Units
# coursedetails = ss.get_text("|", strip = True)
##
# Obtain the enrollment status of the course (Closed or Open)
# coursestatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')
##
# Print back course details into a nice printed statement
# print coursedetails + "|||" + coursestatus
