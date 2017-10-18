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
# Populating the db
#==========================================================

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
    if len(Listy) == 0: #Catch div by 0 error
        return 0
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

def add_table():
    info = get_stud_info()
    c.execute("CREATE TABLE peeps_avg (id int, avg int);")
    for each in info:
        each = each.split(',')
        c.execute("INSERT INTO peeps_avg VALUES (%d, %d);"%(int(each[1]), int(each[2])))

def update_grade(sid, course, new_grade):
    command = "UPDATE courses SET mark = %d WHERE id = %d AND code = \"%s\";"%(new_grade, sid, course)
    c.execute(command);
    return update_average(sid)

def update_average(sid):
    grades_list = get_grades(sid)
    thesum = sum(grades_list)
    if len(grades_list) == 0: #Catch div by 0 error
        return 0
    new_average = thesum / len(grades_list)
    tuple_sid = (sid,)
    command = "UPDATE peeps_avg SET avg = \"%s\" WHERE id = %s;"%(str(new_average), tuple_sid)
    return new_average

    
    
#==========================================================
# Testing Functions
#==========================================================

print "Testing functions... \n"

print "Getting grades for student 1:"
print get_grades(1)

print "\nGetting mean for student kruder:"
print get_mean('kruder')

print "\nPrinting info for all students..."
for each in get_stud_info():
    print each
print '\n'

print "Creating a table of ids & avgs..."
add_table()
for each in c.execute("SELECT * FROM peeps_avg;"):
    print "%d: %d"%(each[0], each[1])

print "Updating average..."
print "Old average kruder = 79, changing 65 to 75, new average should be 83"
print update_grade(1, "softdev", 75)

db.commit() #save changes
db.close()  #close database
