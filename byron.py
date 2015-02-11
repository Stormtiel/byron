#Byron Shitpost Poetry
###################

#imports
import re
import pytumblr
import random
import json
import requests

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

	poemTitle =  ""
	poem = ""
	
	#right now I'm just doing ABAB rhyme scheme
	#keep track of the last word in the scheme
	a = random.choice(keys)
	b = random.choice(keys)
	while a == b:
		b = shitposts.keys()
		
	#the first two lines in the poem are random
	#handling for if two lines end in the same word
	poem += random.choice(shitposts[a]) + "\n"
	poem += random.choice(shitposts[b]) + "\n"
	
	#give us a random number of lines between 5 and 10
	for x in range(2, random.randint(4,6)):
	
		print x
		
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
			print lastWord
			print entry["word"]
			
			if entry["word"] in keys:
				if entry["word"] != lastWord:
					if x % 2 == 0:
						a = entry["word"]
						poem += random.choice(shitposts[b]) + "\n"
					else:
						b = entry["word"]
						poem += random.choice(shitposts[a]) + "\n"
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
	
	#client.create_text("shitpostpoetry", state="queue", tags=["shitpost"], title=poemTitle, body=poem)