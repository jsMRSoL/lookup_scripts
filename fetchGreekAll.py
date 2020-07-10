#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import sys
from bs4 import BeautifulSoup as bs


def make_soup(greek):
    BASE_URL = 'http://www.perseus.tufts.edu/hopper/text?doc='\
        + 'Perseus%3Atext%3A1999.04.0057%3Aentry%3D'
    greek = re.sub('/', '%2F', greek)
    page = requests.get(BASE_URL + greek)
    try:
        page.raise_for_status()
    except Exception as e:
        print('There was a problem: %s' % (e))
        quit()
    pageSoup = bs(page.text, 'html.parser')
    if len(pageSoup.findAll(text=re.compile("We're sorry"))) == 0:
        return pageSoup
    else:
        return -1


def fetch_entry(soup):
    elems = soup.select('#text_main .text span.greek')
    if len(elems) == 0:
        print('Unable to extract text from page.')
    else:
        output = ', '.join([item.getText() for item in elems[0:3]])
        # regex = re.compile(r"(.*?)[v|\n|\.|I|\(].*")
        output = re.sub(' ,', ',', output)
        output = re.sub(',$', '', output.strip())
        output = re.sub(';$', '', output.strip())
        return output


def fetch_meaning(soup):
    elems = soup.select('#text_main .text i')
    if len(elems) == 0:
        print('Unable to get meanings.')
        return 'Meanings unavailable'
    else:
        meanings = [item.getText() for item in elems if not item.getText()[
            0].isupper() if item.getText()[0].isalpha()]
        meanings = [re.sub(',$', '', item) for item in meanings[0:3]]
        meanings = [re.sub(';$', '', item) for item in meanings]
        output = ', '.join(meanings)
        return output


def main(greek):
    soup = make_soup(greek)
    if soup == -1:
        return 'No definition was found for ' + greek
    else:
        entry = fetch_entry(soup)

    meanings = fetch_meaning(soup)

    return entry + ': ' + meanings


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("No argument given.")
    else:
        for item in sys.argv[1:]:
            print(main(item))
