import cPickle

class Cache(object):
    def __init__(self, filename):
        self.filename=filename
   
        self.cache = None
 
        try:
            cachefile = file(filename)
            self.cache = cPickle.load(cachefile)
            cachefile.close()
            print "cache file "+filename+" loaded"
        except IOError:
            print "cache file "+filename+" unreadable"

        if self.cache == None:
            self.cache = {}

    def store(self,key,value):
        self.cache[key] = value

    def exists(self,key):
        if key in self.cache.keys():
            return True
        return False

    def retrieve(self,key):
        if key in self.cache.keys():
            return self.cache[key]
        return None

    def evict(self,key):
        if key in self.cache.keys():
            del self.cache[key]

    def flush(self):
        cachefile = file(self.filename,'w+')
        cPickle.dump(self.cache, cachefile, protocol=2)
        cachefile.close()


if __name__ == "__main__":
    c = Cache("data/cache_test.pck")

    c.store("foo", {'bar':'baz'})
    c.store("bar", 42)

    c.flush()

    cc = Cache("data/cache_test.pck")

    print str(cc.retrieve("foo"))
    print str(cc.retrieve("bar"))
