import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.helper import Helper

class OpenSimLifeFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(OpenSimLifeFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/ec75jhedkmd044t987vtfrnjh4%40group.calendar.google.com/private-2bb542c0613698bcac7f2d1af013ac9a/basic.ics",
            [Category("grid-opensimlife")],
            eventlist,
            webcache,
            Helper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_opensimlife.cache")

    f = OpenSimLifeFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
