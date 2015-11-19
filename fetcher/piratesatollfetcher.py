import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache
from helper.piratesatoll import PiratesAtollHelper

class PiratesAtollFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(PiratesAtollFetcher,self).__init__("https://www.google.com/calendar/ical/johnsimmonshypertext.com_j3h9nteue42li3qbpujh9o9doc%40group.calendar.google.com/public/basic.ics", [Category("grid-piratesatoll")], webcache, PiratesAtollHelper())
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    cache = WebCache("data/test_piratesatoll.cache")

    f = PiratesAtollFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
