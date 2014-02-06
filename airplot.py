#!/usr/bin/python

import matplotlib
matplotlib.use('agg')


import string
import sys
from matplotlib.pylab import *   # For plotting graphs.
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import urllib, string, fileinput, sys
from time import strftime
import datetime
import os
import re
import farebeast_functions as fbf
import MySQLdb as mdb
import numpy as np
import time


def get_timeseries(fid):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    with con:
        cur=con.cursor()
        cur.execute("SELECT searchtime, expediafare, kayakfare from fares where fid= (%s)" % fid)
        timeseries_temp=cur.fetchall()
    times=[]
    expedia_prices=[]
    kayak_prices=[]
    for i in xrange(len(timeseries_temp)):
        times.append(timeseries_temp[i][0])
        expedia_prices.append(int(timeseries_temp[i][1]))
        kayak_prices.append(int(timeseries_temp[i][2]))
        
    return (times,expedia_prices,kayak_prices)



home='/home/ubuntu/farebeast8-aws'
#home='/Users/danok/airfare_monitor/farebeast8-aws'

wait_time=0.1 #in seconds
mydpi=120

for k in xrange(fbf.count_flightgroups()):
    #for k in xrange(2):
    fgid=k+1
    flightgroup_to_check=fbf.read_flightgroups(k+1)
    lastflight=fbf.latest_departure(int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]), int(flightgroup_to_check[23]),int(flightgroup_to_check[24]))
    
    if(datetime.date.today() < lastflight[0]):
        #GREY CURVES
    
        grey_flights=(int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]), int(flightgroup_to_check[23]), int(flightgroup_to_check[24]))
        grey_plot=[]
        for i in xrange(len(grey_flights)):
            if(grey_flights[i] != 0):
                (times_temp,expedia_temp,kayak_temp)=get_timeseries(grey_flights[i])
                allinone=(times_temp,expedia_temp,kayak_temp)
                grey_plot.append(allinone)
    
        # BEST CURVE
        (group_times,search_times,fares,website,alert,dateA,dateB,fid)=fbf.get_best_timeseries(fgid)
        
        
        filtered_searchtimes=[]
        filtered_fares=[]
        for i in xrange(len(fares)):
            if(fares[i] < 10000):
                filtered_fares.append(fares[i])
                filtered_searchtimes.append(search_times[i])
        
        
        
        #GET ALERT TIMES AND FARES
        (alertdate,alertfare)=fbf.alert_dates_and_fares(fgid)
        
        
        smooth_expedia=[]
        smooth_kayak=[]
        mask_expedia=[]
        mask_kayak=[]
        
        # Replace 0 with none
        
        for m in xrange(len(grey_plot)):
            for n in xrange(len(grey_plot[m][2])):
                if (grey_plot[m][2][n] == 0):
                    grey_plot[m][2][n] = None
            for n in xrange(len(grey_plot[m][1])):
                if (grey_plot[m][1][n] == 0):
                    grey_plot[m][1][n] = None
            
        for m in xrange(len(grey_plot)):   
            smooth_expedia.append(np.array(grey_plot[m][1]).astype(np.double))
            smooth_kayak.append(np.array(grey_plot[m][2]).astype(np.double))
        
        for m in xrange(len(smooth_expedia)): 
            mask_expedia.append(np.isfinite(smooth_expedia[m]))
            mask_kayak.append(np.isfinite(smooth_kayak[m]))
        
        dates_expedia=[]
        dates_expedia_row=[]
        dates_kayak=[]
        dates_expedia_row=[]
        dates_kayak=[]
        
        for m in xrange(len(grey_plot)):
            dates_expedia_row=[]
            for n in xrange(len(grey_plot[m][0])):
                if (grey_plot[m][1][n] != None):
                    dates_expedia_row.append(grey_plot[m][0][n])
            dates_expedia.append(dates_expedia_row)
            
            dates_kayak_row=[]
            for n in xrange(len(grey_plot[m][0])):
                if (grey_plot[m][2][n] != None):
                    dates_kayak_row.append(grey_plot[m][0][n])
            dates_kayak.append(dates_kayak_row)
        
        
        
        
        
        
        
        
        
        
        
        #plt.plot(xs[s1mask], series1[s1mask], linestyle='-', marker='o')
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for m in xrange(len(grey_plot)):
            ax.plot_date(dates_expedia[m], smooth_expedia[m][mask_expedia[m]], fmt='-', marker='o',markersize=3,color='#58ACFA',markeredgecolor='#58ACFA', tz=None, xdate=True, ydate=False)
            ax.plot_date(dates_kayak[m], smooth_kayak[m][mask_kayak[m]], fmt='-', marker='o',markersize=3,color='#F7BE81',markeredgecolor='#F7BE81', tz=None, xdate=True, ydate=False)
        
        ax.plot_date(dates_expedia[0], smooth_expedia[0][mask_expedia[0]], fmt='-', marker='o',markersize=3,color='#58ACFA',markeredgecolor='#58ACFA', tz=None, xdate=True, ydate=False,label="fares for flights on expedia" )
        ax.plot_date(dates_kayak[0], smooth_kayak[0][mask_kayak[0]], fmt='-', marker='o',markersize=3,color='#F7BE81',markeredgecolor='#F7BE81', tz=None, xdate=True, ydate=False, label="fares for flights on kayak" )
        
        ax.plot_date(filtered_searchtimes, filtered_fares, fmt=':',color="#009999", linewidth=3, dashes=(20,20), tz=None, xdate=True, ydate=False)
        ax.plot_date(alertdate,alertfare, fmt='o',color="#009999",markeredgecolor='#009999', markersize=12, tz=None,xdate=True, ydate=False)
        dateFmt = mpl.dates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(dateFmt)
        fig.autofmt_xdate(bottom=0.18) # adjust for date labels display
        FGname=fbf.get_flightgroup_name(fgid)
        #PlotTitle='$'+str(fares[-1])+' for '+FGname+' on '+website[-1]+' between '+str(dateA[-1].month)+'/'+str(dateA[-1].day)+' and '+str(dateB[-1].month)+'/'+str(dateB[-1].day)
        #title(PlotTitle)
        xlabel('month/day')
        ylabel('Ticket price (USD)')
        vax1=[min(search_times),max(search_times),min(filtered_fares)*0.95,max(filtered_fares)*1.3]
        ax.legend()
        ax.axis(vax1)

        filename = home+'/static/plots/'+str(fgid)+'b.png'
        savefig(filename, dpi=mydpi)
        plt.clf()
        print "created", filename
        time.sleep(wait_time)
        
    

        fig = plt.figure()
        ax = fig.add_subplot(111)
       
        ax.plot_date(filtered_searchtimes, filtered_fares, fmt='-',color="#009999",linewidth=3, tz=None, xdate=True, ydate=False, label="fare for best trip dates")
        ax.plot_date(alertdate,alertfare, fmt='o',color="#009999",markeredgecolor='#009999', markersize=12, tz=None,xdate=True, ydate=False, label="fare alerts")
        dateFmt = mpl.dates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(dateFmt)
        fig.autofmt_xdate(bottom=0.18) # adjust for date labels display
        FGname=fbf.get_flightgroup_name(fgid)
        #PlotTitle='$'+str(fares[-1])+' for '+FGname+' on '+website[-1]+' between '+str(dateA[-1].month)+'/'+str(dateA[-1].day)+' and '+str(dateB[-1].month)+'/'+str(dateB[-1].day)
        #title(PlotTitle)
        xlabel('month/day')
        ylabel('Ticket price (USD)')
        vax1=[min(search_times),max(search_times),min(filtered_fares)*0.95,max(filtered_fares)*1.3]
        ax.legend(numpoints=1)
        ax.axis(vax1)
        
        
        filename = home+'/static/plots/'+str(fgid)+'a.png'
        savefig(filename, dpi=mydpi)
        plt.clf()
        print "created", filename
        time.sleep(wait_time)


        if(fgid < 18): 
        
            kayak_exact_temp = open (home+'/kayak_exact_daily.txt',"r" )
            kayak_exact = kayak_exact_temp.readlines()
            kayak_exact_temp.close()

            KED_dates=list()
            KED_fares=list()
            
            for n in xrange(len(kayak_exact)):
                line=kayak_exact[n]
                splitup=line.split(',') 
                kyear,kmonth,kday,khour,kminute=splitup[0].split('-')
                KED_dates.append(datetime.datetime(int(kyear)+2000,int(kmonth),int(kday),int(khour),int(kminute)))
                KED_fares.append(int(splitup[fgid]))
                
                #print fgid,KED_fares
            
            fig = plt.figure()
            ax = fig.add_subplot(111)

            ax.plot_date(filtered_searchtimes, filtered_fares, fmt='-',color="#009999",linewidth=3, tz=None, xdate=True, ydate=False)
            ax.plot_date(alertdate,alertfare, fmt='o',color="#009999",markeredgecolor='#009999', markersize=12, tz=None,xdate=True, ydate=False, label='farebeast alert')
            ax.plot_date(KED_dates,KED_fares, fmt='o', color='#F7BE81', markeredgecolor='#F7BE81', markersize=12, tz=None,xdate=True, ydate=False, label='kayak alert')
            
            dateFmt = mpl.dates.DateFormatter('%m/%d')
            ax.xaxis.set_major_formatter(dateFmt)
            fig.autofmt_xdate(bottom=0.18) # adjust for date labels display
            FGname=fbf.get_flightgroup_name(fgid)
            #PlotTitle='$'+str(fares[-1])+' for '+FGname+' on '+website[-1]+' between '+str(dateA[-1].month)+'/'+str(dateA[-1].day)+' and '+str(dateB[-1].month)+'/'+str(dateB[-1].day)
            #title(PlotTitle)
            xlabel('month/day')
            ylabel('Ticket price (USD)')
            vax1=[min(search_times),max(search_times),min(filtered_fares)*0.95,max(filtered_fares)*1.3]
            ax.legend(numpoints=1)
            ax.axis(vax1)

            filename = home+'/static/plots/'+str(fgid)+'c.png'
            savefig(filename, dpi=mydpi)
            plt.clf()
            print "created", filename
            time.sleep(wait_time)

        else:
            
            fig = plt.figure()
            ax = fig.add_subplot(111)

            ax.plot_date(filtered_searchtimes, filtered_fares, fmt='-',color="#009999", linewidth=3, tz=None, xdate=True, ydate=False, label="fare for best trip dates")
            ax.plot_date(alertdate,alertfare, fmt='o',color="#009999",markeredgecolor='#009999', markersize=12, tz=None,xdate=True, ydate=False, label="fare alerts")
            dateFmt = mpl.dates.DateFormatter('%m/%d')
            ax.xaxis.set_major_formatter(dateFmt)
            fig.autofmt_xdate(bottom=0.18) # adjust for date labels display
            FGname=fbf.get_flightgroup_name(fgid)
            #PlotTitle='$'+str(fares[-1])+' for '+FGname+' on '+website[-1]+' between '+str(dateA[-1].month)+'/'+str(dateA[-1].day)+' and '+str(dateB[-1].month)+'/'+str(dateB[-1].day)
            #title(PlotTitle)
            xlabel('month/day')
            ylabel('Ticket price (USD)')
            vax1=[min(search_times),max(search_times),min(filtered_fares)*0.95,max(filtered_fares)*1.3]
            ax.legend(numpoints=1)
            ax.axis(vax1)


            filename = home+'/static/plots/'+str(fgid)+'c.png'
            savefig(filename, dpi=mydpi)
            plt.clf()
            print "created", filename
            time.sleep(wait_time)

print "All done!"

