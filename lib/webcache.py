from lib.cache import Cache
import requests

class WebCache(Cache):

    def fetch(self, url):
        if self.exists(url):
            return self.retrieve(url)
        r = requests.get(url)
        if r.status_code==200:
            self.store(url, r)
        return r

if __name__ == "__main__":
    c = WebCache("data/test_web.cache")

    c.fetch("http://linkwater.org/")

    print str(c.fetch("http://linkwater.org/"))

    c.flush()

    cc = WebCache("data/test_web.cache")

    print str(cc.fetch("http://linkwater.org/"))
    print str(cc.fetch("http://linkwater.org/"))