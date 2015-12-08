#koto - communication tracking utiliity
#created by ben shukman

#each name has attributes: last date contacted, each contact is a commit (so its a unique data struct)

#store JSON / class of data

#import list of names
#if recent email, display in high priority
#if name is under X days old, needs love

from __future__ import print_function

import sqlite3

import httplib2
import os

import base64
import email

from apiclient import discovery
from apiclient import errors
import oauth2client
from oauth2client import client
from oauth2client import tools

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
	Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')

	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print ('An error occurred: %s' % error)

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id, format="full").execute()

    print ('Message snippet: %s' % message['snippet'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

# def insertDB(db_name, values):
#     print ('Inserting into database ' + db_name + '...')	
#     conn = sqlite3.connect(db_name)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS people
#                  (text text, description text, link text,
#                                UNIQUE(text))''')

#     c.executemany('INSERT OR IGNORE INTO people VALUES (?, ?, ?)', values)

#     conn.commit()
#     conn.close()

def initializeDB(db_name):
	print ('Initializing database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS people(firstName text, lastName text, type text, email text, UNIQUE(firstName, lastName))")
	conn.close()

def insertDB(db_name, firstName, lastName):
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

def readDB(db_name):
	print ('Reading from database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	for row in c.execute("SELECT firstName, lastName FROM people"):
		print (row)
	conn.close()

def readDB(db_name, firstName):
	print ('Reading ' + firstName + ' from database ' + db_name + '...')
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("SELECT * FROM people WHERE firstName =?", [firstName])
	print (c.fetchall())
	conn.close()

def readEmail(db_name, firstName):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("SELECT email FROM people WHERE firstName =?", [firstName])
	print (c.fetchall())
	#if multiple, specify ask which one
	conn.close()

def addEmail(db_name, firstName, email):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.executemany("UPDATE people SET email=? WHERE firstName=?", [(email, firstName)])
	# c.executemany("INSERT INTO people (email) VALUES ? WHERE firstName = ?", [email, firstName])
	if (c.rowcount != 0):
		print ('Successfully added ' + email + ' to ' + firstName)
	else:
		print ('Failed to add ' + email + ' ' + firstName)()

		#add already exists if statement error message
	conn.commit()
	conn.close()

class _DeHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.__text = []

	def handle_data(self, data):
		text = data.strip()
		if len(text) > 0:
			text = sub('[ \t\r\n]+', ' ', text)
			self.__text.append(text + ' ')

	def handle_starttag(self, tag, attrs):
		if tag == 'p':
			self.__text.append('\n\n')
		elif tag == 'br':
			self.__text.append('\n')

	def handle_startendtag(self, tag, attrs):
		if tag == 'br':
			self.__text.append('\n\n')

	def text(self):
		return ''.join(self.__text).strip()


def dehtml(text):
	try:
		parser = _DeHTMLParser()
		parser.feed(text)
		parser.close()
		return parser.text()
	except:
		print_exc(file=stderr)
		return text

def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	pass

def main():
	initializeDB('kotodb')
	insertDB('kotodb', 'Yana', 'Yudelevich')
	readDB('kotodb', 'Yana')
	addEmail('kotodb', 'Yana', 'yanapost@gmail.com')
	readDB('kotodb', 'Yana')
	readEmail('kotodb', 'Yana')

	# credentials = get_credentials()
	# http = credentials.authorize(httplib2.Http())
	# service = discovery.build('gmail', 'v1', http=http)

	# msgs = ListMessagesMatchingQuery(service, "me", name)

	# print(msgs[30]['id'])
	# encryptedMsg = GetMessage(service, "me", msgs[15]['id'])['payload']['parts'][1]['body']['data']
	# deencryptedMsg = base64.urlsafe_b64decode(encryptedMsg.encode('UTF-8'))
	# deHTMLmsg = dehtml(deencryptedMsg)

	# print(deHTMLmsg)

if __name__ == '__main__':
	main()


#template code:
	#for each investor in a list:
		#when is the last time we talked?
		#snippet of last conversation
		#num. of total conversations

