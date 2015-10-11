import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from lib.webcache import WebCache

class AvatarFestFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(AvatarFestFetcher,self).__init__("https://www.google.com/calendar/ical/7qk2kkudtb4m864ljdmtsg308c%40group.calendar.google.com/public/basic.ics", [Category("festival")])
        self.webcache = webcache

if __name__=='__main__':
    cache = WebCache("data/test_avatarfest.cache")

    f = AvatarFestFetcher(cache)

    e = f.fetch()

    cache.flush()

    for ev in e:
        print str(ev)
