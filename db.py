import sqlite3


#Connect to database
conn = sqlite3.connect("office_hours.db") 
#Turn foreign keys on
conn.execute("PRAGMA foreign_keys = ON")
#Create cursor object
cursor = conn.cursor()

'''Functions that interact with database'''

def create():
#Create the tables if not created already
	cursor.execute("""CREATE TABLE IF NOT EXISTS tutors 
					(name CHAR(20) PRIMARY KEY, 
					start INTEGER, 
					end INTEGER)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS sessions 
					(id INTEGER PRIMARY KEY, 
					student_name CHAR(20), 
					tutor_name CHAR(20), 
					start INTEGER, 
					end INTEGER, 
					FOREIGN KEY(tutor_name) REFERENCES tutors(name))""")

	return 

#Add data to Tutors table
def add_tutor(name, start, end):
	if new_tutor(name):
		cursor.execute("""INSERT INTO tutors (name, start, end)
						VALUES (?, ?, ?)""", (name, int(start), int(end)))
		conn.commit()
		return "Added %s available %s to %s." % (name, convert(start), convert(end))
	
	else: 
		return "ERROR: %s already in database. Tutor names must be unique." % (name)

#Add data to Session table
def add_session(stu_name, tu_name, start, end):
	cursor.execute("""INSERT INTO sessions (student_name, tutor_name, start, end) 
							VALUES (?, ?, ?, ?)""", (stu_name, tu_name, start, end))
	conn.commit()
	return "Scheduled %s with %s from %s to %s."%(stu_name, tu_name, convert(start), convert(end))

#Retrieve tutor schedule
def tutor_sched(name):
	sched = cursor.execute("""SELECT student_name, start, end 
								FROM sessions 
								WHERE tutor_name= (?) 
								ORDER BY start""", (name,))

	return printable_format(sched)



#retrieve student schedule
def stu_sched(name):
	sched = cursor.execute("""SELECT tutor_name, start, end 
								FROM sessions 
								WHERE student_name = (?) 
								ORDER BY start""", (name,))
	
	return printable_format(sched)

#disconnect from database
def close_db():
	conn.close()
	return 

''' Helper functions '''

#Change time format for output
def convert(time):
	if int(time) == 0:
		return "12:00am"

	elif int(time) < 1200:
		return time[:-2] + ":" + time[-2:] + "am"

	elif int(time) < 1300: 
		return time[:-2] + ":" + time[-2:] + "pm"
	
	else: 
		new_time = str(int(time) - 1200)
		return new_time[:-2] + ":" + new_time[-2:] + "pm"

#nicely format schedule for printing
def printable_format(sched):
	sessions_list = ""
	
	for row in sched: 
		sessions_list = sessions_list + "-- " + convert(row[1]) + " to " + convert(row[2]) + " with " + row[0] + "\n"
	
	print sessions_list
	return

#check for unique values
def new_tutor(name):
	cursor.execute("""SELECT name
						FROM tutors 
						WHERE name = ?""",(name,))
	
	results = cursor.fetchall()
	
	if len(results)== 0:
		return True
	else: 
		return False

#check if tutor works during those hours and if tutor is available
def open_tu(name, start, end):
#is tutor in database?
	if new_tutor(name) == True: 
		return "no_tutor"

#find hours tutor works
	hours = cursor.execute("""SELECT start, end
						FROM tutors
						WHERE name = ?""", (name,))

	hours = cursor.fetchall()

#make sure tutor works during session time
	if hours[0][0] > int(start) or hours[0][1] < int(end):
		return "unavail"

#find tutor's session times
	cursor.execute("""SELECT start, end 
						FROM sessions 
						WHERE tutor_name = ?
						ORDER BY start""", (name,))

	results = cursor.fetchall()

	overlap_time = overlap(results, start, end)

#check for overlap between tutor's sessions and requested session

	if len(results) == 0:
		return True

	elif overlap_time == True: 
		return "overlap"
			
	elif overlap_time == False:
		return True

	else:
		return "ERROR"
	

#check if student already has session scheduled
def open_stu(name, start, end):
	cursor.execute("""SELECT start, end 
						FROM sessions 
						WHERE student_name = ?""", (name,))

	results = cursor.fetchall()

	if len(results) == 0 or overlap(results, start, end) == False:
		return True

	if overlap(results, start, end) == True:
		return False

#check for overlap with info from database and requested session start and end 
def overlap(results, start, end):

 	start_i = int(start) 
 	end_i = int(end)

 	for x in range(len(results)):
 		#modify range so classes may start and end back to back
		if start_i in xrange(results[x][0], results[x][1]):
			return True
		elif end_i in xrange(results[x][0], results[x][1]):
			return True
	return False



'''Check database functions'''

#Print tutors table
def get_tutors():
	for row in cursor.execute("""SELECT * FROM tutors"""):
		print row

#Print sessions table
def get_sessions():
	for row in cursor.execute("""SELECT * FROM sessions"""):
		print row

