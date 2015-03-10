#Byron Post Poetry
###################

#imports
import re
import pytumblr
import random
import requests
from lxml import html

#thanks stack-o
def remove_html(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out

def main():
	print "Connecting to Tumblr..."

	# Authenticate via OAuth
	client = pytumblr.TumblrRestClient(#auth info
	)

	# Make the request
	client.info()

	#load posts into RAM
	file = open("lines.txt", "r")
	posts = {}

	print "Loading file..."

	for l in file:
		l = l.strip("\n")
		lastWord = l.split(" ")
		lastWord = lastWord[len(lastWord)-1]
		#freaking regexs
		lastWord = re.sub(r'[^a-zA-Z]','', lastWord.lower())
		
		if lastWord in posts:
			posts[lastWord].append(l)
		else:
			posts[lastWord] = [l]

	#How many poems are you prepared to queue
	numOfPoems = int(raw_input("How many poems do you want to generate? "))

	#gimme all the keys in posts
	keys = posts.keys()

	poemTitle =  ""
	poem = ""
	length = -1

	#and now we build our poems!
	for i in range(0,numOfPoems):

		keysCopy = keys
		
		poemTitle =  ""
		poem = ""
		length = -1

		#make sure the poem isn't awful. we have standards.
		while poem == "" and poemTitle == "" and length <= 2:
			#so we can delete keys we've used
			keysCopy = keys
			
			poemTitle =  ""
			poem = ""
			
			#ABAB rhyme scheme
			#keep track of the last word in the scheme
			a = random.choice(keysCopy)
			b = random.choice(keysCopy)
			while a == b:
				b = random.choice(keysCopy)
				
			#the first two lines in the poem are random
			#handling for if two lines end in the same word
			poem += random.choice(posts[a]) + "\n"
			keysCopy.remove(a)
			poem += random.choice(posts[b]) + "\n"
			keysCopy.remove(b)
			
			#give us a random number of lines between 5 and 10
			for x in range(2, random.randint(4,6)):
				
				#get me the last word of the previous line
				if x % 2 == 0:
					lastWord = a
				else:
					lastWord = b
				
				#get rhymes
				url = "http://rhymezone.com/r/rhyme.cgi?Word=" + lastWord + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y"
				r = requests.get(url)
				rhymes = remove_html(r.text)
				rhymes = rhymes.split("syllables:")
				for list in rhymes:
					if list 
					rhymes[1]
				
				#search for rhymes
				for word in keysCopy:
					if word + "," in rhymes[1] and word != lastWord:
						if x % 2 == 0:
								a = word
								poem += random.choice(posts[a]) + "\n"
								keysCopy.remove(a)
						else:
								b = word
								poem += random.choice(posts[b]) + "\n"
								keysCopy.remove(b)
					else:
						continue
			
			#generate the poem title based on whatever posts got put in said poem
			poemCopy = poem.replace("\n", " ")
			poemCopy = poemCopy.split(" ")
			for x in range(0, random.randint(1,4)):
				poemTitle +=  re.sub(r'[^a-zA-Z]','', random.choice(poemCopy)) + " "
				
			poemTitle = poemTitle.title()
			
			length = poem.count('\n')
				
		#print poem
		print poemTitle
		print "-----"
		print poem
		print "-----"
		
		#uncomment this to post to tumblr
		#client.create_text("url", state="queue", tags=[""], title=poemTitle, body=poem)
		
main()