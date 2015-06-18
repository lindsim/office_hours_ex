#import the python file that creates/connects to database
import db
#import re since using regular expressions
import re


''' Functions for commands'''

def tutor (tu_name, start, end):

	time_valid = check_time(start, end, 0)
	name_valid = check_name(tu_name)
	
	if time_valid != True:
		return time_valid

	elif name_valid != True:
		return name_valid	

	elif time_valid and name_valid:
		
		return db.add_tutor(tu_name, start, end)
	
	else: 
		return "ERROR: input error."


def reserve (stu_name, tu_name, start, end):
	
	time_valid = check_time(start, end, 1)
	name_valid = check_name(stu_name)
	
	if time_valid != True:
		return time_valid
	elif name_valid != True: 
		return name_valid


  
	open_tutor = db.open_tu(tu_name, start, end)
	
	if open_tutor == "unavail":
		return "ERROR: %s is not available during that time." % (tu_name)
	
	elif open_tutor == "overlap": 
		return "ERROR: %s already has a student during that time." % (tu_name)
	
	elif open_tutor == "no_tutor":
		return "ERROR: %s not in database." % (tu_name)

	elif open_tutor == True:  
		if db.open_stu(stu_name, start, end) == False:
			return "ERROR: %s already has a tutor during that time." % (stu_name)
	
		else:
			return db.add_session(stu_name, tu_name, start, end)

	else:
		return "ERROR: Unknown error."

def schedule(tu_name):
	return db.tutor_sched(tu_name)


def student(stu_name):
	return db.stu_sched(stu_name)


'''Helper functions'''

#verify names contain only alphanumeric characters, dash, and underscore
def alphanum(name, search=re.compile(r'[^a-z0-9-_]').search):
		return not bool(search(name))

#verify correct inputs
def check_name(name):
	#check that name between 3 and 20 characters long, inclusive
	#verify name is alphanumeric + "-" and "_"
	if len(name) >= 3 and len(name) <= 20 and alphanum(name):
		return True
	else:
		return "ERROR: Name input is invalid."

def check_time(time1_str, time2_str, num):
	too_high = ["6", "7", "8", "9"]

	#make sure minutes place < 6 to determine if military time is correct
	if len(time1_str) >= 2 and time1_str[-2] in too_high: 
			return "ERROR: Start time is invalid. Use military time."
			
	if len(time2_str) >= 2 and time2_str[-2] in too_high:
			return "ERROR: End time is invalid. Use military time."

	
	#convert time to int to determine if in correct range
	time1 = int(time1_str)
	time2 = int(time2_str)


	
	if (time1 > 2359 or time1 < 0):
		return "ERROR: Start time is invalid."
	
	if (time2 > 2359 or time2 < 0):
		return "ERROR: End time is invalid."

	if time1 > time2:
		return "ERROR: End time cannot be before start time."

	if (time1 > (time2 - 30)):
			if num == 0:
				return "ERROR: Tutors must be scheduled for at least half an hour."
			else: 
				return "ERROR: Tutoring sessions must be for at least half an hour."
	else:
		return True



'''Set up what runs when file is opened'''

try:
	while True:

		input = raw_input('> ')
		separated = input.split() #will remove extra spaces 
		command = separated[0] 
		arguments = separated[1:]
		db.create()

		if command == "tutor" and len(arguments) == 3:
			print tutor(arguments[0], arguments[1], arguments[2])
		elif command == "reserve" and len(arguments) == 4:
			print reserve(arguments[0], arguments[1], arguments[2], arguments[3])
		elif command == "schedule" and len(arguments) == 1:		
			schedule(arguments[0])
		elif command == "student" and len(arguments) == 1:
			student(arguments[0])
		elif command == "quit":
			break
		else: 
			print "ERROR: Command or arguments invalid."

except KeyboardInterrupt:
	db.close_db()
	pass