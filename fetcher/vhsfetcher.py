import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.vhs import VHSHelper

class VHSFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(VHSFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/04sq3ngb5us2m850rc6o1k0ftc%40group.calendar.google.com/public/basic.ics",
            [Category("education")],
            eventlist,
            webcache,
            VHSHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_vhs.cache")

    f = VHSFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
