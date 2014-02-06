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


message='Hello Danok,\n \n This is test message. \n \n  --- FareBeast ---' 

subject="FareBeast Email Test"
attachment=home+'/static/plots/1a.png'
email="daniel@perezbecker.com"

gmailbeast.sendMail(email, subject, message, attachment)


smsrecipient='5106218790@txt.att.net'


smsmessage="This is a FareBeast test.\n --- FareBeast ---"
smssubject="FareBeast Test!"
if (smsrecipient != "none"):
    smsgmailbeast.sendMail(smsrecipient,smssubject,smsmessage)