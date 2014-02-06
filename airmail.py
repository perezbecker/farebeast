#!/usr/bin/python

import string
import sys

import urllib, string, fileinput, sys
from time import strftime
import datetime
import re
import gmailbeast
import smsgmailbeast
import os
import farebeast_functions as fbf

home='/home/ubuntu/farebeast8-aws'
#home='/Users/danok/airfare_monitor/farebeast8-aws'


for k in xrange(fbf.count_flightgroups()):
    fgid=k+1
    flightgroup_to_check=fbf.read_flightgroups(fgid)
    lastflight=fbf.latest_departure(int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]), int(flightgroup_to_check[23]), int(flightgroup_to_check[24]))
    
    if(datetime.date.today() < lastflight[0]):
        days_since_alert=fbf.days_since_last_alert(fgid)
        
        if (days_since_alert < 1./48.):
        
            (user,email,mobile,carrier,pref,alarm)=fbf.get_userinfo(fgid)
            FGname=fbf.get_flightgroup_name(fgid)
            # BEST CURVE
            (group_times,search_times,fares,website,alert,dateA,dateB,fid)=fbf.get_best_timeseries(fgid)
        
            (portA,portB)=fbf.get_flightgroup_ports(fgid)
        
            dayA=("%02d" %dateA[-1].day)
            monthA=("%02d" %dateA[-1].month)
            yearA=("%02d" %(dateA[-1].year-2000))
            dayB=("%02d" %dateB[-1].day)
            monthB=("%02d" %dateB[-1].month)
            yearB=("%02d" %(dateB[-1].year-2000))
        
        
        
            expedia_url="http://www.expedia.com/pub/agent.dll?qscr=fexp&flag=q&city1="+portA+"&citd1="+portB+"&date1="+monthA+"/"+dayA+"/20"+yearA+"&time1=362&date2="+monthB+"/"+dayB+"/20"+yearB+"&time2=362&cAdu=1&cSen=&cChi=&cInf=&infs=2&tktt=&trpt=2&ecrc=&eccn=&qryt=8&load=1&airp1=&dair1=&rdct=1&rfrr=-429"
            bing_url="http://www.bing.com/travel/flights/search?q=&vo1=%28"+portA+"%29&o="+portA+"&ve1=%28"+portB+"%29&e="+portB+"&d1="+monthA+"%2F"+dayA+"%2F20"+yearA+"&r1="+monthB+"%2F"+dayB+"%2F20"+yearB+"&p=1&b=COACH"
        
        
            if(website[-1] == 'expedia'):
                gourl=expedia_url
        
            else:
                gourl=bing_url
        
        
            message='Hello '+user+',\n \n The current fare for '+FGname+' on '+website[-1]+' between '+str(dateA[-1].month)+'/'+str(dateA[-1].day)+' and '+str(dateB[-1].month)+'/'+str(dateB[-1].day)+' is $'+str(fares[-1])+'. \n The average fare over the last week for the optimal flight dates was $'+str(int(fbf.avg_fare_within_last_week(fgid)))+'. \n \n To book this flight go to: '+gourl+' \n \n  --- FareBeast ---' 

            subject="$"+str(fares[-1])+" - FareBeast Alert for "+FGname+" trip"
            attachment=home+"/static/plots/"+str(fgid)+'a.png'

            gmailbeast.sendMail(email, subject, message, attachment)

        
        
            if(carrier=='att'):
                smsrecipient=str(mobile)+'@txt.att.net'
            elif(carrier=='verizon'):
                smsrecipient=str(mobile)+'@vtext.com'
            elif(carrier=='sprint'):
                smsrecipient=str(mobile)+'@messaging.sprintpcs.com'                  
            elif(carrier=='tmobile'):
                smsrecipient=str(mobile)+'@tmomail.net'           
            elif(carrier=='virgin'):
                smsrecipient=str(mobile)+'@vmobl.com'            
            elif(carrier=='cricket'):
                smsrecipient=str(mobile)+'@sms.mycricket.com'            
            elif(carrier=='boost'):
                smsrecipient=str(mobile)+'@myboostmobile.com'            
            else:
                smsrecipient = "none"

            smsmessage="$"+str(fares[-1])+" for "+FGname+"\n --- FareBeast ---"
            smssubject="FareBeast Alert!"
            if (smsrecipient != 9999999999):
                smsgmailbeast.sendMail(smsrecipient,smssubject,smsmessage)


