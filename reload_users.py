import MySQLdb as mdb
import datetime
import string
from math import ceil

def get_from_list():
    alluserdata = open ("users.txt","r" )
    userdatalines = alluserdata.readlines()
    alluserdata.close()
    
    userdata=[]
    for i in xrange(len(userdatalines)):
        line=userdatalines[i]
        split=string.split(line)
        # data ordered as "uid, username, password, email, mobile, carrier, datajoined"
        userdata.append((split[1],split[2],split[3],split[4],split[5],datetime.date.today()))
    return userdata


def drop_create_users():
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    
    with con: 
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS `users`")
        cur.execute("CREATE TABLE `users` (`uid` int NOT NULL AUTO_INCREMENT, `user` varchar(100) NOT NULL, `password` varchar(100) NOT NULL, `email` varchar(100) NOT NULL, `mobile` char(10) NOT NULL, `carrier` varchar(100) NOT NULL,`datejoined` date NOT NULL, PRIMARY KEY (`uid`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8")

    
def insert_users(userdata):
    con = mdb.connect(host='localhost', user='root', db='farebeast')
    
    # Create the insert strings
    column_str = "user, password, email, mobile, carrier, datejoined"
    insert_str = ("%s, " * 6)[:-2]
    final_str = "INSERT INTO users (%s) VALUES (%s)" % (column_str, insert_str)
    #print final_str, len(userdata)
    
    # Insert each symbol
    with con: 
        cur = con.cursor()
        # This line avoids the MySQL MAX_PACKET_SIZE
        # Although of course it could be set larger!
        for i in range(0, int(ceil(len(userdata) / 100.0))):
            cur.executemany(final_str, userdata[i*100:(i+1)*100-1])



if __name__ == "__main__":
    userdata = get_from_list()
    drop_create_users()
    insert_users(userdata)
