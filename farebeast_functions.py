
import string
import sys

from matplotlib.dates import date2num
import urllib, string, fileinput, sys
from time import strftime
import datetime
import os
import re
import MySQLdb as mdb
import numpy as np


def get_best_timeseries(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT groupfares.grouptime, groupfares.searchtime, groupfares.fare, groupfares.website, groupfares.alert, flights.dateA, flights.dateB, groupfares.fid  from groupfares join flights on groupfares.fid=flights.fid where fgid= (%s)" % fgid)
        timeseries_temp=cur.fetchall()
    group_times=[]
    search_times=[]
    fares=[]
    website=[]
    alert=[]
    dateA=[]
    dateB=[]
    fid=[]
    for i in xrange(len(timeseries_temp)):
        group_times.append(timeseries_temp[i][0])
        search_times.append(timeseries_temp[i][1])
        fares.append(int(timeseries_temp[i][2]))
        website.append(timeseries_temp[i][3])
        alert.append(int(timeseries_temp[i][4]))
        dateA.append(timeseries_temp[i][5])
        dateB.append(timeseries_temp[i][6])
        fid.append(int(timeseries_temp[i][7]))
    return (group_times,search_times,fares,website,alert,dateA,dateB,fid)
    

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
        cur.execute("SELECT fgid, fgname, uid, pref, alarm, fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20 FROM flightgroups where fgid = (%s)" % fgid)
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

        
def days_since_last_alert(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT grouptime from groupfares where alert=1 and fgid=(%s) order by groupfareid desc limit 1" % fgid)
        date_of_last_alert=cur.fetchone()
    
    if date_of_last_alert:
        DaysSinceLastAlert=float(date2num(datetime.datetime.utcnow()))-float(date2num(date_of_last_alert))
    else:
        DaysSinceLastAlert=1000.
    
    return DaysSinceLastAlert

def fare_of_last_alert(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT fare from groupfares where alert=1 and fgid=(%s) order by groupfareid desc limit 1" % fgid)
        fare_of_last_alert=cur.fetchone()
    
    if fare_of_last_alert:
        FareLastAlert=float(fare_of_last_alert[0])
    else:
         FareLastAlert=10000.
    
    return FareLastAlert

def alert_dates_and_fares(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT searchtime,fare from groupfares where alert=1 and fgid=(%s) order by groupfareid asc" % fgid)
        dates_fares=cur.fetchall()

    search_times=[]
    fares=[]
    for i in xrange(len(dates_fares)):
         
        search_times.append(dates_fares[i][0])
        fares.append(int(dates_fares[i][1]))
            
    return (search_times,fares)




def min_fare_within_last_week(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT min(fare) from groupfares where searchtime > DATE_ADD(CURDATE(), INTERVAL -7 DAY) and fgid=(%s)" % fgid)
        min_fare=cur.fetchone()
    
    return float(min_fare[0])
         
        
def avg_fare_within_last_week(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT fare from groupfares where searchtime > DATE_ADD(CURDATE(), INTERVAL -7 DAY) and fgid=(%s)" % fgid)
        avg_fare=cur.fetchall()
    
    filter_avg_fares=[]
    for i in xrange(len(avg_fare)):
        if (float(avg_fare[i][0]) > 10. and float(avg_fare[i][0]) < 10000.):
            filter_avg_fares.append(float(avg_fare[i][0]))
    
    filtered_average=int(round(sum(filter_avg_fares)/len(filter_avg_fares)))
    return filtered_average  
    
    
def get_userinfo(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT user, email, mobile, carrier, pref, alarm from users join flightgroups on users.uid=flightgroups.uid where fgid=(%s)" % fgid)
        userdetails=cur.fetchone()
    
    user=userdetails[0]
    email=userdetails[1]
    mobile=int(userdetails[2])
    carrier=userdetails[3]
    pref=int(userdetails[4])
    alarm=int(userdetails[5])
    
    return (user,email,mobile,carrier,pref,alarm)
    
def get_flightgroup_name(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT fgname from flightgroups where fgid= (%s)" % fgid)
        flightgroupname=cur.fetchone()
    return flightgroupname[0]
    
def get_flightgroup_ports(fgid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT portA, portB from flights join flightgroups on flights.fid=flightgroups.fid01 where flightgroups.fgid=(%s)" % fgid)
        flightports=cur.fetchone()
    portA=flightports[0]
    portB=flightports[1]
    return (portA,portB)
    

    