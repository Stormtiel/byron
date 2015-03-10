#Populate Byron Module
#Takes the newest posts from the #post tag and loads them into lines.txt
###################

import pytumblr

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
  'veXTmnXDd7jmPZ5fdILVATJU200LWAr9UjbPbeJwzwxoO1Gcub',
  'rs6hs2y1HCszVb88nszvKUes9tAFnJwJ3IJUJrvQ9RjDCBjrTI',
  'bMARTVAHGQlToaFJuLMf9MEFbYwWc6w7sNsMf5L50jWM4cZBGS',
  'TjYVpKbn6S8ZQHt54WDtQ14qAM4UINbuxA07T8OkCQg3ofEyQk'
)

# Make the request
client.info()

#Get posts
posts = client.tagged('post')
file = open("lines.txt", "a")

#Process posts
for i in posts:
	if i["type"] == "text":
		
		if i["body"]:
			#ignore posts with replies or images.... I don't feel like writing something to parse them
			if "said:" in i["body"] or "wrote:" in i["body"] or "<img" in i["body"]:
				pass
			else:
				l = i["body"]
				l = l = l.replace(u'\n',' ')
				l = l.replace('<p>','')
				l = l.replace('</p>','\n')
				l = l.replace('<br/>','')
				print l.encode('utf-8','ignore')
				print "-----"
				if l == "":
					pass
				else: 
					file.write(l.encode('utf-8', 'ignore'))
		if i["title"]:
			if ">>" in i["title"]:
				pass
			else:
				l = i["title"].replace(u'<p>',u'')
				l = i["title"].replace(u'</p>',u'')
				i["title"].replace(u'<br>',u'')
				file.write((i["title"]).encode('utf-8','ignore') + "\n")