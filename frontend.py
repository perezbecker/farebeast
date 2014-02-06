from flask import Flask
from flask import request, url_for
from flask import render_template
import webfunctions as wf
import farebeast_functions as fbf
from matplotlib.dates import date2num
import datetime

app = Flask(__name__)

app.config.update( DEBUG=True)
app.secret_key = "chingados384579847"

@app.route('/')
def my_index():
   
   user_table=wf.get_user_table()

   return render_template("index.html",users=user_table[1])


@app.route('/join_now')
def join_now():

    try:
        username=str(request.args.get("username",None))
        email=str(request.args.get("email",None))
        mobile=str(request.args.get("mobile",None))
        carrier=str(request.args.get("carrier",None))
        
        print 'mobile=', mobile
        
        if (mobile == ''):
            mobile='9999999999'
        
    
        mobile=int(mobile)

        username=username.replace(' ','_')

        password='nopassword'
        date_joined=datetime.date.today()
  
        userdata=[username,password,email,mobile,carrier,date_joined]
  
        if(wf.user_doesnt_exist(username)):
            wf.insert_users(userdata)
            wf.add_user_to_file(userdata)

  
        user_table=wf.get_user_table()


        return render_template("join_now.html",users=user_table[1],username=username)
    
    except:
        
        return render_template("error.html")





@app.route("/add_flight")
def add_flight():
    
    user_table=wf.get_user_table()
    
    user=str(request.args.get("user",None))
    
    welcome="Adding trip for "+user
    
    return render_template("add_flight.html",users=user_table[1],welcome=welcome, active_user=user)

@app.route("/add_verification")
def add_verification():

    try:
        user_table=wf.get_user_table()

        portA_long=str(request.args.get("PortA",None))
        dateA=str(request.args.get("dateA",None))
        portB_long=str(request.args.get("PortB",None))
        dateB=str(request.args.get("dateB",None))
        extraA=str(request.args.get("extraA",None))
        extraB=str(request.args.get("extraB",None))
        min_d=str(request.args.get("min_d",None))
        max_d=str(request.args.get("max_d",None))
        active_user=str(request.args.get("active_user",None))
        nickname=str(request.args.get("nickname",None))
    
    
        portA=portA_long[0:3]
        portB=portB_long[0:3]
    
        if (nickname==''):
            nickname=portA+'-'+portB+'_on_'+dateA
    
        nickname=nickname.replace(' ','_')
    
        if (min_d==''):
            min_d=0
    
        if (max_d==''):
            max_d=0
    
        ddateA=wf.DateUS2GER(dateA)
        ddateB=wf.DateUS2GER(dateB)
    
        ValidDates = wf.GenerateDatesWeb(ddateA,ddateB,int(extraA),int(extraB),int(min_d),int(max_d))
    
        #from code import interact; interact(local=locals())
        #FlightList=[dayA,monthA,yearA,dayB,monthB,yearB,NoOfDays,weekdaylist[DayOfWeekA],weekdaylist[DayOfWeekB]]
    
    
        messages=[]
        for i in xrange(min(len(ValidDates),20)):
            j=i+1
            messages.append('Flight '+("%02d" %j)+': '+ValidDates[i][7]+' '+ValidDates[i][1]+'/'+ValidDates[i][0]+' to '+ValidDates[i][8]+' '+ValidDates[i][4]+'/'+ValidDates[i][3]+' ('+ValidDates[i][6]+' days)')
        
    
    
        welcome="Preparing trip \""+nickname+"\" for "+active_user
    
        return render_template("add_verification.html",welcome=welcome,messages=messages,active_user=active_user,nickname=nickname,users=user_table[1],portA=portA,portB=portB,dateA=dateA,dateB=dateB,extraA=extraA,extraB=extraB,min_d=min_d,max_d=max_d)

    except:
        
        return render_template("error.html")


