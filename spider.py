import requests
from bs4 import BeautifulSoup
import concurrent.futures
from htmlparser import HtmlParser
from urlparser import UrlParser
from time import sleep
from requests.auth import HTTPBasicAuth
from dataformat import CsvFormat
from opentagfinder import OpenTagFinder
from filemanager import FileManager
import os


# spider class gets the url as a string (it can be any url starting with www or // or http https)
class Spider:
    def __init__(self, url, number_of_threads=20, allowed_urls=[], blocked_urls=[], basic_auth=(), depth=-1):
        self.url = url
        self.number_of_threads = number_of_threads
        self.allowed_urls = allowed_urls
        # self.blocked_urls = blocked_urls
        self.lost_url = set()
        self.basic_auth = basic_auth
        self.depth = depth
        self.crawl = True
        self.visited = {}
        self.general_visited = set()
        self.unvisited = set()
        self.general_unvisited = {self.url}
        self.fetched_url_record = dict()
        self.csv_table = CsvFormat(
            [
                "url", "status code", "title", "keyword", "description",
                "h1", "h2", "h3",
                "h4", "h5", "h6",
                "index", "open tags", "external links", "h_tag_format"
            ]
        )
        self.downloaded_pages = {}
        self.record = []
        self.url_parser = UrlParser(url)
        self.parser = HtmlParser()
        self.filemanager = FileManager()

    def start(self):
        self.fetch_html()
        while len(self.general_visited) < len(self.general_unvisited) and self.crawl == True:
            self.fetch_html()

    def fetch_html(self):
        url = self.get_url()
        if url in self.general_visited or not url:
            return
        res = self.get_html(url)
        if res.status_code >= 500:
            self.add_to_visited(url, 500)
            return False
        elif res.status_code >= 400:
            self.save_formated_data(res, url)
            self.add_to_visited(url, 400)
        elif res.status_code >= 300:
            if res.history:
                if self.url_parser.domain not in res.url:
                    return False
        elif res.status_code >= 200:
            self.save_formated_data(res, url)
            self.add_to_visited(url, 200)


    def save_formated_data(self, response, current_url):
        html = BeautifulSoup(response.content, "lxml")
        self.csv_table.create_row('data')
        h_tags = self.parser.get_all_h(html)
        update = {
            "url": current_url,
            "status code": response.status_code,
            "title": self.parser.get_title(html),
            "keyword": self.parser.get_meta_keyword(html),
            "description": self.parser.get_meta_description(html),
            "h1": self.parser.get_htag("h1", h_tags), "h2": self.parser.get_htag("h2", h_tags),
            "h3": self.parser.get_htag("h3", h_tags), "h4": self.parser.get_htag("h4", h_tags),
            "h5": self.parser.get_htag("h5", h_tags), "h6": self.parser.get_htag("h6", h_tags),
            "index": self.parser.get_meta_index(html),
            "open tags": self.find_open_tags(response.text),
            "external links": self.parser.get_broken_a_tags(response.text, self.url_parser.domain, current_url),
            "h_tag_format": self.parser.tag_structure(response.text),
        }
        if response.status_code >= 400:
            update["status code"] = str(update["status code"])
            for fetched_page_url, fetched_url_list in self.fetched_url_record.items():
                if current_url in fetched_url_list:
                    update["status code"] += f" {fetched_page_url}にあります、\n"
        self.csv_table.update_row('data', update)
        self.csv_table.add_row_to_table('data')
        fetched_urls = self.parser.get_url(html, self.url_parser.domain, current_url)
        self.add_to_unvisited(current_url, fetched_urls)

    def get_url(self):
        if not self.unvisited:
            self.unvisited = self.general_unvisited - self.general_visited
            return self.unvisited.pop()

        return self.unvisited.pop()

    def add_to_visited(self, key, *args):
        if key not in self.visited and args:
            self.visited[key] = list(args)
        self.general_visited.add(key)

    def add_to_unvisited(self, url, fetched_urls):
        self.fetched_url_record[url] = fetched_urls
        self.general_unvisited.update(fetched_urls)

    def find_open_tags(self, html):
        open_tag_finder = OpenTagFinder()
        open_tag_finder.feed(html)
        open_tag_finder.reset()
        open_tags = open_tag_finder.get_open_tags()
        return open_tags

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'}
        try:
            if self.basic_auth:
                return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.basic_auth[0], self.basic_auth[1]), timeout=5.0)
            else:
                return requests.get(url, headers=headers, timeout=80.0)
        except requests.exceptions.RequestException as e:
            print(e)
            self.filemanager.save_to_log(f"{e} in url {url}")
            return
