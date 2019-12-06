import requests
from bs4 import BeautifulSoup
from urlparser import UrlParser
from dataformat import CsvFormat
from filemanager import FileManager
import re


# spider class gets the url as a string (it can be any url starting with www or // or http https)
class HtmlParser:
    def __init__(self):
        self.checked = set()
        self.status_codes = {}
        self.filemanager = FileManager()

    def get_url(self, html, domain):
        url_parser = UrlParser(domain)
        netloc = url_parser.get_netloc(domain)
        urls = set()
        try:
            for bs_object in html.find_all(["a", "img"]):
                raw_url = ""
                if "href" in bs_object.attrs:
                    raw_url = bs_object.attrs["href"]
                elif "src" in bs_object.attrs:
                    raw_url = bs_object.attrs["src"]
                else:
                    continue

                if not url_parser.is_internal(raw_url, url_parser.domain):
                    continue
                if not url_parser.pretty_url(raw_url, url_parser.domain):
                    continue
                if url_parser.pretty_url(raw_url, url_parser.domain).count(netloc) > 1:
                    continue
                if "tel:" in raw_url.lower():
                    continue
                if "mailto:" in raw_url.lower():
                    continue
                url = url_parser.pretty_url(raw_url, url_parser.domain)
                urls.add(url)
        except Exception as e:
            self.filemanager.save_to_log(e)
        return urls

    def get_broken_a_tags(self, html, domain, current_url):
        html_soup = BeautifulSoup(html, "lxml")
        url = UrlParser(domain)
        rel = ""
        urls = ""
        for bs_object in html_soup.find_all("a"):
            if "rel" in bs_object.attrs:
                rel = bs_object["rel"]
            else:
                rel = "rel 属性はありません"
            if not ("href" in bs_object.attrs):
                continue
            line = self.find_line(html, bs_object["href"])
            if url.is_external(bs_object["href"], domain):
                urls = urls + f"{line}行目、 外部 url: {bs_object['href']} rel属性: {rel}" + "\n"
                continue

        return urls

    # return list of strings args html = beautifulsoup object
    def get_all_h(self, html):
        all_h_tags = []
        try:
            for bs_object in html.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                if bs_object.find('img'):
                    img_tag = bs_object.find('img')
                    if img_tag['alt']:
                        bs_object.string = f"画像 alt 属性: {img_tag['alt']}"
                    else:
                        bs_object.string = "画像"
                if bs_object.text:
                    string_format = f"{bs_object.name}: {bs_object.text}"
                    all_h_tags.append(string_format)
        except Exception as e:
            self.filemanager.save_to_log(e)
        return all_h_tags

    # return string args html = beautifulsoup object
    def get_title(self, html):
        title = ""
        if html.title:
            title = html.title.string
        return title

    # return string args html = beautifulsoup object
    def get_meta_keyword(self, html):
        bs_object = html.find('meta', attrs={'name': 'keywords'})
        if bs_object:
            return bs_object["content"]
        else:
            return ""

    # return string args html = beautifulsoup object
    def get_meta_description(self, html):
        bs_object = html.find('meta', attrs={'name': 'description'})
        if bs_object:
            return bs_object["content"]
        else:
            return ""

    # return string args html = beautifulsoup object
    def get_meta_index(self, html):
        index = ""
        if html.find('meta', attrs={'name': 'robots'}):
            index = html.find('meta', attrs={'name': 'robots'})["content"]
        else:
            index = "no index meta tag"
        return index

    def find_line(self, raw_html, tag):
        lines = []
        html_lines = raw_html.split("\n")
        for line in html_lines:
            if "<a" in line:
                if tag in line:
                    lines.append(html_lines.index(line))
                    continue
        return lines

    def remove_tags(self, text, exceptions):
        soup = BeautifulSoup(text, "lxml")
        for tag in soup.find_all(True):
            if tag.name not in exceptions:
                if tag.name == 'img':
                    parent = tag.parent
                    if parent:
                        alt = ""
                        if tag["alt"]:
                            alt = tag["alt"]
                        if parent.name in exceptions:
                            tag.unwrap()
                            parent.string = f"alt 属性: {alt}"
                            continue
                try:
                    tag.unwrap()
                except Exception as e:
                    raise e
        return str(soup)

    def tag_structure(self, raw_html):
        raw_html = raw_html.split("\n")
        h_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
        result = []
        for line in raw_html:
            match = re.search(r"<(main|section|aside|article|\/main|\/section|\/aside|\/article|h\d).*?>", line)
            if match:
                if match.group(1) in h_tags:
                    line = "    " + self.remove_tags(line, h_tags)
                    result.append(line)
                else:
                    splited_tag = match.group(0).split()
                    the_tag = splited_tag[0]
                    result.append(the_tag)
        return "\n".join(result)

    # string
    def get_htag(self, tag, h_tags):
        all_targeted_htags = ""
        for htag in h_tags:
            if htag[:htag.find(":")] == tag:
                all_targeted_htags = all_targeted_htags + htag[htag.find(":")+1:] + "\n"
        return all_targeted_htags

    # string
    def h_tag_format(self, h_tags, parent):
        formating = ""
        for index, htag in enumerate(h_tags):
            htag_number = htag[1:htag.find(":")]
            indent = int(htag_number) * " "
            h_tags[index] = indent + htag
        h_tags = "\n".join(h_tags)
        formating = f"""
        {parent}
        {h_tags}
        /{parent}
        """
        return formating
