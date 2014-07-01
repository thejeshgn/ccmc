#couldnt get this thing to work
#!/usr/bin/env python
import sys
import sqlite3 as lite
import requests
import time
from bs4 import BeautifulSoup
import dataset

zones = {"East":"01","West":"02","South":"03","North":"04","Central":"05"}
wards_east = {}
db = dataset.connect('sqlite:///./database/ccmc.sqlite')


for zone_name, zone_id in zones.iteritems():
    print "Now for zone="+str(zone_name)
    request_session = requests.Session()
    html_src = ""
    user_agent = {'User-agent': 'Mozilla/5.0'}
    html_get_src = request_session.get("https://payment.ccmc.gov.in/repAssesseeDet.asp?type=P",headers = user_agent)

    zone_page_url = "https://payment.ccmc.gov.in/repAssesseeDet.asp?type="
    payload = {'hdnCode':  str(zone_id)} 
    user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36','Referer':'https://www.ksndmc.org/Reservoir_Details.aspx','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.ksndmc.org','Host':'www.ksndmc.org','Accept-Encoding':'gzip,deflate,sdch','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}        
    html_post_src = request_session.get(zone_page_url,data=payload,cookies=html_get_src.cookies, headers = user_agent)
    soup = BeautifulSoup(html_post_src.content)
    #print html_post_src.content
    print "+++++++++++++++++++++++++++++++++++++++++++++="
    ward_cells = soup.select("body")
    print ward_cells
    wards = []
    for ward in ward_cells:
        print ward
    break

