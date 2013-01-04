#Crawler Code

import sys
import urllib2
from urlparse import urlparse

#Global variables
crawledurls = []       			 	 #List of urls already crawled 
urls = []           				 #List of urls - all these urls be added to final repo and we will be crawling many of these urls
reposize = 50         			 	 #Default size of url repo
noofurls = 0;         			 	 #Number of urls
seedurl = " http://haricm.in/" 	     #Default seed url

#Get page fom web and return it as a string
def get_page(url)	:
	try : 
		sock = urllib2.urlopen(url)
	except IOError, (errno):
		return "error"
	html = sock.read()
	sock.close()
	return html

# Parses the html string and returns a list of urls
def get_urls(crawlingurl, html):
	listofurls = []
	global noofurls
	global reposize
	global crawledurls
	global urls
	length = len(html)
	index = 0
	crawlingurl = crawlingurl.strip()
	#Formating crawlingurl 
	if crawlingurl.endswith('/'):
			crawlingurl = crawlingurl[:len(crawlingurl) -1]
	parsedurl = urlparse(crawlingurl)
	crawlingurl = parsedurl.scheme + "://" + parsedurl.netloc
	#Scan till the end of html response. Stop scanning once we collect enough urls
	while ((index < length) and (noofurls < reposize)):
		nexthrefindex = html.find("href",index)
		if nexthrefindex == -1:                        #No more links
			return listofurls
		startingindex = html.find('"',nexthrefindex)
		if startingindex == -1:                        #Exception
			return listofurls
		endingindex = html.find('"',startingindex + 1)
		if endingindex == -1:                          #Exception
			return listofurls
		
		url = html[startingindex + 1:endingindex]
		#Format url
		url = url.strip()
		if url.startswith('//'):
			url = parsedurl.scheme + ":" + url
		if url.startswith('/'):
				url = crawlingurl  + url
				
		#Update noofurls and listofurls
		if url not in crawledurls and url not in listofurls  and url not in urls:
			noofurls = noofurls + 1
			listofurls.append(url)
		index = nexthrefindex + 1
	return listofurls

#Maining Crawling Function which returns a list of urls
def crawl(seedurl):
	global urls
	
	#Check 
	response = str(get_page(seedurl))
	if response == "error" :
		print "Wrong URL or No Internet Connection."
		return
	
	#initialize urls with seedurl
	urls = [seedurl]
	
	while ((urls!=[]) and (noofurls < reposize)) :
		url = urls.pop(0)          #Instead of pop(), pop(0) used so that it crawls like a BFS algorithm
		crawledurls.append(url)
		response = str(get_page(url))
		if response != 'error' :
			urls.extend(get_urls(url,response))
			
#Command line
if len(sys.argv) == 2:
	seedurl = sys.argv[1]
elif len(sys.argv) == 3:
	seedurl = sys.argv[1]
	try:
		reposize = int(sys.argv[2])
	except exceptions.ValueError:
		print "You have entered wrong value for reposize, so we are proceeding with default value"
elif len(sys.argv) > 3:
	print "Syntax error"
	sys.exit(2)
	
#calling main function
crawl(seedurl)
urls.extend(crawledurls)

#
for url in urls:
	print url
