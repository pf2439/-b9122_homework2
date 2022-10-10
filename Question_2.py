#Question 2, Peiran Fu
from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"
seed_url_path = "https://www.sec.gov/news/press-release/"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
found = []           #stack of url with the word "charges"
texts = []           #contains text of the page

maxNumUrl = 20; #set the maximum number of urls to visit
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
        #checks for the searchword & store url + the article body
        if(webpage_text.find("charges") != -1):
          found.append(curr_url)
          soup = BeautifulSoup(webpage, 'html.parser')
          text = soup.find("div", {"class":"article-body"})
          texts.append(text)

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
print("List of URLs containing the word \"charges\":")
for found_url, found_text in zip(found, texts):
    print("URL: " + str(found_url))
    print("Text: " + str(found_text) + "\n\n")