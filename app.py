from spider import Spider
from filemanager import FileManager
import pandas as pd
import json


class App:
    def __init__(self, url, depth=-1, basic_auth="", allowed_urls=[]):
        self.spider = Spider(url, depth=depth, basic_auth=basic_auth, allowed_urls=allowed_urls)
        self.filemanager = FileManager()
        self.shown_urls = []

    def run(self):
        try:
            self.spider.start()
        except Exception as e:
            self.filemanager.save_to_log(e)
            return
        data = {"visited":list(self.spider.general_visited), "unvisited":list(self.spider.general_unvisited)}
        self.filemanager.save_to_json(data)

        return

    def stop(self):
        self.spider.crawl = False

    def get_csv_table(self):
        return self.spider.csv_table.get_table(), self.spider.csv_table.column

    def remaining(self):
        print(f"number of urls found: {len(self.spider.general_unvisited)}")
        print(f"number of urls fetched: {len(self.spider.general_visited)}")

    def retrive_lost_urls(self):
        self.spider.general_visited = self.spider.general_visited - self.spider.lost_url
        self.spider.csv_table.remove_table()
        return

    def has_lost_url(self):
        if self.spider.lost_url:
            return True
        else:
            return False

    def show_lost_urls(self):
        return self.spider.lost_url

    def get_urls_to_show(self):
        urls_to_show = {}
        for url in self.spider.visited:
            if url not in self.shown_urls:
                urls_to_show[url] = self.spider.visited[url]
                self.shown_urls.append(url)
        return urls_to_show
