import requests
from lib.event import Event
from dateutil import parser
import datetime
from lxml import html
import re
import sys
import pytz
from lib.category import Category
from helper.craft import CraftHelper

class CraftFetcher:
    eventurl="http://webapp.craft-world.org/events/index.php"
    tz_slt = pytz.timezone('US/Pacific')

    def __init__(self, eventlist, webcache):
        self.eventlist = eventlist
        self.webcache = webcache
        self.helper = CraftHelper()

    def fetch(self, limit=0):
        print "CraftFetcher: fetch event page"

        n_events = 0

        rv = []

        r = requests.get(self.eventurl)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            events = tree.xpath('//span[@class="title"]/parent::div/parent::div')
            events += tree.xpath('//span[@class="title"]/parent::a/parent::div/parent::div')

            for event in events:
                print "\rCraftFetcher: processing event "+str(n_events+1),
                n_events += 1
                sys.stdout.flush()

                e = Event()

                e.categories = [ Category("grid-craft") ]

                e.title = event.xpath('.//span[@class="title"]')[0].text

                e.description = '';

                raw = event.xpath('./div')[2].text_content()

                m = re.search('On ([0-9]{1,2}-[0-9]{1,2}-[0-9]{4})', raw)
                if m is None:
                    continue
                date_str = m.group(1)

                m = re.search('at ([0-9]{1,2}:[0-9]{2} (P|A)M) SLT', raw)
                if m is None:
                    continue
                time_str = m.group(1)
            
                date = parser.parse("%s %s" % (date_str, time_str))
                
                e.start = self.tz_slt.localize(date)
                e.end = e.start + datetime.timedelta(hours=2)

                m = re.search('In region:.*?\s+(.*)$', raw)
                if m is None:
                    continue
                region = self.helper.findRegion(m.group(1))

                if region is None:
                    continue

                e.hgurl = "craft-world.org:8002:"+region

                customized = self.helper.customizeEvent(e)

                if customized!=None:
                    self.eventlist.add(customized)

            print ""

        return rv



if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    webcache = WebCache("data/test_craft.cache")

    f = CraftFetcher(eventlist, webcache)

    f.fetch(12)

    webcache.flush()

    for event in eventlist:
        print str(event)
