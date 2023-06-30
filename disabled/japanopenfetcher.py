import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from helper.japanopen import JapanOpenHelper

class JapanOpenFetcher(IcalFetcher):
    def __init__(self, eventlist, webcache=None):
        super(JapanOpenFetcher,self).__init__(
            "https://www.jogrid.net/wi/calendar/export_execute.php?preset_what=all&preset_time=recentupcoming&userid=1&authtoken=e28a743647dec6f4201bda97b35ef37db073da2f",
            [Category("grid-jog")],
            eventlist,
            webcache,
            JapanOpenHelper()
        )
        self.webcache = webcache
        self.minexpiry = 1000
        self.maxexpirty = 1800

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_kitely.cache")

    f = JapanOpenFetcher(eventlist, cache)

    f.fetch()

    cache.flush()

    for ev in eventlist:
        print str(ev)
