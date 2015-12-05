#koto - communication tracking utiliity
#created by ben shukman

#each name has attributes: last date contacted, each contact is a commit (so its a unique data struct)

#store JSON / class of data

#import list of names
#if recent email, display in high priority
#if name is under X days old, needs love

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

def idGen(name, date):
	#generate id name such as 8839GODZILLA040494
	y = "hey"

#make preferences tab