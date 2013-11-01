import csv, sys
from Crypto.Cipher import DES
import MySQLdb as mdb
import sys
import urllib2
import urllib
import os
import subprocess
import time

obj=DES.new('abcdefgh', DES.MODE_ECB)
#filename = '/home/abdelbar/encryption/csvfile.csv'

try:
    con = mdb.connect('localhost', 'root', '066abde', 'crypt');
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print "Database version : %s " % ver
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)

csvfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk('/home/abdelbar/encryption/')
             for name in files
             if name.endswith((".csv"))]

def criptage(filename) :
	with open(filename, 'rb') as f:
		reader = csv.reader(f,delimiter=';')
		try:
			res=""
			x=['','','','','','']
			for row in reader:
				n=0
				for i in row:
							#cryptage cette section peut etre remlacer avec une focntion
							if len(i)%8==0 :
								res=obj.encrypt(i)
								print res
								print obj.decrypt(res).replace("*","")
							else : 
								for j in range(8-int(len(i)%8)) : i+="*"
								res=obj.encrypt(i)
								print res
								print obj.decrypt(res).replace("*","")
							x[n]=res
							n+=1
				cur = con.cursor()
				sql="INSERT INTO crypto (NE,ND,AE,AD,date,text) VALUES (%s, %s, %s, %s, %s, %s)"
				cur.execute(sql,[x[0],x[1],x[2],x[3],x[4],x[5]])
				con.commit()
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

for filename in csvfiles :
	criptage(filename)
	p=subprocess.Popen("rm %s" %filename,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

con.close()
#Aglagane Abdelbar ; abdellbar@gmail.com