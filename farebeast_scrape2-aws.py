#!/usr/bin/python

import MySQLdb as mdb
import string
import sys
import urllib, string, fileinput, sys
from time import strftime
import datetime
import os
import re
from subprocess import Popen, PIPE
import time
import socket
import urllib2





def count_flights():
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
       cur=con.cursor()
       cur.execute("SELECT COUNT(*) FROM flights")
       no_of_flights_tupple=cur.fetchone()
       no_of_flights=int(no_of_flights_tupple[0])
    return no_of_flights


def read_flights(fid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT portA, portB, dateA, dateB FROM flights where fid = (%s)" % fid)
        flightinfo=cur.fetchone()
    return flightinfo

def write_fares(fid,expediafare, kayakfare):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    
    # Create the insert strings
    column_str = "searchtime, fid, expediafare, kayakfare"
    insert_str = ("%s, " * 4)[:-2]
    final_str = "INSERT INTO fares (%s) VALUES (%s)" % (column_str, insert_str)
    
    data_to_insert=(datetime.datetime.utcnow(), fid, expediafare, kayakfare)
    #print final_str, len(userdata)
    
    # Insert each symbol
    with con: 
        cur = con.cursor()
        cur.execute(final_str,data_to_insert)

#### INSERT FLIGHTGROUP - FUNCTIONS

def count_flightgroups():
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
       cur=con.cursor()
       cur.execute("SELECT COUNT(*) FROM flightgroups")
       no_of_flightgroups_tuple=cur.fetchone()
       no_of_flightgroups=int(no_of_flightgroups_tuple[0])
    return no_of_flightgroups

def read_flightgroups(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT fgid, fgname, uid, fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20 FROM flightgroups where fgid = (%s)" % fgid)
        flightgroupinfo=cur.fetchone()
    return flightgroupinfo

def latest_departure(fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        insert_str = ("%s, " * 20)[:-2]
        final_str = "SELECT max(dateA) from flights WHERE FID in (%s)" % insert_str
        
        cur.execute(final_str,(fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20))
        last_departure=cur.fetchone()
    return last_departure

def min_fare_flight_website(fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        insert_str = ("%s, " * 20)[:-2]
        # final_str = "SELECT max(fareid),searchtime,fid,expediafare,kayakfare from fares WHERE fid in (%s) AND searchtime > DATE_ADD(CURDATE(), INTERVAL -1 DAY) GROUP BY fid" % insert_str
        final_str= "SELECT maxfareid, fareid, fid2, searchtime, expediafare, kayakfare from fares join (SELECT max(fareid) as maxfareid, fid as fid2 from fares WHERE fid in (%s) AND searchtime > DATE_ADD(CURDATE(), INTERVAL -1 DAY) GROUP BY FID) as tabletemp on maxfareid=fareid"  % insert_str
        
        cur.execute(final_str,(fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20))
    
    min_stuff=[]
    for row in cur:
        min_stuff.append((int(row[2]),row[3],int(row[4]),int(row[5])))
    return min_stuff

def write_groupfare(currentdatetime,fgid,fid,fare,website,searchtime ,alert):
    con = mdb.connect(host='localhost', user='root', db='farebeast')

    # Create the insert strings
    column_str = "grouptime, fgid, fid, fare, website, searchtime, alert"
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO groupfares (%s) VALUES (%s)" % (column_str, insert_str)
    
    tuple_to_insert=(currentdatetime,fgid,fid,fare,website,searchtime,alert)
    with con: 
        cur = con.cursor()
        cur.execute(final_str, tuple_to_insert)


#### END INSERT GROUPFARES-FUNCTIONS

home='/home/ubuntu/farebeast8-aws/'
    
for k in xrange(count_flights()):
    flight_to_check=read_flights(k+1)
    fid=k+1

    if(datetime.date.today() < flight_to_check[2]):
    
        #time.sleep(5)
    
        portA=flight_to_check[0]
        portB=flight_to_check[1]
        dayA=("%02d" %flight_to_check[2].day)
        monthA=("%02d" %flight_to_check[2].month)
        yearA=("%02d" %(flight_to_check[2].year-2000))
        dayB=("%02d" %flight_to_check[3].day)
        monthB=("%02d" %flight_to_check[3].month)
        yearB=("%02d" %(flight_to_check[3].year-2000))

        expedia_url="http://www.expedia.com/pub/agent.dll?qscr=fexp&flag=q&city1="+portA+"&citd1="+portB+"&date1="+monthA+"/"+dayA+"/20"+yearA+"&time1=362&date2="+monthB+"/"+dayB+"/20"+yearB+"&time2=362&cAdu=1&cSen=&cChi=&cInf=&infs=2&tktt=&trpt=2&ecrc=&eccn=&qryt=8&load=1&airp1=&dair1=&rdct=1&rfrr=-429"
        kayak_url="http://www.kayak.com/flights/"+portA+"-"+portB+"/20"+yearA+"-"+monthA+"-"+dayA+"/20"+yearB+"-"+monthB+"-"+dayB
        bing_url="http://www.bing.com/travel/flights/search?q=&vo1=%28"+portA+"%29&o="+portA+"&ve1=%28"+portB+"%29&e="+portB+"&d1="+monthA+"%2F"+dayA+"%2F20"+yearA+"&r1="+monthB+"%2F"+dayB+"%2F20"+yearB+"&p=1&b=COACH"
        #BEGIN EXPEDIA SEARCH

        process = Popen(["python", home+"get_expedia.py", expedia_url], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
        try:
            minfare_expedia=int(output)
        except ValueError: 
            minfare_expedia=0


        # END EXPEDIA PRICE SEARCH
        # BEGIN KAYAK PRICE SEARCH
        #minfare_kayak=0
        #process = Popen(["python", "jw_kayak.py", kayak_url, "40"], stdout=PIPE)
        #(output, err) = process.communicate()
        #exit_code = process.wait()
        #try:
        #    minfare_kayak=int(output)
        #except ValueError: 
        #    minfare_kayak=0


        # END KAYAK PRICE SEARCH

        #BEGIN BING SEARCH
        process = Popen(["xvfb-run" ,"--auto-servernum" , "--server-num=1","python", home+"jw_bing.py", bing_url, "30"], stdout=PIPE)
        #process = Popen(["xvfb-run" ,"--auto-servernum" , "--server-num=1","python", "jw_bing.py"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        deal_with_AWS=re.findall(r'\n(\d+)',output)
        
        if(deal_with_AWS != []):
            minfare_kayak=int(deal_with_AWS[0])
        else:
            minfare_kayak=0
        #END BING SEARCH
    
        print ("%02d"% datetime.datetime.utcnow().hour)+":"+("%02d"% datetime.datetime.utcnow().minute)+":"+("%02d"% datetime.datetime.utcnow().second)+"  Flight ID: "+str(fid)+" Expedia: $"+str(minfare_expedia)+" Bing: $"+str(minfare_kayak)
    
        write_fares(fid,minfare_expedia, minfare_kayak)
    
#### INSERT GROUPFARES

for k in xrange(count_flightgroups()):
    fgid=k+1
    flightgroup_to_check=read_flightgroups(k+1)
    lastflight=latest_departure(int(flightgroup_to_check[3]), int(flightgroup_to_check[4]), int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]))

    if(datetime.date.today() < lastflight[0]):
        min_stuff=min_fare_flight_website(int(flightgroup_to_check[3]), int(flightgroup_to_check[4]), int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]))
        searchdates=[]
        fids=[]
        expedia_prices=[]
        kayak_prices=[]
        min_price=0
    
        for i in xrange(len(min_stuff)):
            searchdates.append(min_stuff[i][1])
            fids.append(min_stuff[i][0])
            if (min_stuff[i][2] !=0):
                expedia_prices.append(min_stuff[i][2])
            else:
                expedia_prices.append(100000)
            if (min_stuff[i][3] !=0):
                kayak_prices.append(min_stuff[i][3])
            else:
                kayak_prices.append(100000)
    
        if (expedia_prices != []):
    
            if min(expedia_prices) < min(kayak_prices):
                best_website="expedia"
                min_price=min(expedia_prices)
                golden_index=expedia_prices.index(min_price)
                best_flight=fids[golden_index]
                best_time=searchdates[golden_index]
                alert=0
        
            elif (min(kayak_prices) != 1000000):
                best_website="kayak"
                min_price=min(kayak_prices)
                golden_index=kayak_prices.index(min_price)
                best_flight=fids[golden_index]
                best_time=searchdates[golden_index]
                alert=0
    
    
        if (min_price != 0):
            write_groupfare(datetime.datetime.utcnow(),fgid,best_flight,min_price,best_website,best_time,alert)