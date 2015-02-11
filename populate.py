#Populate Byron Module
#Takes the newest posts from the #shitpost tag and loads them into lines.txt
###################

import pytumblr

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(#nope
)

# Make the request
client.info()

#Get shitposts
shitposts = client.tagged('shitpost')
file = open("lines.txt", "a")

#Process shitposts
for i in shitposts:
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
				print l
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
		
#remove duplicates, in case somebody had the same shitpost or I ran this too much
#thanks stackoverflow

lines = open('lines.txt', 'r').readlines()
precount = sum(1 for l in lines)

lines_set = set(lines)

out  = open('lines.txt', 'w')

for line in lines_set:
    out.write(line)
	
postcount = sum(1 for l in lines)
print "Removed " + (precount - postount) + " line(s)"