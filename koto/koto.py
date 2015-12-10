'''koto

Usage:
	koto [-h | --help | -v | --version]
	koto status [-a | --all]
	koto add [TYPE] FIRSTNAME LASTNAME [EMAIL]
	koto commit FIRSTNAME [LASTNAME] [-fb | -e | -m] COMMIT

Optional arguments:
	-h --help     Show help dialog
	-v --version  Show verison number

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

import db_methods, gmail_methods

import sys

from docopt import docopt

g = gmail_methods
db = db_methods
db_name = 'kotodb'

#put quotations around "COMMIT" ?

def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	#use id's for commits
	pass

def print2(test):
	print(test)

def main():
	arguments = (docopt(__doc__, version='0.1.1'))
	print(arguments)
	# print ("hi: " + sys.argv[0])

	db.initializeDB()
	db.insertDB('Ben', 'Shukman')
	db.readDB('Ben')
	db.addEmail('Yana', 'yanaspace@gmail.com')
	db.addEmail('Ben', 'shukipost@gmail.com')
	db.readDB('Ben')

	for row in db.readEmail('Ben'):
		query = row	
	print (query)

	credentials = g.get_credentials()
	http = credentials.authorize(g.httplib2.Http())
	service = g.discovery.build('gmail', 'v1', http=http)

	'''
	print("debug here: ")
	test = g.getLatest(service, "me", "from: shukipost@gmail.com")['id']
	print(g.GetMessage(service, "me", test)['snippet'])
	'''
	
	'''
	tempmsg = g.GetMessage(service, "me", g.getLatest(service, "me", "from: yanapost@gmail.com")['id'])
	print (g.extractBody(tempmsg)

	msgs = g.ListMessagesMatchingQuery(service, "me", query)

	message = g.GetMessage(service, "me", msgs[3]['id'])

	# snippet = g.GetMessage(service, "me", msgs[3]['id'])['snippet']
	# print (snippet)

	print (g.extractBody(message))
	'''
	

	#import list of investors

	#grab email of each
	emails = db.readAllEmails()

	#look up ID of latest email
	for x in emails:
		print("last message received from " + "{0}" + ":") .format(x[0])
		msgID = (g.getLatest(service, "me", "from: {0}".format(x[0]))['id'])
		print("message ID: " + msgID)

		#calculate date of email + days since last comm + get snippet

		#list the data
		date = g.getDate(service, msgID)
		print("received on: " + str(date))
		print(g.daysSince(date) + " since last communication")

		print("")
		print(g.GetMessage(service, "me", msgID)['snippet'])
		print("")


if __name__ == '__main__':
	main()


#template code:
	#for each investor in a list:
		#when is the last time we talked?
		#snippet of last conversation
		#num. of total conversations

