import sqlite3
import os

# db_directory = '/usr/local/Library/Koto'
db_path = '/usr/local/Library/Koto/kotodb'

def initializeDB():
	print ('Initializing database ' + db_path + '...')
	db_directory = os.path.dirname(db_path)
	if not os.path.exists(db_directory):
		os.makedirs(db_directory)
		print ('Directory created')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS people(firstName text, lastName text, type text, email text, UNIQUE(firstName, lastName))")
	print('Database created')
	conn.close()

def insertDB(firstName, lastName):
	print ('Inserting ' + firstName + ' ' + lastName + ' into database ' + db_path + '...')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	# c.execute("CREATE TABLE IF NOT EXISTS people(firstName, lastName, UNIQUE(firstName, lastName))")
	c.executemany("INSERT OR IGNORE INTO people(firstName, lastName) VALUES (?, ?)", [(firstName, lastName)])
	if (c.rowcount != 0):
		print ('Successfully added ' + firstName + ' ' + lastName)
	else:
		print ('Failed to add ' + firstName + ' ' + lastName)
		#add already exists if statement error message
	conn.commit()
	conn.close()

def readAllEmails():
	print ('Reading emails from database ' + db_path + '...' + '\n')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT email FROM people")
	return c.fetchall()
	conn.close()

def readDB(firstName):
	print ('Reading ' + firstName + ' from database ' + db_path + '...')
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT * FROM people WHERE firstName =?", [firstName])
	print (c.fetchall())
	conn.close()

def readEmail(firstName, lastName=None):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute("SELECT email FROM people WHERE firstName =?", [firstName])
	return (c.fetchone())
	#if multiple, specify ask which one
	conn.close()

def addEmail(email, firstName):
	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.executemany("UPDATE people SET email=? WHERE firstName=?", [(email, firstName)])
	# c.executemany("INSERT INTO people (email) VALUES ? WHERE firstName = ?", [email, firstName])
	if (c.rowcount != 0):
		print ('Successfully added ' + email + ' to ' + firstName)
	else:
		print ('Failed to add ' + email + ' ' + firstName)

		#add already exists if statement error message
	conn.commit()
	conn.close()