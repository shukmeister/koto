import sqlite3

db_name = 'kotodb'

def initializeDB():
	print ('Initializing database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS people(firstName text, lastName text, type text, email text, UNIQUE(firstName, lastName))")
	conn.close()

def insertDB(firstName, lastName):
	print ('Inserting ' + firstName + ' ' + lastName + ' into database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
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
	print ('Reading emails from database ' + db_name + '...' + '\n')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("SELECT email FROM people")
	return c.fetchall()
	conn.close()

def readDB(firstName):
	print ('Reading ' + firstName + ' from database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("SELECT * FROM people WHERE firstName =?", [firstName])
	print (c.fetchall())
	conn.close()

def readEmail(firstName, lastName=None):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("SELECT email FROM people WHERE firstName =?", [firstName])
	return (c.fetchone())
	#if multiple, specify ask which one
	conn.close()

def addEmail(email, firstName):
	conn = sqlite3.connect(db_name)
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