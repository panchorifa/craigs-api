

class XRequests(object):
    def __init__(self, url_map):
        self.url_map = url_map

    def get(self, url):
        return open(self.url_map[url], 'r').read()
