import cPickle
from time import time

class CachedObject(object):
    def __init__(self, data, expiry=None):
        self.data = data
        self.expiry = expiry

    def __str__(self):
        return "expiry: "+str(self.expiry)
    

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

    def store(self,key,value,expiry=None):
        self.cache[key] = CachedObject(value,time() + expiry)

    def exists(self,key):
        if self.retrieve(key)!=None:
            return True
        return False

    def retrieve(self,key):
        if key in self.cache.keys():
            cachedObject = self.cache[key]
            if cachedObject.expiry!=None:
                if cachedObject.expiry > time():
                    return cachedObject.data
                else:
                    self.evict(key)
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
