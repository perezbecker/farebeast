#!/usr/bin/python
""" Air Alert program idea:
(A)First Check if Alert data exists:
(A)NO:
   Compute: Days until flight
            Days monitoring
            Average Price
            Lowest Price
Alert: If days until flight > 100 and Days monitoring > 10, alert if price is lower or equal than lowest No->(or 30% less than average).
       If days until flight < 100 and Days monitoring > 3, alert if price is lower than lowest (or 30% less than average).
       Create Alert data file.

(A)YES:
      Read price and date of last buying suggestion. 
      If last suggestion was less than 5 days ago only suggest again if price is >5% lower than suggestion.
      If last suggestion was more than 5 days ago buy less 14 days ago suggest price suggest if price is lower or equal than last suggestion.
      If last suggestion was more than 14 days ago, suggest if price is lower than the lowest in the past 7 days. 
"""


import string
import sys

import urllib, string, fileinput, sys
from time import strftime
import datetime
import re
from matplotlib.dates import date2num
import os
import farebeast_functions as fbf


for k in xrange(fbf.count_flightgroups()):
    fgid=k+1
    flightgroup_to_check=fbf.read_flightgroups(fgid)
    lastflight=fbf.latest_departure(int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]), int(flightgroup_to_check[23]), int(flightgroup_to_check[24]))
    
    if(datetime.date.today() < lastflight[0]):
    
    
        (group_times,search_times,fares,website,alert,dateA,dateB,fids)=fbf.get_best_timeseries(fgid)
     
        totflags=sum(alert)
     
        if(totflags < 0.5):
            DaysMonitoring=float(date2num(datetime.datetime.utcnow()))-float(date2num(search_times[0]))
            DaysUntilFlight=float(date2num(lastflight[0]))-float(date2num(datetime.datetime.utcnow()))
            LowestPrice=min(fares) 
                       
            #If days until flight > 100 and Days monitoring > 10, alert if price is lower or equal than lowest No->(or 30% less than average).
            if ((DaysUntilFlight > 100.) and (DaysMonitoring > 10.) and (fares[-1] <= LowestPrice)):
                fbf.write_groupfare(datetime.datetime.utcnow(),fgid,fids[-1],fares[-1],website[-1],search_times[-1],1)


            #If days until flight < 100 and Days monitoring > 3, alert if price is lower than lowest (or 30% less than average).    
            if ((DaysUntilFlight < 100.) and (DaysMonitoring > 3.) and (fares[-1] <= LowestPrice)):
                fbf.write_groupfare(datetime.datetime.utcnow(),fgid,fids[-1],fares[-1],website[-1],search_times[-1],1)
               
        
        
        if(totflags > 0.5):
            DaysSinceAlert=fbf.days_since_last_alert(fgid)
            BestPriceOfLastWeek=fbf.min_fare_within_last_week(fgid)
            LastAlertPrice=fbf.fare_of_last_alert(fgid)
            
            #If last suggestion was less than 5 days ago only suggest again if price is >5% lower than suggestion.
            if ((DaysSinceAlert < 5.) and (fares[-1] <= (0.95*LastAlertPrice))):
                fbf.write_groupfare(datetime.datetime.utcnow(),fgid,fids[-1],fares[-1],website[-1],search_times[-1],1)

            #If last suggestion was more than 5 days ago buy less 14 days ago suggest price suggest if price is lower or equal than last suggestion.
            if ((DaysSinceAlert > 5.) and (DaysSinceAlert < 14.) and (fares[-1] <= LastAlertPrice)):
                fbf.write_groupfare(datetime.datetime.utcnow(),fgid,fids[-1],fares[-1],website[-1],search_times[-1],1)
   
                 
            #If last suggestion was more than 14 days ago, suggest if price is lower than the lowest in the past 7 days.
            if ((DaysSinceAlert > 14.) and (fares[-1] <= BestPriceOfLastWeek)):
                fbf.write_groupfare(datetime.datetime.utcnow(),fgid,fids[-1],fares[-1],website[-1],search_times[-1],1)
     
     
     
     
     
     
