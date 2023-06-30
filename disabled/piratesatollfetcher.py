import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.piratesatoll import PiratesAtollHelper

class PiratesAtollFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(PiratesAtollFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/johnsimmonshypertext.com_j3h9nteue42li3qbpujh9o9doc%40group.calendar.google.com/public/basic.ics",
            [Category("grid-digiworldz")],
            eventlist,
            webcache,
            PiratesAtollHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_piratesatoll.cache")

    f = PiratesAtollFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
