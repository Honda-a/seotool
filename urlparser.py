from urllib.parse import urlparse, urljoin
import re


class UrlParser:
    def __init__(self, domain):
        self.domain = self.get_domain(domain)


    def get_domain(self, url):
        url = urlparse(url)
        if url.netloc:
            return url.scheme + "://" + url.netloc
        else:
            return False

    def get_netloc(self, url):
        url = urlparse(url)
        if url.netloc:
            netloc = url.netloc.replace("www.", "")
            return netloc
        else:
            return False

    def is_relative(self, url):
        part_url = urlparse(url)
        if not part_url.netloc and part_url.path:
            if ".jpg" in url or ".pdf" in url or ".png" in url or ".gif" in url :
                return False
            return True
        else:
            return False

    def is_internal(self, url, domain):
        if not self.is_relative(url):
            if domain in url:
                return True
            else:
                return False
        else:
            return True

    def is_external(self, url, domain):
        # domain = domain.replace("www.", "")
        if not self.is_internal(url, domain):
            if domain in url:
                return False
            elif "http" not in url:
                return False
            else:
                return True
        else:
            return False
# add the jpg pdf png exception to valid and remove it from pretty url
    def valid_url(self, url,domain):
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return False
        if not self.pretty_url(url, domain):
            return False
        else:
            return True

    def pretty_url(self, url, domain):
        url = url.strip()
        match = re.search(r'\d+-\d+-\d+', url)
        invalid = ["@", "void(0);"]
        for invalid_syntax in invalid:
            if invalid_syntax in url:
                return False
        if match:
            return False
        elif not url.endswith("/"):
            url = url + "/"
        url = urlparse(url)
        return urljoin(domain, url.path)
