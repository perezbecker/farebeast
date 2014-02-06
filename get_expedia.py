
import os
import sys
import re
import urllib, string, fileinput, sys
import time
import socket
import urllib2
import httplib

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

minfare_expedia=0
req = urllib2.Request(sys.argv[1])

try:
    try:
        ref = urllib2.urlopen(req, timeout=30)
    
    except httplib.IncompleteRead, e:
        ref = e.partial
        print "Expedia Incomplete Read"
    
    #BEGIN Experimental
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)
    #END Experimental
    
    text=ref.readlines()
    fares_expedia=list()

    text.pop()
    for i in text:
        if "<B>$" in i:
            price=re.findall(r'<B>\$(\S+)</B>',i)
            try:
                fares_expedia.append(int(price[0].replace(",", "")))
            except ValueError: 
                fares_expedia.append(1000000)
    try:
        minfare_expedia=min(fares_expedia)
    except ValueError: 
        minfare_expedia=0

except urllib2.URLError:
    print "Expedia URL Error"
    minfare_expedia=0
    #continue # skips to the next iteration of the loop

except socket.timeout:
    print "Expedia socket timeout"
    minfare_expedia=0
    #continue # skips to the next iteration of the loop
    
sys.stdout.write(str(minfare_expedia))