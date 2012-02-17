
#Tested on Python 2.6.6.
#Scrapes Finnish election results from official "tulos" palvelu

import json
import pickle
import sys
import random
import time
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urljoin

rate_limit = 50 #this many accesses per second
access_time = 0
tries = 0
def check_rate_limit():
  """
  Limit requests to web service
  """
  global access_time
  global tries 
  t = int(time.time())
  if access_time != t:
    access_time = t
    tries = 0
  else:
    tries += 1
    if tries > rate_limit:
      print "API rate limit reached, waiting 1 sec..."
      time.sleep(1.1)
      tries = 0

max_api_tries = 5 # try at most 5 times 
def geturl(url):
  """
  Fetch URL content
  """
  tries = 0
  while 1:
    try:
      check_rate_limit()
      request = urllib2.Request(url)
      response = urllib2.urlopen(request)
      return response
    except:
      tries +=1
      if tries > max_api_tries:
        raise
      print "API fail: (%s)" %sys.exc_info()[0]
      return None

def find_links(url):
  """
  Find all links at given URL
  """
  l = []
  for link in BeautifulSoup(geturl(url), parseOnlyThese=SoupStrainer('a')):
    if link.has_key('href') and link['href']:
      l.append( link['href'] )
  return l

def find_pages(url):
  """
  Parse result pages from tulos -service
  """
  links = find_links(url)
  print "found", len(links), "links total"
  links = [urljoin(url,x) for x in links if x.find("ku") == 0]
  print "found", len(links), "links for kunnat"
  print "first kunta link:", links[0]
  d = {}
  for link in links:
    alue_links = find_links(link)
    alue_links = [urljoin(link,x) for x in alue_links if x.find("aluetulos") == 0]
    d[link] = alue_links
    print "found", len(alue_links), "links for kunta ", link
  dd = {}
  for kunta in d:
    for alue in d[kunta]:
      response = geturl(alue).read()
      dd[alue] = response
      print "got page ", alue
  return (d,dd)

def usage():
  print "%s base_URL matched_pages.pickle" %sys.argv[0]
  print "example: %s http://192.49.229.35/TP2012K1/s/tulos/lasktila.html matched_pages.pickle" %sys.argv[0]

def parse_cp():
  if len(sys.argv) != 3:
    usage()
    sys.exit(-1)
  return (sys.argv[1],sys.argv[2])

def main():
  (url,outfn) = parse_cp()
  f = open(outfn,"w")
  pages = find_pages(url)
  pickle.dump(pages,f)
  f.close()

if __name__ == "__main__":
  main()

