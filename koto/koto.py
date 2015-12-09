#koto - communication tracking utiliity
#created by ben shukman

#each name has attributes: last date contacted, each contact is a commit (so its a unique data struct)

#store JSON / class of data

#import list of names
#if recent email, display in high priority
#if name is under X days old, needs love

import db_methods, gmail_methods

g = gmail_methods
db = db_methods
db_name = 'kotodb'

def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	pass

def main():
	db.initializeDB()
	db.insertDB('Ben', 'Shukman')
	db.readDB('Ben')
	db.addEmail('Ben', 'bananas4ben@gmail.com')
	db.readDB('Ben')

	for row in db.readEmail('Ben'):
		query = row

	print (query)

	credentials = g.get_credentials()
	http = credentials.authorize(g.httplib2.Http())
	service = g.discovery.build('gmail', 'v1', http=http)

	msgs = g.ListMessagesMatchingQuery(service, "me", query)

	# print (msgs)

	# print(msgs[0]['id'])
	message = g.GetMessage(service, "me", msgs[3]['id'])

	# parsedMsg = encryptedMsg.parts.filter(function(parsedMsg)
	# 	return part.mimeType == 'text/html')

	# var part = message.parts.filter(function(part) {
	# 	return part.mimeType == 'text/html';
	# 	});
	# var html = urlSafeBase64Decode(part.body.data);


	#['payload']['parts'][1]['body']['data']
	# deencryptedMsg = base64.urlsafe_b64decode(encryptedMsg.encode('UTF-8'))
	# deHTMLmsg = dehtml(deencryptedMsg)

	# print(encryptedMsg)

	#<<

	msg_str = g.base64.urlsafe_b64decode(message['raw'].encode('UTF-8'))
	msg = g.email.message_from_string(msg_str)

	# print (msg)

	#this works!!
	for part in msg.walk():
		msg.get_payload()
		if part.get_content_type() == 'text/plain':
			# mytext = base64.urlsafe_b64decode(part.get_payload().encode('UTF-8'))
			mytext = part.get_payload()
			# print part.get_payload()
			print (mytext)
	#>>
	
if __name__ == '__main__':
	main()


#template code:
	#for each investor in a list:
		#when is the last time we talked?
		#snippet of last conversation
		#num. of total conversations

