from html.parser import HTMLParser


class OpenTagFinder(HTMLParser):
    open_tags = []
    open_tags_lines = []
    end_tags = []
    singleton_tags = [
                    "area",
                    "base",
                    "col",
                    "br",
                    "command",
                    "hr",
                    "embed",
                    "img",
                    "input",
                    "link",
                    "meta",
                    "source",
                    "track",
                    "wbr",
                ]

    def handle_starttag(self, tag, attrs):
        if tag not in self.singleton_tags:
            self.open_tags.insert(0, tag)
            self.open_tags_lines.insert(0, self.getpos()[0])

    def handle_endtag(self, tag):
        if tag not in self.singleton_tags:
            self.end_tags.append(tag)
            if tag in self.open_tags:
                index = self.open_tags.index(tag)
                del self.open_tags[index]
                del self.open_tags_lines[index]

    def get_open_tags(self):
        string_of_open_tags = ""
        for line, tag in enumerate(self.open_tags):
            line = self.open_tags_lines[line]
            string_of_open_tags = f"閉じてないタグ <{tag}>: {line}行目 \n" + string_of_open_tags
        # print(len(self.end_tags),len(self.open_tags) )
        self.open_tags.clear()
        self.open_tags_lines.clear()
        self.end_tags.clear()
        return string_of_open_tags
