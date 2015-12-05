#koto - communication tracking utiliity
#created by ben shukman

#each name has attributes: last date contacted, each contact is a commit (so its a unique data struct)

#store JSON / class of data

#import list of names
#if recent email, display in high priority
#if name is under X days old, needs love

'''

template = ['jon', 'murloc', 'morty']
personList = []
count = 0

class person:
	def __init__(self):
		self.firstName = None
		self.lastName = None
		self.numOfCommits = 0
		self.lastContact = None
	#personType = friend
	#make friend into a class?
	#firstName
	#lastName
	#numOfCommits
	#lastContact
	#type - friend, associate, investor, coworker (make these into classes?)

godzilla = person()
woz = person()
belka = person()

testList = [godzilla, woz, belka]
# testList.append(godzilla)

godzilla.firstName = "godzilla"
godzilla.lastContact = 4

# initialization:
for x in template:
	# print x
	x = person()
	x.firstName = str(x)
	# print x.firstName
	x.lastContact = count
	count += 1
	personList.append(x)

# print personList[0]

# if 'koto status':
for z in testList:
	#make each unit in the list a person class
	print str(z.firstName) + '\n' + '- days since last communication: ' + str(z.lastContact) + '\n'

for z in personList:
	print str(z.firstName) + '\n' + '- days since last communication: ' + str(z.lastContact) + '\n'

class commit:
	pass
	#id = idGen(name, date)
	#date
	#type - email, text, phone, fb, meeting
	#subject
	#body

'''

#make preferences tab

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

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
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

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

def main():
	#fetch google account credentials
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)



def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	pass

if __name__ == '__main__':
    main()