#!/usr/bin/env python3
import requests, bs4, sys

if len(sys.argv) < 1:
    quit()

page = requests.get("http://www.greek-language.gr/greekLang/modern_greek/tools/lexica/georgakas/search.html?lq=%s" % sys.argv[1])

try:
    page.raise_for_status()
except Exception as e:
    print('There was a problem: %s' % (e))

pageSoup = bs4.BeautifulSoup(page.content, "lxml")

elems = pageSoup.select('#lemmas dt')

print(elems[0].getText())

