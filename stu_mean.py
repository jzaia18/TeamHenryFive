# Team HenryFive -- Jake Zaia & Michela Marchini
# SoftDev p09
# 2017-10-17
# Work10

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

# Populates courses
c.execute("CREATE TABLE courses (code str, mark int, id int);")

with open('courses.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute('INSERT INTO courses VALUES ("' + str(row['code']) + '",' + str(row['mark']) + ',' + str(row['id']) + ');')

# Populates peeps
c.execute("CREATE TABLE peeps (name str, age int, id int);")

with open('peeps.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute('INSERT INTO peeps VALUES ("' + str(row['name']) + '",' + str(row['age']) + ',' + str(row['id']) + ');')


command = ""          #put SQL statement in this string
c.execute(command)    #run SQL statement

#==========================================================
# Helper Functions
#==========================================================
def get_grades(sid):
    Listy = []
    for each in c.execute("SELECT mark FROM courses WHERE id=%d;"%(sid)):
        Listy.append(each[0])
    return Listy

def get_mean(stud):
    sid = 0
    for each in c.execute("SELECT id FROM peeps WHERE name = \"%s\";"%stud):
        sid = each[0]
    Listy = get_grades(sid)
    thesum = sum(Listy)
    return thesum / len(Listy)

def get_stud_info():
    info_list = []
    for each in c.execute("SELECT name FROM peeps;"):
        name = each[0]
       # print name
        info_list.append(str(name))
    count = 0
    for name in info_list:
        for each in c.execute("SELECT id FROM peeps WHERE name = \"%s\";"%name):
            sid = each[0]
            info_list[count] += ", " + str(sid) + ", " + str(get_mean(name))
            count += 1
    return info_list            


#==========================================================

print get_stud_info()

db.commit() #save changes
db.close()  #close database


