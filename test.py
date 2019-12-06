import requests
from bs4 import BeautifulSoup
from htmlparser import HtmlParser
from urlparser import UrlParser
from time import sleep
import codecs
import json
import pandas as pd

visited = set()
unvisited = set()
domain = 'www.motoji.co.jp'
siteUrl = f"https://{domain}/"
praser_url = UrlParser(siteUrl)
parser_html = HtmlParser()
DATA = []

def get_res(url):

    headers_pc = {'User-Agent': 'robot wpmake'}
    try:
        res = requests.get(url, headers=headers_pc, timeout=5.0, allow_redirects=False)
        return res
    except requests.exceptions.RequestException as e:
        print(e)
        return False

def update_data(url, status_code):

    DATA.append({"url": url, "status_code": status_code})

def remove_lead_and_trail_slash(s):
    if s.startswith('/'):
        s = s[1:]
    if s.endswith('.jpg/') or s.endswith('.png/'):
        s = s[:-1]
    return s

def crawl(url, unvisited, visited):
    response = get_res(url)
    if not response:
        update_data(url, 301)
        update_data(response.url, response.status_code)
        return
    if response.status_code > 200:
        update_data(response.url, response.status_code)

    html = BeautifulSoup(response.content, "lxml")
    if not html:
        return

    urls = parser_html.get_url(html, siteUrl)
    unvisited.update(urls - visited)


crawl(siteUrl, unvisited, visited)

while unvisited:
    sleep(0.1)
    url = unvisited.pop()
    url = remove_lead_and_trail_slash(url)
    if url in visited:
        continue
    print(url)
    crawl(url, unvisited, visited)
    visited.add(url)

    df = pd.DataFrame(DATA)
    df.to_excel('output.xlsx')

print(len(visited))

sorted_keys = sorted(DATA.keys())
sorted_DATA = {}
for sorted_key in sorted_keys:
    sorted_DATA[sorted_key] = DATA[sorted_key]

with codecs.open('/Users/bahrami-a/Desktop/seotool/production_source/your_filepc.json', 'w', encoding='utf-8') as f:
   json.dump(sorted_DATA, f, ensure_ascii=False)
