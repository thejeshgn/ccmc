#couldnt get this thing to work
#!/usr/bin/env python
import sys
import sqlite3 as lite
import requests
import time
from BeautifulSoup import BeautifulSoup
import dataset

zones = {"East":"01","West":"02","South":"03","North":"04","Central":"05"}
wards_east = {}
db = dataset.connect('sqlite:///./database/ccmc.sqlite')
db_ward_table = db['wards']
db_ward_table_len = len(db_ward_table)
if db_ward_table_len > 1:
    print "1. Ward info exists. Not getting."
else:
    print "2. Getting the ward info for Zones"
    for zone_name, zone_id in zones.iteritems():
        print "Now for zone="+str(zone_name)
        request_session = requests.Session()
        html_src = ""
        user_agent = {'User-agent': 'Mozilla/5.0'}
        html_get_src = request_session.get("https://payment.ccmc.gov.in/repAssesseeDet.asp?type=P",headers = user_agent)
        #print html_get_src.content
        zone_page_url = "https://payment.ccmc.gov.in/repAssesseeDet.asp?type=P"
        payload = {'hdnCode':  str(zone_id)} 
        user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36','Referer':'https://www.ksndmc.org/Reservoir_Details.aspx','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.ksndmc.org','Host':'www.ksndmc.org','Accept-Encoding':'gzip,deflate,sdch','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}        
        html_post_src = request_session.get(zone_page_url,data=payload,cookies=html_get_src.cookies, headers = user_agent)
        soup = BeautifulSoup(html_post_src.content)
        main_div = soup.findAll(id="d1")
        main_table = ((main_div[0].contents)[2]).contents
        for rows in main_table:
            break_row = False
            column_values = []
            if rows != None:
                if str(rows).strip() != "":
                    #print rows.contents
                    for columns in rows.contents:
                        if str(columns) == '<td rowspan="1" class="title">S.No</td>':
                            break_row = True
                            continue
                        if str(columns).strip() == "" or str(columns) == "\n" :
                            continue
                        else:
                            column_values.append(columns.contents[0])
                    if break_row:
                        continue
            #print column_values
            if len(column_values) > 2:
                ward_no = str(column_values[1]).split("-")[1]
                no_of_assessees =  (column_values[2]).contents[0]
                insert_data = dict({"zone":zone_name , "zone_id":str(zone_id) , "ward":""  , "ward_no":str(ward_no), "no_of_assessees":no_of_assessees})
                print insert_data
                db_ward_table.insert(insert_data)

print "Get Street info for each ward"
all_wards = db_ward_table.all()
for ward in all_wards:
    zone_id = ward['zone_id']
    ward_no = str("WD-"+ward['ward_no'])
    hdnCode = zone_id + "'^" + ward_no
    street_page_url = "https://payment.ccmc.gov.in/repAssesseeDet.asp?type=P"
    payload = {'hdnCode':  str(hdnCode)} 
    user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36','Referer':'https://www.ksndmc.org/Reservoir_Details.aspx','Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.ksndmc.org','Host':'www.ksndmc.org','Accept-Encoding':'gzip,deflate,sdch','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}        
    html_post_src = requests.get(street_page_url,data=payload, headers = user_agent)
    print html_post_src.content
    soup = BeautifulSoup(html_post_src.content)
    main_div = soup.findAll(id="d1")
    main_table = ((main_div[0].contents)[2]).contents
    for rows in main_table:
        break_row = False
        column_values = []
        if rows != None:
            if str(rows).strip() != "":
                #print rows.contents
                for columns in rows.contents:
                    if str(columns) == '<td rowspan="1" class="title">S.No</td>':
                        break_row = True
                        continue
                    if str(columns).strip() == "" or str(columns) == "\n" :
                        continue
                    else:
                        column_values.append(columns.contents[0])
                if break_row:
                    continue
        print column_values
        if len(column_values) > 2:
            street      = str(column_values[1])
            street_id   = str(column_values[2])
            no_of_assessees =  (column_values[2]).contents[0]

            #insert_data = dict({"zone":zone_name , "zone_id":str(zone_id) , "ward":""  , "ward_no":str(ward_no), "no_of_assessees":no_of_assessees})
            #print insert_data
            

    break

