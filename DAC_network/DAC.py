__author__ = 'Jiarui Xu'

class Author():
    def __init__(self, name, aid):
        self.name = name
        self.aid = aid
        self.nicknames = []
        self.paper_ids = []

    def add_paper(self, pid):
        if pid not in self.paper_ids:
            self.paper_ids.append(pid)

    def add_nickname(self, name):
        if name not in self.nicknames:
            self.nicknames.append(name)


class Paper():
    def __init__(self, title, abstract, year, author_names, b_topic, topics, pid, detc, url):

        # Basic info
        self.title = title
        self.abstract = abstract
        self.year = year
        self.author_names = author_names
        self.broad_topic = b_topic
        self.topics = topics
        self.pid = pid
        self.detc = detc
        self.url = url

        # add later
        self.author_ids = []
        self.citations = []
        self.cited_by = []

    def add_author_id(self, aid):
        if aid not in self.author_ids:
            self.author_ids.append(aid)