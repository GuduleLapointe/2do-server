from lib.cache import Cache
import requests
from random import randrange

class WebCache(Cache):
    min_expiry = 3*3600
    max_expiry = 24*3600

    def __init__(self, filename):
        super(WebCache,self).__init__(filename)
        self.hits = 0
        self.miss = 0

    def fetch(self, url, min_expiry=None, max_expiry=None, timeout=10):
        if self.exists(url):
            self.hits += 1
            return self.retrieve(url)

        self.miss += 1

        r = requests.get(url, headers={"user-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"}, timeout=timeout)

        if r.status_code==200:
            if max_expiry!=None and min_expiry!=None:
                expiry = randrange(min_expiry,max_expiry)
            else:
                expiry = randrange(WebCache.min_expiry, WebCache.max_expiry)

            self.store(url, r, expiry)

        return r

    def __str__(self):
        return "hits: " + str(self.hits) + ", miss: " + str(self.miss)

if __name__ == "__main__":
    c = WebCache("data/test_web.cache")

    c.fetch("http://linkwater.org/")

    print str(c.fetch("http://linkwater.org/"))

    c.flush()

    cc = WebCache("data/test_web.cache")

    print str(cc.fetch("http://linkwater.org/"))
    print str(cc.fetch("http://linkwater.org/"))
