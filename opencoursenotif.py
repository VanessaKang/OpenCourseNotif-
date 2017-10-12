#############################
#Name: Vanessa Kang
#Date started: September 30, 2017
#Purpose: Determine when closed course is open so that notified students can enroll
#Version: 1
#############################

import requests
from bs4 import BeautifulSoup

##my_list_of_links = ["https://www.google.com/"]
##
##for index, link in enumerate(my_list_of_links):
##    #payload = {'q' : 'test'}
##    test = requests.get(link + "#q=test")
##    test.encoding = "ISO 8859-1"
##    print(test.text)

login_url = "https://epprd.mcmaster.ca/psp/prepprd/?cmd=login&languageCd=ENG"
request_url = "Where I want to go "

payload = { 'userid': 'x',
            'pwd': 'xx'}


with requests.Session() as s:
    p = s.post(login_url, data = payload)
    soup = BeautifulSoup(p.content, 'html.parser')
    print soup.prettify()

#Requesting to get a webpage (type anything in searchbar)
#r = requests.get(url)

###beautiful soup takes website content which we got from request r.content
##soup = BeautifulSoup(r.content, 'html.parser')
##
###Parse through all links in a HTML document and title beside it 
##for link in soup.find_all("a"):
##    print "Link: '%s' //// %s" %(link.get("href"), link.text)





