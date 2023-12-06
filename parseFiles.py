from psycopg2 import OperationalError, connect
from psycopg2.extras import DictCursor
import os
from datetime import datetime
import shutil

class Colors:
	RST = '\033[0m'
	RD = '\033[91m'
	GN = '\033[92m'
	IL = '\033[3m'

DIRECTORY = "test/" # Directory of files that must be parsed
DESTINATION = "complete/" #Directory of where to move processed files to
FILES = [file for file in os.listdir(DIRECTORY)]
COUNT = 0


# DATABASE INFO
# COMPLETE THIS SECTION!!!
# Enter table name, username, password, host/url, port, databasename
TABLE_NAME = "tablename" 
credentials = {'user' : "enterusername",
			   'password' :"enterpassword",
			   'host' :"enterhostname/url",
			   'port' : "enterportnumber",
			   'dbname' : "enterdatabasename"}

try:
	cnx = connect(**credentials)
	cnx.autocommit=True
	cursor = cnx.cursor(cursor_factory=DictCursor)
	print(f"{Colors.GN}Connection successful!\n{Colors.RST}")
	error_log = open("errorlog.txt", 'a')
	resubmit = open("resubmit.txt", 'a')
	success_log = open("successlog.txt", 'a')
except OperationalError:
	print(f"{Colors.RD}Connection failedn{Colors.RST}")
	exit()

# Change left side to column name in your database table
# Change right side to the word/phrase you are looking for in files you are parsing
# For example uname = "USERNAME:"
column1 = "keyword1"
column2 = "keyword2"
column3 = "keyword3"

# If you need more or less keywords for your parsing, simply add or remove
# Also add/remove the corresponding value in below code!


for eachfile in FILES:
	COUNT += 1
	with open(DIRECTORY + eachfile,"r") as file:
		print("Uploading file to database [" + eachfile + "]")
		line = file.readline()
		while (line):
			while (len(line) > 0 and line[:len(keyword1)] != keyword1):
				line = file.readline()
			if (len(line) > 0 and line[:len(keyword1)] == keyword1):
				# Number of values should match number of keywords you are looking for
				value1 = "" 
				value2 = ""
				value3 = ""
				
				value1 = line[len(keyword1) + 1:].strip()
				line = file.readline()
				if (len(line) > 0 and line[:len(keyword2)] == keyword2):
					value2 = line[len(keyword2) + 1:].strip()
				line = file.readline()
				if (len(line) > 0 and line[:len(keyword3)] == keyword3):
					value3 = line[len(keyword3) + 1:].strip()
				try:
					sql = f"INSERT INTO {TABLE_NAME} ({column1}, {column2}, {column3}) values ('{value1}' , '{value2}', '{value3}')"
					cursor.execute(sql)
				except Exception as e:
					error_log.write("FILE: " + eachfile + f" Failed to add {keyword1}:" + value1 + 
						f" | {keyword2}: " + value2 + f" | {keyword3}: " + value3 
						+ "\nError: " + str(e) + '\n-----\n')
					
					resubmit.write( f"{keyword1}: " + value1 +'\n' + \
									f"{keyword2}: " + value2 +'\n' + \
									f"{keyword3}: " + value3 +'\n\n')
			else:
				line = file.readline()

	print(Colors.GN + "PROCESSED: " + eachfile + " FILE NUMBER " , COUNT , Colors.RST)

	success_log.write(datetime.now().strftime("%d/%m/%y %H:%M") + " : Success: "+ DIRECTORY + eachfile + '\n')
	try:
		shutil.move(DIRECTORY+eachfile, DESTINATION)
		print(Colors.IL + eachfile + " successfully moved to location: " + DESTINATION, '\n', Colors.RST)
	except Exception as e:
		print(Colors.RD + "Error: Unable to move file " + eachfile + " to " + DESTINATION + "\n" + str(e) ,'\n', Colors.RST)

print(Colors.GN + "All files processed!", Colors.RST)
cnx.close()
