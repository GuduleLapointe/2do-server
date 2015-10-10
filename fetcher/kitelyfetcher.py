import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache

class KitelyFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(KitelyFetcher,self).__init__("https://www.google.com/calendar/ical/857iq9v0nfqrg3qmt4e00n53rc%40group.calendar.google.com/public/basic.ics")
        self.categories = [ Category("grid-kitely") ]
        self.webcache = webcache

if __name__=='__main__':
    cache = WebCache("data/test_kitely.cache")

    f = KitelyFetcher(cache)

    e = f.fetch()

    f.flush()

    for ev in e:
        print str(ev)