@app.route('/trip_added')
def trip_added():

    user_table=wf.get_user_table()

    portA=str(request.args.get("PortA",None))
    dateA=str(request.args.get("dateA",None))
    portB=str(request.args.get("PortB",None))
    dateB=str(request.args.get("dateB",None))
    extraA=str(request.args.get("extraA",None))
    extraB=str(request.args.get("extraB",None))
    min_d=str(request.args.get("min_d",None))
    max_d=str(request.args.get("max_d",None))
    active_user=str(request.args.get("active_user",None))
    nickname=str(request.args.get("nickname",None))
    
    
    # uid_index=user_table[1].index(active_user)
    #     uid=user_table[0][uid_index]
    

    my_message='Created Trip '+nickname+' for '+active_user+' between '+portA+' and '+portB+'.'

    #for_computer=active_user+', '+nickname+', '+portA+', '+portB+', '+dateA+', '+dateB+', '+extraA+', '+extraB+', '+min_d+', '+max_d+', 0, 0'
    wf.add_flightgroup_to_file(active_user,nickname,portA,portB,dateA,dateB,extraA,extraB,min_d,max_d)
    
    return render_template("trip_added.html",users=user_table[1],message=my_message)





@app.route('/check_flights')
def check_flights():
   
   user_table=wf.get_user_table()
   user=str(request.args.get("user",None))
   
   uid_index=user_table[1].index(user)
   uid=user_table[0][uid_index]
   
   fgids=wf.get_gfids(uid)
   
   trips=[]
   embryos=[]
   
   
   born_fgids=[]
   embryo_fgids=[]
   for fgid in fgids:
       try:
          with open('static/plots/'+str(fgid)+'a.png'):
              born_fgids.append(fgid)
              print fgid, "born"
       except IOError:
           embryo_fgids.append(fgid)
           print fgid, "embryo"


   
   for fgid in born_fgids:
       
       graph1=str(fgid)+"a.png"
       graph2=str(fgid)+"b.png"
       graph3=str(fgid)+"c.png"
       FGname=fbf.get_flightgroup_name(fgid)
       (group_times,search_times,fares,website,alert,dateA,dateB,fid)=fbf.get_best_timeseries(fgid)
       
       (portA,portB)=fbf.get_flightgroup_ports(fgid)
       
       fare_of_last_alert=int(fbf.fare_of_last_alert(fgid))
       days_since_last_alert=int(fbf.days_since_last_alert(fgid))
       min_fare_within_last_week=int(fbf.min_fare_within_last_week(fgid))
       avg_fare_within_last_week=int(fbf.avg_fare_within_last_week(fgid))
       
       if(days_since_last_alert > 999):
           days_since_last_alert='N/A'
           fare_of_last_alert='N/A'
           
       
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
       
       flightgroup_to_check=fbf.read_flightgroups(fgid)
       lastflight=fbf.latest_departure(int(flightgroup_to_check[5]), int(flightgroup_to_check[6]), int(flightgroup_to_check[7]), int(flightgroup_to_check[8]), int(flightgroup_to_check[9]), int(flightgroup_to_check[10]), int(flightgroup_to_check[11]), int(flightgroup_to_check[12]), int(flightgroup_to_check[13]), int(flightgroup_to_check[14]), int(flightgroup_to_check[15]), int(flightgroup_to_check[16]), int(flightgroup_to_check[17]), int(flightgroup_to_check[18]), int(flightgroup_to_check[19]), int(flightgroup_to_check[20]), int(flightgroup_to_check[21]), int(flightgroup_to_check[22]), int(flightgroup_to_check[23]), int(flightgroup_to_check[24]))

       DaysUntilFlight=float(date2num(lastflight[0]))-float(date2num(datetime.datetime.utcnow()))
       
       
       trip_to_show=[gourl,graph1,graph2,graph3,portA,portB,FGname,fares[-1],fare_of_last_alert,days_since_last_alert,avg_fare_within_last_week, min_fare_within_last_week,int(DaysUntilFlight)]
       trips.append(trip_to_show)
       
   
   for fgid in embryo_fgids:
       FGname=fbf.get_flightgroup_name(fgid)
       (portA,portB)=fbf.get_flightgroup_ports(fgid)
       embryo_to_show=[FGname,portA,portB]
       embryos.append(embryo_to_show)
   
   
   if (len(born_fgids)==0 and len(embryo_fgids)==0):
       user_approval='Awaiting administrator approval for '+user+'.'
   
   else:
       user_approval=''
   
   return render_template("check_flights.html",trips=trips,embryos=embryos,user_approval=user_approval,users=user_table[1])
   

     


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)