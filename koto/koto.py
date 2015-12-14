'''
Koto - Communication tracking CLI
Created by Ben Shukman

Usage:
	koto [-h | --help | --version]
	koto init
	koto status (all | <firstname> [<lastname>])
	koto add <firstname> <lastname> [<email>]
	koto delete <firstname> [<lastname>]
	koto commit <firstname> [<lastname>] <commit>
	koto list [-e | --email] [-t | --time]
	koto import

Optional arguments:
	-h --help  Show help dialog
	--version  Show verison number

The most commonly used git commands are:
   add        Add file contents to the index
   branch     List, create, or delete branches
   checkout   Checkout a branch or paths to the working tree
   clone      Clone a repository into a new directory
   commit     Record changes to the repository
   push       Update remote refs along with associated objects
   remote     Manage set of tracked repositories

See 'koto help <command>' for more information on a specific command.
'''


#koto - communication tracking utiliity
#created by ben shukman

#each name has attributes: last date contacted, each contact is a commit (so its a unique data struct)

#store JSON / class of data

#import list of names
#if recent email, display in high priority
#if name is under X days old, needs love

#TODO: add email validation and error handling for gmail errors
#TODO: add to database: validated field + last time communicated field
#TODO: koto status -> more comprehensive overview of comms
	#TODO: # of times talked to an investor
#TODO: finish main koto command
	# - run validation + update last time communicated (+ num. of times communicated if needed)
	# - 
#TODO: import file CSV

#write up read.me -> show ppl

#TODO: add commits
#TODO: add commit trees
#TODO: add person types, koto add [friend | associate | investor] 
#TODO: add commit types [-fb| -e| -m] w/ documentation
#TODO: for 'jeeves?' pull from sublime todo also


import db_methods, gmail_methods

from docopt import docopt

g = gmail_methods
db = db_methods
versionNumber = '0.1.2'

def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	#use id's for commits
	pass

