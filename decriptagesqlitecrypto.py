from Crypto.Cipher import DES
import MySQLdb as mdb
import sys
import sqlite3
import sys
import os
import subprocess
import time

obj=DES.new('abcdefgh', DES.MODE_ECB)
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('CREATE TABLE base(NE varchar(40), ND varchar(40), AE varchar(100), AD varchar(100), date date, text text, lus varchar(4), id int(11))')
try:
    con = mdb.connect(host='127.0.0.1', user='root', passwd='066abde', db='crypt'); #host='127.0.0.1',port=3307, user='root', passwd='066abde', db='crypt'
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print "Database version : %s " % ver
except mdb.Error, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


def getdata() :
    cur.execute("SELECT * FROM crypto")
    rows = cur.fetchall()
    return rows

def decripte(rows,key):
        for row in rows:
                if len(str(row[0]))%8==0:
                    test="test"
                    #c.execute("INSERT INTO base VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (obj.decrypt(row[0]).replace("*",""),obj.decrypt(row[1]).replace("*",""),obj.decrypt(row[2]).replace("*",""),obj.decrypt(row[3]).replace("*",""),obj.decrypt(row[4]).replace("*",""),obj.decrypt(row[5]).replace("*",""),row[6],row[7])) 
                    #%(obj.decrypt(row[0]).replace("*",""),obj.decrypt(row[1]).replace("*",""),obj.decrypt(row[2]).replace("*","")))
                    sql="INSERT INTO base VALUES (?,?,?,?,?,?,?,?)"
                    c.execute(sql,[obj.decrypt(row[0]).replace("*",""),obj.decrypt(row[1]).replace("*",""),obj.decrypt(row[2]).replace("*",""),obj.decrypt(row[3]).replace("*",""),obj.decrypt(row[4]).replace("*",""),obj.decrypt(row[5]).replace("*",""),row[6],row[7]])
                    conn.commit()
                    #print obj.decrypt(row[0]).replace("*","") + "|"+obj.decrypt(row[1]).replace("*","") +"|"+obj.decrypt(row[2]).replace("*","") +"|"
                else :
                    print "|"+row[0]+"|"+row[1]+"|"+row[2]+"|"
                print "-------------------------"

def getdatasqlite(option):
    if option=="all":
        c.execute("SELECT * FROM base")
        rows=c.fetchall()
    if option=="new":
        c.execute("SELECT * FROM base WHERE lus='non'")
        rows=c.fetchall()
    return rows

def getmenu():
    var=raw_input("Hello voulez vous aficher:\n 1- l'archive de conevresations \n 2- les conevresations non vues \n 3- quiter \nentrer votre choix: ")
    if var=="1" or var=="2" or var=="3" :
        if var=="1":
            rowsd=getdatasqlite("all")
            x = sum(1 for row in rowsd)
            pages= ((x-x%5)/5)+1
            printdata(rowsd,1,pages,"all")
            getnavigate(1,pages,rowsd,"all")
        if var=="2":
            rowsd=getdatasqlite("new")
            x = sum(1 for row in rowsd)
            pages= ((x-x%5)/5)+1
            print pages
            printdata(rowsd,1,pages,"new")
            getnavigate(1,pages,rowsd,"new") 
        if var=="3":
            exit(1)
    else :
        raw_input("\nEreur! press any key")
        getmenu()

def getnavigate(page,pages,rows,option):
    print         "-----------------------------------------------------------------------"
    var=raw_input("entrer: A- pour avancer  R- pour reculer  Q- quiter entrer votre choix: ")
    if (var=="A" and page<pages) or (var=="R" and page>1) or var=="Q" :
        if var=="A":
            printdata(rows,page+1,pages,option)
            getnavigate(page+1,pages,rows,option)
        if var=="R":
            printdata(rows,page-1,pages,option)
            getnavigate(page-1,pages,rows,option)
        if var=="Q":
            getmenu()
    else :
        raw_input("\nEreur! press any key")
        getnavigate(page,pages,rows,option)  

def setlus(line):
            #x=obj.encrypt("lus*****")
            x="lus"
            y=line[7]
            print y
            sql="UPDATE crypto SET lus=%s WHERE id=%s"
            cur.execute(sql,[x,y])
            con.commit()

def printdata(rows,page,pages,option): # diffrent options for printing

    #for row in rows:
    #        print "|"+row[0]+"|"+row[1]+"|"+row[2]+"|"
    #        print "---------------------------------"
    if (page<=pages) and (page>0):
        for i in range((page-1)*5,page*5):
            if i<len(rows):
                print "======================================================================"
                print "Mesage: --------------"
                print "date: "+rows[i][4]
                print "|From: "+rows[i][0]+"| To: "+rows[i][1]+"\n|Adress Source: "+rows[i][2]+"|Adress distination: "+rows[i][3]
                print "TEXT: --------------"
                print rows[i][5]
                print "======================================================================="
                if option=="new":
                    setlus(rows[i])
            else :
                print "-"

    

def main():
        rows=getdata()
        decripte(rows,'all')
        getmenu()
        #phase d'afichage
        #afficher tous

        #afficher le nauvaux
   


        conn.close()
        con.close()
        return 0

if __name__ == '__main__':
    main()
#Aglagane Abdelbar ; abdellbar@gmail.com