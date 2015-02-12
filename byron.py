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
client = pytumblr.TumblrRestClient(#nope
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

poemTitle =  ""
poem = ""
len = -1

#and now we build our poems!
for i in range(0,numOfPoems):

	keysCopy = keys
	
	poemTitle =  ""
	poem = ""
	len = -1

	while poem == "" and poemTitle == "" and len <= 2:
		#so we can delete keys we've used
		keysCopy = keys
		
		poemTitle =  ""
		poem = ""
		
		#right now I'm just doing ABAB rhyme scheme
		#keep track of the last word in the scheme
		a = random.choice(keysCopy)
		b = random.choice(keysCopy)
		while a == b:
			b = random.choice(keysCopy)
			
		#the first two lines in the poem are random
		#handling for if two lines end in the same word
		poem += random.choice(shitposts.pop(a, [""])) + "\n"
		poem += random.choice(shitposts.pop(b, [""])) + "\n"
		
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
					if entry["score"] >= 250 and entry["word"] != lastWord:
							if x % 2 == 0:
								a = entry["word"]
								poem += random.choice(shitposts[a]) + "\n"
								keysCopy.remove(a)
							else:
								b = entry["word"]
								poem += random.choice(shitposts[b]) + "\n"
								keysCopy.remove(b)
					else:
						break
				else:
					poem += ""
		
		poem = poem.strip("\n")
		
		#generate the poem title based on whatever shit posts got put in said poem
		poemCopy = poem.replace("\n", " ")
		poemCopy = poemCopy.split(" ")
		for x in range(0, random.randint(1,4)):
			poemTitle += random.choice(poemCopy) + " "
			
		poemTitle = poemTitle.title()
		
		#LET'S PUT THIS POEM ON TUMBLR
		len = poem.count('\n')
		if poem != "" and poemTitle != "" and len > 2:
			break
			
	#make sure the poem isn't awful. we have standards.
	#show me the shit
	print poemTitle
	print "-----"
	print poem
	print "-----"
	
	#client.create_text("shitpostpoetry", state="queue", tags=[""], title=poemTitle, body=poem)