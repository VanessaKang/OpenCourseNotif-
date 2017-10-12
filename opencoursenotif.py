#############################
#Name: Vanessa Kang
#Date started: September 30, 2017
#Purpose: Determine when closed course is open so that notified students can enroll
#Version: 1
#############################

import requests

my_list_of_links = ["http://www.hipstercode.com",
                    "http://www.hipstercode.com/about"]

for index, link in enumerate(my_list_of_links):
    test = requests.get(link)
    test.encoding = "ISO 8859-1"
    print(test.headers)
    

