
# parse results scraped using pull_results.py
# output is more convenient dictionary

import json
import pickle
import sys
import random
import time
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from urlparse import urljoin

num_header = ">"
num_end = "</td>"
def parse_num(line):
  s = line.find(num_header) + len(num_header)
  e = line.find(num_end)
  num = line[s:e]
  return num
 
header = '<td valign="top" class="leipateksti" align="left" bgcolor="#E6E6E6">'
end = '</td>'
def parse_page(page):
  i = 0
  lines = page.split("\n")
  d = {}
  while i < len(lines):
    line = lines[i]
    if line.find(header) != -1:
      begpos = line.find(header) + len(header)
      endpos = line.find(end)
      name = line[begpos:endpos]
      name = unicode(name,encoding="iso8859_10",errors="replace")
      if name[0] == "M" or name[0] == "<":
        i = i+1
        continue
      l = [parse_num(lines[i+j]) for j in range(1,7)]
      assert len(l) == 6
      #print name, l
      d[name.encode("utf8")] = l[4]
      i = i+6
    i = i+1
  assert len(d) == 8
  return d

def parse_pages(d):
  dd = {}
  for alue in d:
    print "processing", alue
    page = d[alue]
    dd[alue] = parse_page(page)
  return dd

def usage():
  print "transforms scraped election results to more convenient dictionary"
  print "%s matched_pages.pickle parsed_results.pickle" %sys.argv[0]

def parse_cp():
  if len(sys.argv) != 3:
    usage()
    sys.exit(-1)
  return (sys.argv[1],sys.argv[2])

def main():
  (infn,outfn) = parse_cp()
  (d,dd) = pickle.load(open(infn))
  f = open(outfn,"w")
  pages = parse_pages(dd)
  pickle.dump(pages,f)
  f.close()

if __name__ == "__main__":
  main()

