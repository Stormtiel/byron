#Byron Post Poetry
###################

#imports
import re
import pytumblr
import random
import requests
import urllib2
import bs4

def getRhymes(word):

	#open the webpage and process it
	url = urllib2.urlopen("http://rhymezone.com/r/rhyme.cgi?Word=" + word + "&typeofrhyme=perfect&org1=syl&org2=l&org3=y")
	page = bs4.BeautifulSoup(url).get_text()

	#if we didn't have any perfect rhymes, end the poem
	if 'Words and phrases that rhyme with' not in page:
		return []

	#filter out just the part that has the rhymes
	page = (page.split("Words and phrases that rhyme with"))[1].split("var")[0]
	page = re.sub(r'syllables|results|syllable| ' + word + ' ', ',', page)
	page = page.split(",")
	rhymes = []

	for word in page:
			word = re.sub(r'[^a-zA-Z-\']',' ', word).strip()
			if word != '':
				rhymes.append(word)

	return rhymes

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

	#each line is stored in a dictionary, as a list, with the last word as its key
	#if there are lines sharing the same last word, then it's appended to the list
	for l in file:
		l = l.strip("\n")
		lastWord = l.split(" ")
		lastWord = lastWord[len(lastWord)-1]
		lastWord = re.sub(r'[^a-zA-Z]','', lastWord.lower())

		if lastWord in posts:
			posts[lastWord].append(l)
		else:
			posts[lastWord] = [l]

	#How many poems are you prepared to queue
	numOfPoems = int(raw_input("How many poems do you want to generate? "))

	#get all the keys in posts
	keys = posts.keys()

	#default values
	poemTitle =  ""
	poem = ""
	length = -1

	#and now we build our poems!
	for i in range(0,numOfPoems):

		keysCopy = keys

		poemTitle =  ""
		poem = ""
		length = -1

		#make sure the poem isn't too short
		while length <= 1:
			#so we can delete keys we've used
			keysCopy = keys

			#reset values
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
			poem += random.choice(posts[a]) 
			keysCopy.remove(a)
			poem += "\n" + random.choice(posts[b])
			keysCopy.remove(b)

			#give us a random number of lines between 6 and 8
			for x in range(2, random.randint(4,6)):

				#get me the last word of the previous line
				if x % 2 == 0:
					lastWord = a
				else:
					lastWord = b

				rhymes = getRhymes(lastWord)
			
				#for each word in the list of rhymes...
				for word in rhymes:
						#for each key in the list of keys...
						for key in keysCopy:
							#check if the word is equal to any of the keys, and make sure that we're not repeating words
							if key == word and word != lastWord:
								#if this is an even line
								if x % 2 == 0:
										a = word
										line = random.choice(posts[a])
										print line
										poem += "\n" + line
										keysCopy.remove(a)
								#if this is an odd line
								else:
										b = word
										line = random.choice(posts[b])
										print line
										poem += "\n" + line
										keysCopy.remove(b)
			
			#generate the poem title based on whatever posts got put in said poem
			poemCopy = poem.replace("\n", " ")
			poemCopy = poemCopy.split(" ")
			for x in range(0, random.randint(1,4)):
				choice = re.sub(r'[^a-zA-Z]','', random.choice(poemCopy))
				if choice not in poemTitle:
					poemTitle += choice + " "

			poemTitle = poemTitle.title()

			length = poem.count('\n')
			if length <= 1:
				print "Poem under 2 lines. Trying again..."

		#print poem
		print poemTitle
		print "-----"
		print poem
		print "-----"
		
		q = ''
		
		#do we want to post this to tumblr?
		while q != 'yes' and q != 'no':
			q = raw_input("Post to tumblr? (yes/no) ")
			if q == 'yes':
				q = raw_input("Queue post? (yes/no) ")
				if q == 'yes':
					client.create_text("postpoetrybot", state="queue", tags=[""], title=poemTitle, body=poem)
				if q == 'no':
					client.create_text("postpoetrybot", state="published", tags=[""], title=poemTitle, body=poem)

main()