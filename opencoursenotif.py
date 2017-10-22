#############################
#Name: Vanessa Kang
#Date started: September 30, 2017
#Purpose: Determine when a course is open or closed for enrollment and notify user when the course is availiable for Enrollment
#Version: 4
#############################

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

#Credentials here
macid = raw_input("What is your MacID?: ")
password = raw_input("What is your password?: ")
studentnumber = raw_input("Student Number (exclude leading zeros): ")

#This is the login url needed to get onto Mosaic 
login_url = "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG"

#This is the url of the enrollment shopping cart
request_url = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UGRD&EMPLID="+str(studentnumber)+"&INSTITUTION=MCMST&STRM=2181&TargetFrameName=None"

#This includes the name and password to get onto the site 
payload = { 'userid': macid,'pwd': password }

#Excel Initialization 
wb = Workbook()
sheet1 = wb.add_sheet("Courses")
attribute = ["Course","Course Number","Time","Room Number","Teacher","Units"]
for i in range(0,6):
    sheet1.col(i).width = 7000
    sheet1.write(1,i, attribute[i])


with requests.Session() as session:
    #Logs in using your credentials and creates a session where you stay logged in 
    post = session.post(login_url, data = payload)

    #Navigate to McMaster Enrollment Cart Page
    enroll_page = session.get(request_url)

    #Getting Beautiful Soup to parse through the HTML content
    soup = BeautifulSoup(enroll_page.text, 'html.parser')

    eachrow = 2
    for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):
        coursestatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')
        coursedetails = ss.get_text("|", strip = True)
        
        eachcol = 0 
        if coursestatus == "Closed":
            for string in ss.stripped_strings:
                sheet1.write(eachrow,eachcol,string)
                eachcol = eachcol + 1
            eachrow = eachrow + 1
            

wb.save("coursetracker.xls")
        


        


#------------Version 2-----------------------------------------------------------------------------

#I know how to iterate through the rows, lets test parsing from one row first 
#row1 =  soup.find(id = "trSSR_REGFORM_VW$0_row1")
#print " %s ---------------------------------------------------" %(ss)
        
##    for status in soup.find_all(id = 'win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1'):
##        print status.img.get('alt')

#Parse through all links in a HTML document and title beside it 
##    for link in soup.find_all("a"):
##        print "Link: '%s' //// %s" %(link.get("href"), link.text)

#-----------Version 3- Just getting it to print out courses--------------------------------------------
    
      #Find all rows of classes that are in the enrollement cart 
##    for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):
##        
##        #Obtain all the course details including Course Code,Course Number, Schedule (Date and Time), Room Number, Teacher, Units
##        coursedetails = ss.get_text("|", strip = True)
##
##        #Obtain the enrollment status of the course (Closed or Open) 
##        coursestatus = ss.find(id=lambda value: value and value.startswith("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$")).img.get('alt')
##
##        # Print back course details into a nice printed statement
##        print coursedetails + "|||" + coursestatus