def main():
	arguments = (docopt(__doc__, version=versionNumber))

	#check if version is up to date

	if (db.firstStartupCheck()):
		if arguments['init']:
			pass
		else:
			print("This looks like your first time using koto.  Run 'koto init' to initialize setup.")
			db.exit()

	'''

	koto standard command:
	- high priority
	- new emails
	- needs love
		- someone filter only ones in [recent-ish] communication (<2 months?)
	- forgotten (maybe)

	format:
	First Last - 6 days ago (if > 31 days, say months (1 month, 5 days ago))


	koto status should be comprehensive, not for only one msg
	'''

	if arguments['init']:

		print('\nInitializing koto setup\n')

		import json
		#check if version up to date

		#gmail authentication
		print("Authenticating gmail connection")
		success = g.get_credentials()
		if (success):
			print("Authentication successful")

		#database creation
		db.initializeDB()

		#settings file creation
		db.initializeSettings()
		with open('/usr/local/Library/Koto/koto_settings.txt', 'w') as outfile:
			json.dump({'updateTime':'', 'responseTime':'',}, outfile)

		#set up personal usage settings
		print("\nHow often do you want to update your contacts? Answer in days")
		updateTime = db.selectNumber()
		#write updateTime to a file

		print("What is the maximum number of days that can pass before a response?")
		responseTime = db.selectNumber()
		#write responseTime to a file

		with open('/usr/local/Library/Koto/koto_settings.txt', 'w') as outfile:
			json.dump({'updateTime': updateTime, 'responseTime': responseTime}, outfile)

		#ask to import CSV
		print("Do you have a list of contacts to import? (Y/N)")
		importBoolean = db.selectBoolean()
		if (importBoolean):
			db.importCSV()

		print("\nWelcome to koto!  Use '--help' to learn more")

	credentials = g.get_credentials()
	http = credentials.authorize(g.httplib2.Http())
	service = g.discovery.build('gmail', 'v1', http=http)

	#grab updateTime and responseTime from a file

	if arguments['add']:
		if arguments['<email>']:
			# print("Adding " + str(arguments['<firstname>']) + " " + str(arguments['<lastname>']) + " to database")
			db.insertDB(arguments['<firstname>'].capitalize(), arguments['<lastname>'].capitalize())
			db.addEmail(arguments['<email>'], arguments['<firstname>'].capitalize(), arguments['<lastname>'].capitalize())
		else:
			# print("Adding " + str(arguments['<firstname>']) + " " + str(arguments['<lastname>']) + " to database")
			db.insertDB(arguments['<firstname>'].capitalize(), arguments['<lastname>'].capitalize())

	if arguments['import']:
		db.importCSV()

	elif arguments['status']:
		if (arguments['all']):
			#grab email of each
			emails = db.readAllEmails()

			#look up ID of latest email

			print("Gathering last messages from database \n")
				
			for x in emails:

				name = db.readName(str(x[0]))
				firstName = name[0]
				lastName = name[1]

				#add owner name of email
				print("From: " + str(firstName) + " " + str(lastName) + " ({0})").format(x[0])
				msgID = (g.getLatest(service, "me", "from: {0}".format(x[0]))['id'])
				print("Message ID: " + msgID)

				#calculate date of email + days since last comm + get snippet

			 	#list the data
				date = g.getDate(service, msgID)
				print("Received: " + str(date))
				print(g.daysSince(date) + " since last communication")

				print("")
				print(g.GetMessage(service, "me", msgID)['snippet'])
				print("")



		else:
			print("Gathering last messages from database \n")

			matches = db.countMatches(arguments['<firstname>'].capitalize())

			#if multiple people exist with given first name
			if (matches > 1):

				lastName = db.selectPerson(arguments['<firstname>'].capitalize())

				emailID = db.readEmail(arguments['<firstname>'].capitalize(), lastName.capitalize())[0]
				print("") #to make space away from select person input
				print("From: " + arguments['<firstname>'].capitalize() + " " + lastName.capitalize() + " (" + emailID + ")")
				msgID = (g.getLatest(service, "me", "from: {0}".format(emailID))['id'])
				print("Message ID: " + msgID)

				#calculate date of email + days since last comm + get snippet

			 	#list the data
				date = g.getDate(service, msgID)
				print("Received: " + str(date))
				print(g.daysSince(date) + " since last communication")

				print("")
				print(g.GetMessage(service, "me", msgID)['snippet'])
				print("")

			#if only one person exists with given first name
			elif (matches == 1):
				lastName = db.readLastName(arguments['<firstname>'].capitalize())
				emailID = db.readEmail(arguments['<firstname>'].capitalize(), lastName)[0]
				print("From: " + arguments['<firstname>'].capitalize() + " " + str(lastName) + " (" + emailID + ")")
				msgID = (g.getLatest(service, "me", "from: {0}".format(emailID))['id'])
				print("Message ID: " + msgID)

				#calculate date of email + days since last comm + get snippet

			 	#list the data
				date = g.getDate(service, msgID)
				print("Received: " + str(date))
				print(g.daysSince(date) + " since last communication")

				print("")
				print(g.GetMessage(service, "me", msgID)['snippet'])
				print("")

			elif (matches == 0):
				print ('Error: person with that name does not exist')

	elif arguments['delete']:
		# print("Deleting " + str(arguments['<firstname>']) + " " + str(arguments['<lastname>']) + " from database \n")
		if (arguments['<lastname>']):
			db.deleteDB(arguments['<firstname>'].capitalize(), arguments['<lastname>'].capitalize())
		else:
			db.deleteDB(arguments['<firstname>'].capitalize())

	elif arguments['list']:

		names = db.allNames()

		for x in names:
			if ((arguments['-t'] | arguments['--time']) & (arguments['-e'] | arguments['--email'])):
				msgID = (g.getLatest(service, "me", "from: {0}".format(x[1]))['id'])
				date = g.getDate(service, msgID)
				days = g.daysSince(date)
				email = db.readEmail(x[0], x[1])[0]
				print(x[0] + ' ' + x[1] + ' (' + str(email) + ') - ' + days + ' ago')
			elif (arguments['-e'] | arguments['--email']):
				email = db.readEmail(x[0], x[1])[0]
				print(x[0] + ' ' + x[1] + ' (' + str(email) + ')')
			elif ((arguments['-t'] | arguments['--time'])):
				msgID = (g.getLatest(service, "me", "from: {0}".format(x[1]))['id'])
				date = g.getDate(service, msgID)
				days = g.daysSince(date)
				print(x[0] + ' ' + x[1] + ' - ' + days + ' ago')
			else:
				print(x[0] + ' ' + x[1])
				
	#standard koto command:
	else:
		print('High priority:')
			#if (# of days < X):


		print('Needs love:')
			#if (# of days > X):

		#check if any new investors
		#update validations + num of comms



if __name__ == '__main__':
	main()

