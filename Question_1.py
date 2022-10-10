#Question 1, Peiran Fu HELLO THIS IS A CHANGE MADE BY PEIRAN
from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
seed_url_path = "https://www.federalreserve.gov/newsevents/pressreleases/"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
found = []           #stack of url with the word "covid"

maxNumUrl = 10; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(found) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        print("num. of URLs in stack: %d " % len(urls))
        print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        webpage_text = webpage.decode("utf-8").lower()
        opened.append(curr_url)
        #checks for the searchword & store url
        if(webpage_text.find("covid") != -1):
          found.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if seed_url_path in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("List of URLs containing the word \"covid\":")
for found_url in found:
    print(found_url)