import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.phaandoria import PhaandoriaHelper

class PhaandoriaFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(PhaandoriaFetcher,self).__init__("https://calendar.google.com/calendar/ical/ath2lhne44mfcsmqp66p0iu2jo%40group.calendar.google.com/public/basic.ics", [Category("grid-phaandoria")], webcache, PhaandoriaHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_phaandoria.cache")

    f = PhaandoriaFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
