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
    
r = requests.get("https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Los+Angeles%2C+CA")

soup = BeautifulSoup(r.content, 'html.parser')
for link in soup.find_all("a"):
    print link.get("href")




