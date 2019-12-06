from time import sleep


class CommandUi:
    def __init__(self):
        self.page = "main"
        self.commands = {
        "welcome": self.welcome, "help": self.help,
        "url": self.get_url, "depth of crawl": self.get_depth,
        "current page": self.page, "basic auth": self.basic_auth,
        #"allowed urls": self.allowed_urls,
        }
        self._help = {
        "help": "type help to get explanation for each command",
        "url": """
type url to enter url that you want to crawl,
if the url is http please enter the full url scheme like:http://example.com
else you can just enter the domain like: example.com""",
"basic auth": """
please enter basic auth id and password if is needed,
please sepreate id and password with a coma
like this: myid,mypassword,
please dont put spaces
if no basic auth is needed you can skip by pressing return""",
        "get depth of crawl": """
please enter the depth of crawl,
the defualt is to crawl the whole site
the depth indicates how many url to follow if you
want only to check one page type 0,
if you want 1 page and just urls inside this page type 2""",
        "exit": "to exit type exit"
        }
        self.welcome()

    def welcome(self):
        print("""
============================================================
                        Welcome to Crawler
============================================================
This app is made for and by plate company,
please contact plate.co.jp for more information
This is Crawler.Alfa.1.0
new updates may or may not be available.

to plate members:
if you need any help with the app
or you want new features
or easier and prettier command line please contact arashi
for more help with commands type help
============================================================
                        have a nice crawling
============================================================
        """)
        sleep(0.7)

    def help(self):
        for key in self._help:
            print(f"""\t{key}:
{self._help[key]}
======================================================""")
            print("\n")

    def get_url(self):
        print("\t", self._help["url"], "\n")
        url = input("please enter desired url: ")
        url = "".join(url.split())
        if not url.startswith("http"):
            if url.startswith("www"):
                url = url.replace("www.", "")
                url = "https://" + url
            else:
                url = "https://" + url
        if not url.endswith("/"):
            url = url + "/"
        return url

    def get_depth(self):
        print(self._help["get depth of crawl"], "\n")
        depth = input("please enter desired depth: ")
        if depth == "":
            depth = -1
        try:
            depth = int(depth)
        except Exception as e:
            print(e)
        if type(depth) is int:
            return depth
        else:
            print("wrong value")
            self.get_depth()

    def basic_auth(self):
        print(self._help["basic auth"], "\n")
        auth = input("enter id and password: ")
        if auth:
            auth = auth.split(',')
            if len(auth) is 2:
                auth_id, auth_pass = auth[0], auth[1]
                return auth_id, auth_pass
            else:
                print("wrong input")
                self.basic_auth()
        else:
            return


    def manager(self, command):
        if command in self.commands:
            return self.commands[command]()
        else:
            print("wrong command")
            self.manager(command)

    def crawl_page(self):
        url = self.manager("url")
        depth = self.manager("depth of crawl")
        basic_auth = self.manager("basic auth")
        #allowed_urls = self.manager("allowed urls")
        return url, depth, basic_auth

    def curation_page(self):
        url = self.manager("url")
        depth = self.manager("depth of crawl")
        basic_auth = self.manager("basic auth")
        return url, depth, basic_auth

    def start_page(self, page):
        if page == "crawl":
            return self.crawl_page()
        elif page == "curation":
            return self.curation_page()
