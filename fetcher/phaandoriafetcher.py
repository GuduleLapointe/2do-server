import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.phaandoria import PhaandoriaHelper

class PhaandoriaFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(PhaandoriaFetcher,self).__init__(
            "https://calendar.google.com/calendar/ical/ath2lhne44mfcsmqp66p0iu2jo%40group.calendar.google.com/public/basic.ics",
            [Category("grid-phaandoria")],
            eventlist,
            webcache,
            PhaandoriaHelper()
        )
        self.webcache = webcache
        self.minexpiry = 600
        self.maxexpirty = 1200

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_phaandoria.cache")

    f = PhaandoriaFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
