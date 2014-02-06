
import string
import sys
import urllib, string, fileinput, sys
from time import strftime
import datetime
import os
import re
import MySQLdb as mdb
import numpy as np



def get_user_table():
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT uid, user, password, email, mobile, carrier from users order by uid asc")
        user_data=cur.fetchall()
    
    uids=[]
    users=[]
    passwords=[]
    emails=[]
    mobiles=[]
    carriers=[]    
    for i in xrange(len(user_data)):
        uids.append(int(user_data[i][0]))
        users.append(user_data[i][1])
        passwords.append(user_data[i][2])
        emails.append(user_data[i][3])
        mobiles.append(user_data[i][4])
        carriers.append(user_data[i][5])    
            
    return (uids,users,passwords,emails,mobiles,carriers)

def get_gfids(uid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT fgid FROM flightgroups where uid=(%s)" % uid)
        user_fgids=cur.fetchall()
    
    fgids=[]
    for i in xrange(len(user_fgids)):
        fgids.append(int(user_fgids[i][0]))
    
    return fgids
    

###### FLIGHT DATE GENERATION ########

    
def DateUS2GER(datein):
    month,day,year = datein.split('/')
    year=year[-2:]
    gerdate=day+'.'+month+'.'+year
    return gerdate

def Traveldays(DateOut,DateIn):
    temp=datetime.datetime.strptime(DateIn,"%d.%m.%y") - datetime.datetime.strptime(DateOut,"%d.%m.%y")
    seconds=temp.total_seconds()
    return int(seconds/(60.*60.*24.))

def Triad2Date(day,month,year):
    return str(day)+'.'+str(month)+'.'+str(year)

def DatePlusN(day,month,year,N):
    Date=str(day)+'.'+str(month)+'.'+str(year)
    a=datetime.datetime.strptime(Date,"%d.%m.%y")+datetime.timedelta(days=N)
    return (a.day,a.month,a.year-2000)

def DatePlusN_datetime(day,month,year,N):
    Date=str(day)+'.'+str(month)+'.'+str(year)
    a=datetime.datetime.strptime(Date,"%d.%m.%y")+datetime.timedelta(days=N)
    return datetime.date(a.year,a.month,a.day)




def GenerateDatesWeb(DateOut,DateIn,ExtraOut,ExtraIn,min_d,max_d):
    
    weekdaylist=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    
    day2,month2,year2 = DateIn.split('.')
    day1,month1,year1 = DateOut.split('.')

    #print ExtraOut, ExtraIn

    dday1=int(day1)
    dday2=int(day2)
    dmonth1=int(month1)
    dmonth2=int(month2)
    dyear1=int(year1)
    dyear2=int(year2)

    #print dday1

    ValidFlights=[]

    for i in range(ExtraOut+1):
        for j in range(ExtraIn+1):
            #print i,j
            Date1=Triad2Date(DatePlusN(dday1,dmonth1,dyear1,i)[0],DatePlusN(dday1,dmonth1,dyear1,i)[1],DatePlusN(dday1,dmonth1,dyear1,i)[2])
            Date2=Triad2Date(DatePlusN(dday2,dmonth2,dyear2,j)[0],DatePlusN(dday2,dmonth2,dyear2,j)[1],DatePlusN(dday2,dmonth2,dyear2,j)[2])
            #print Date1,Date2
            TryDates=Traveldays(Date1,Date2)
            #print TryDates
            (dayA,monthA,yearA)=DatePlusN(day1,month1,year1,i)
            (dayB,monthB,yearB)=DatePlusN(day2,month2,year2,j)
            NoOfDays=TryDates
            DayOfWeekA=datetime.date(yearA,monthA,dayA).weekday()
            DayOfWeekB=datetime.date(yearB,monthB,dayB).weekday()
            FlightList=[str(dayA),str(monthA),str(yearA),str(dayB),str(monthB),str(yearB),str(NoOfDays),weekdaylist[DayOfWeekA],weekdaylist[DayOfWeekB]]
            
            if TryDates >= min_d and TryDates <= max_d:
                ValidFlights.append(FlightList)
            elif min_d == 0 and max_d == 0:
                ValidFlights.append(FlightList)
            elif TryDates >= min_d and max_d == 0:
                ValidFlights.append(FlightList)
            elif min_d == 0 and TryDates <= max_d:
                ValidFlights.append(FlightList)
    
    return ValidFlights
    
def insert_users(userdata):
    con = mdb.connect(host='localhost', user='root', db='farebeast')

    # Create the insert strings
    column_str = "user, password, email, mobile, carrier, datejoined"
    insert_str = ("%s, " * 6)[:-2]
    final_str = "INSERT INTO users (%s) VALUES (%s)" % (column_str, insert_str)


    # Insert each symbol
    with con: 
        cur = con.cursor()
        cur.execute(final_str, userdata)


def add_user_to_file(userdata):
    g = open('users.txt', 'r')
    flines=g.readlines()
    no_of_users=len(flines)
    g.close()
    f = open('users.txt', 'a')
    #userdata consists of [username,password,email,mobile,carrier,date_joined]
    print >> f, str(no_of_users+1), str(userdata[0]), str(userdata[1]), str(userdata[2]), str(userdata[3]), str(userdata[4]) 
    f.close()


def add_flightgroup_to_file(active_user,nickname,portA,portB,dateA,dateB,extraA,extraB,min_d,max_d):
    string_to_add=active_user+', '+nickname+', '+portA+', '+portB+', '+dateA+', '+dateB+', '+extraA+', '+extraB+', '+min_d+', '+max_d+', 0, 0'
    f = open('flight_queue.txt', 'a')
    print >> f, string_to_add
    f.close()


def user_doesnt_exist(username):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    user_does_not_exist=True
    with con:
        cur=con.cursor()
        cur.execute("SELECT user FROM users")
        for row in cur:
            if (row[0] == username):
                user_does_not_exist=False

    return user_does_not_exist
    
    
def GenerateFlights((UserID,FGname,portA,portB,dateA,dateB,extraA,extraB,min_d,max_d,pref,alarm)):
    dayA=dateA.day
    monthA=dateA.month
    yearA=dateA.year-2000

    dayB=dateB.day
    monthB=dateB.month
    yearB=dateB.year-2000

    #print ExtraOut, ExtraIn

    dday1=int(dayA)
    dday2=int(dayB)
    dmonth1=int(monthA)
    dmonth2=int(monthB)
    dyear1=int(yearA)
    dyear2=int(yearB)

    #print dday1

    ValidFlights=[]

    for i in range(extraA+1):
        for j in range(extraB+1):
            #print i,j
            Date1=Triad2Date(DatePlusN(dday1,dmonth1,dyear1,i)[0],DatePlusN(dday1,dmonth1,dyear1,i)[1],DatePlusN(dday1,dmonth1,dyear1,i)[2])
            Date2=Triad2Date(DatePlusN(dday2,dmonth2,dyear2,j)[0],DatePlusN(dday2,dmonth2,dyear2,j)[1],DatePlusN(dday2,dmonth2,dyear2,j)[2])
            #print Date1,Date2
            TryDates=Traveldays(Date1,Date2)
            #print TryDates
            if TryDates >= min_d and TryDates <= max_d:
                FlightTuple=(portA,portB,DatePlusN_datetime(dday1,dmonth1,dyear1,i),DatePlusN_datetime(dday2,dmonth2,dyear2,j))
                ValidFlights.append(FlightTuple)
            elif min_d == 0 and max_d == 0:
                FlightTuple=(portA,portB,DatePlusN_datetime(dday1,dmonth1,dyear1,i),DatePlusN_datetime(dday2,dmonth2,dyear2,j))
                ValidFlights.append(FlightTuple)  
            elif TryDates >= min_d and max_d == 0:
                FlightTuple=(portA,portB,DatePlusN_datetime(dday1,dmonth1,dyear1,i),DatePlusN_datetime(dday2,dmonth2,dyear2,j))
                ValidFlights.append(FlightTuple)
            elif min_d == 0 and TryDates <= max_d:
                FlightTuple=(portA,portB,DatePlusN_datetime(dday1,dmonth1,dyear1,i),DatePlusN_datetime(dday2,dmonth2,dyear2,j))
                ValidFlights.append(FlightTuple)


    return ValidFlights
    



#### INSERT FLIGHTGROUP FUNCTIONS

def insert_flight(flight):

    con = mdb.connect(host='localhost', user='root', db='farebeast')

    # Create the insert strings
    column_str = "portA, portB, dateA, dateB"
    insert_str = ("%s, " * 4)[:-2]
    final_str = "INSERT INTO flights (%s) VALUES (%s)" % (column_str, insert_str)
    #print final_str, len(flights)

    # Insert each symbol
    with con: 
        cur = con.cursor()
        cur.execute(final_str, flight)

def flight_doesnt_exist(flight):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    flight_does_not_exist=True
    with con:
        cur=con.cursor()
        cur.execute("SELECT portA, portB, dateA, dateB FROM flights")
        for row in cur:
            if (row == flight):
                flight_does_not_exist=False

    return flight_does_not_exist

def get_flight_id(flight):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    final_str = "SELECT fid FROM flights WHERE portA = (%s) AND portB=(%s) AND dateA=(%s) AND dateB=(%s)" % ("%s","%s","%s","%s")
    with con:
        cur=con.cursor()
        cur.execute(final_str, flight)
        a=cur.fetchone()
    return int(a[0])


def insert_flight_group((uid,fgname,pref,alarm,fids)):

    con = mdb.connect(host='localhost', user='root', db='farebeast')

    # Create the insert strings
    column_str = "fgname, uid, pref, alarm, fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20"
    insert_str = ("%s, " * 24)[:-2]
    final_str = "INSERT INTO flightgroups (%s) VALUES (%s)" % (column_str, insert_str)
    #print final_str, len(flights)

    if len(fids)==1:
        fid01=fids[0]; fid02=0; fid03=0; fid04=0; fid05=0; fid06=0; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==2:
        fid01=fids[0]; fid02=fids[1]; fid03=0; fid04=0; fid05=0; fid06=0; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==3:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=0; fid05=0; fid06=0; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==4:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=0; fid06=0; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==5:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=0; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==6:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=0; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==7:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=0; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==8:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=0; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==9:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=0; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==10:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=0; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==11:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=0; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==12:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=0; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==13:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=0; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==14:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=0; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==15:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=0; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==16:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=fids[15]; fid17=0; fid18=0; fid19=0; fid20=0
    elif len(fids)==17:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=fids[15]; fid17=fids[16]; fid18=0; fid19=0; fid20=0
    elif len(fids)==18:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=fids[15]; fid17=fids[16]; fid18=fids[17]; fid19=0; fid20=0
    elif len(fids)==19:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=fids[15]; fid17=fids[16]; fid18=fids[17]; fid19=fids[18]; fid20=0
    else:
        fid01=fids[0]; fid02=fids[1]; fid03=fids[2]; fid04=fids[3]; fid05=fids[4]; fid06=fids[5]; fid07=fids[6]; fid08=fids[7]; fid09=fids[8]; fid10=fids[9]; fid11=fids[10]; fid12=fids[11]; fid13=fids[12]; fid14=fids[13]; fid15=fids[14]; fid16=fids[15]; fid17=fids[16]; fid18=fids[17]; fid19=fids[18]; fid20=fids[19]
        
    tuple_to_insert=(fgname,uid,pref, alarm, fid01, fid02, fid03, fid04, fid05, fid06, fid07, fid08, fid09, fid10, fid11, fid12, fid13, fid14, fid15, fid16, fid17, fid18, fid19, fid20)
    
    with con: 
        cur = con.cursor()
        cur.execute(final_str, tuple_to_insert) 
    
 
 
def get_uid_from_name(name):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con: 
        cur = con.cursor()
        cur.execute("SELECT uid FROM users where user=\'%s\'" % name)
        userdetails=cur.fetchone()
    
    uid=int(userdetails[0])
    return uid


    
    
