#############################
#Name: Vanessa Kang
#Date started: September 30, 2017
#Purpose: Determine when closed course is open so that notified students can enroll
#Version: 1
#############################

import requests
from bs4 import BeautifulSoup


#---Enter your credentials here-----------------------
macid = 'XXX'
password = 'XXX'
studentnumber = 'XXX' #exclude the leading zeros
#-----------------------------------------------------

#This is the login url needed to get onto Mosaic 
login_url = "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG"

#This is the url of the enrollment shopping cart
request_url = "https://csprd.mcmaster.ca/psc/prcsprd/EMPLOYEE/HRMS_LS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UGRD&EMPLID="+str(studentnumber)+"&INSTITUTION=MCMST&STRM=2181&TargetFrameName=None"

#This includes the name and password to get onto the site 
payload = { 'userid': macid,'pwd': password }


with requests.Session() as session:
    #creates a session and logs your credentials in
    post = session.post(login_url, data = payload)

    #Navigate to the intended enrollment cart page
    enroll_page = session.get(request_url)

    #Getting Beautiful Soup to parse through the document
    soup = BeautifulSoup(enroll_page.text, 'html.parser')

    #I know how to iterate through the rows, lets test parsing from one row first 
    row1 =  soup.find(id = "trSSR_REGFORM_VW$0_row1")

    coursedetails = row1.get_text("|", strip = True)


    #Find all rows of classes that are in the enrollement cart
##    for ss in soup.find_all(id=lambda value: value and value.startswith("trSSR_REGFORM_VW$0_row")):
##        coursedetails = ss.get_text("|", strip = True)
##        print " %s ---------------------------------------------------" %(ss)

#------------------------- Currently testing 
##    for status in soup.find_all(id = 'win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1'):
##        print status.img.get('alt')

#Parse through all links in a HTML document and title beside it 
##    for link in soup.find_all("a"):
##        print "Link: '%s' //// %s" %(link.get("href"), link.text)
#-------------------------




