import string
import sys
#from matplotlib.pylab import *   # For plotting graphs.
#from matplotlib.pyplot import *
import urllib, string, fileinput, sys
from time import strftime
import datetime
#from matplotlib.dates import date2num
import os
import re
import MySQLdb as mdb
import webfunctions as wf



    
def get_flight_queue():
    allflightdata = open ("flight_queue.txt","r" )
    flightlines = allflightdata.readlines()
    allflightdata.close()

    flightgroupdata=[]
    for i in xrange(len(flightlines)):
        line=flightlines[i]
        split=[x.strip() for x in line.split(',')]
        flightgroupdata.append((split[0],split[1],split[2],split[3],split[4],split[5],split[6],split[7],split[8],split[9],split[10],split[11]))
    return flightgroupdata

def deleteContent(fName):
    with open(fName, "w"):
        pass

if __name__ == "__main__":
    
    flightgroupdata=get_flight_queue()
     
    for flightgroup in flightgroupdata:
        
        #DATA IN FILE: Lauren, Switzerland, SFO, ZRH, 06/04/2014, 06/13/2014, 18, 18, 7, 9, 0, 0
        username=flightgroup[0]
        nickname=flightgroup[1]
        portA=flightgroup[2]
        portB=flightgroup[3]
        dateA=flightgroup[4]
        dateB=flightgroup[5]
        extraA=flightgroup[6]
        extraB=flightgroup[7]
        min_d=flightgroup[8]
        max_d=flightgroup[9]
        pref=flightgroup[10]
        alarm=flightgroup[11]
        
        uid=wf.get_uid_from_name(username)
        (monthA,dayA,yearA)=dateA.split('/')
        (monthB,dayB,yearB)=dateB.split('/')
        
        formated_flightgroup=(int(uid),nickname,portA,portB,datetime.date(int(yearA),int(monthA),int(dayA)),datetime.date(int(yearB),int(monthB),int(dayB)),int(extraA),int(extraB),int(min_d),int(max_d),int(pref),int(alarm))
        #EXPECTED: flightgroup = (10, "Switzerland", "SFO", "ZRH", datetime.date(2014,6,4), datetime.date(2014,6,13), 18,18, 7,9,0,0)
        
        ValidFlights=wf.GenerateFlights(formated_flightgroup)
            
        maxflights=20
        currflight=0
            
        fids=[]
        for flight in ValidFlights:
            currflight=currflight+1
            if (currflight < maxflights+1):
                if wf.flight_doesnt_exist(flight):
                    wf.insert_flight(flight)
                    fid=wf.get_flight_id(flight)
                    print "flight did not exist, added", flight, fid
                    fids.append(fid)
                else:
                    fid=wf.get_flight_id(flight)
                    print "flight existed, did not add", flight, fid
                    fids.append(fid)
            else:
                print "exceeded more than 20 flights, not adding more"
        #insert_flight_group((uid,fgname,pref,alarm,fids))        
        wf.insert_flight_group((formated_flightgroup[0],formated_flightgroup[1],formated_flightgroup[10],formated_flightgroup[11],fids))
    
    deleteContent("flight_queue.txt")
