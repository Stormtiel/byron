#Byron Shitpost Poetry
###################

#imports
import re
import pytumblr
import random
import json
import requests

print "Connecting to Tumblr..."

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'veXTmnXDd7jmPZ5fdILVATJU200LWAr9UjbPbeJwzwxoO1Gcub',
  'rs6hs2y1HCszVb88nszvKUes9tAFnJwJ3IJUJrvQ9RjDCBjrTI',
  'bMARTVAHGQlToaFJuLMf9MEFbYwWc6w7sNsMf5L50jWM4cZBGS',
  'TjYVpKbn6S8ZQHt54WDtQ14qAM4UINbuxA07T8OkCQg3ofEyQk'
)

# Make the request
client.info()

#load shitposts into RAM
file = open("lines.txt", "r")
shitposts = {}

print "Loading file..."

for l in file:
	l = l.strip("\n")
	lastWord = l.split(" ")
	lastWord = lastWord[len(lastWord)-1]
	#freaking regexs
	lastWord = re.sub(r'[^a-zA-Z]','', lastWord.lower())
	
	if lastWord in shitposts:
		shitposts[lastWord].append(l)
	else:
		shitposts[lastWord] = [l]

#How many poems are you prepared to queue
numOfPoems = int(raw_input("How many poems do you want to generate? "))

#gimme all the keys in shitposts
keys = shitposts.keys()

#and now we build our poems!
for i in range(0,numOfPoems):

	#so we can delete keys we've used
	keysCopy = keys
	
	poemTitle =  ""
	poem = ""
	
	#right now I'm just doing ABAB rhyme scheme
	#keep track of the last word in the scheme
	a = random.choice(keysCopy)
	b = random.choice(keysCopy)
	while a == b:
		b = shitposts.keysCopy()
		
	#the first two lines in the poem are random
	#handling for if two lines end in the same word
	poem += random.choice(shitposts.pop(a, None)) + "\n"
	poem += random.choice(shitposts.pop(b, None)) + "\n"
	
	#give us a random number of lines between 5 and 10
	for x in range(2, random.randint(4,6)):
		
		#get me the last word of the previous line
		if x % 2 == 0:
			lastWord = a
		else:
			lastWord = b
		
		#get rhymes
		#thanks rhymebrain! yer great
		url = 'http://rhymebrain.com/talk?function=getRhymes&word=' + lastWord + "&maxResults=20"
		r = requests.get(url)
		j = json.loads(r.text)
		
		#search for rhymes
		for entry in j:
			if entry["word"] in keysCopy:
				if entry["word"] != lastWord:
					if x % 2 == 0:
						a = entry["word"]
						poem += random.choice(shitposts.pop(a, [""])) + "\n"
					else:
						b = entry["word"]
						poem += random.choice(shitposts.pop(b, [""])) + "\n"
			else:
				poem += ""
	
	#generate the poem title based on whatever shit posts got put in said poem
	poemCopy = poem.replace("\n", " ")
	poemCopy = poemCopy.split(" ")
	for x in range(0, random.randint(1,4)):
		poemTitle += random.choice(poemCopy) + " "
		
	poemTitle = poemTitle.title()
	
	#show me the shit
	print poemTitle
	print "-----"
	print poem
	print "-----"
	
	#LET'S PUT THIS POEM ON TUMBLR
	
	if body == "" or title == "":
		pass
	else:
		client.create_text("shitpostpoetry", state="queue", tags=[""], title=poemTitle, body=poem)