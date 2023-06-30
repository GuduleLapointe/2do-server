import requests
from lib.event import Event
from dateutil import parser
from lxml import html
import re
import sys
import pytz
import datetime
from lib.category import Category
from helper.helper import Helper

class GridTalkEvent(Event):
    tz_berlin = pytz.timezone('Europe/Berlin')
    hgexp = re.compile('secondlife://hypergrid.org:8002:([^/]+)/')

    # 02.01.2015, 20:00 - 31.12.2015, 23:59
    fromtoRE = re.compile("([0-9]{2})\.([0-9]{2})\.([0-9]{4}), ([0-9]{2}:[0-9]{2}) - ([0-9]{2})\.([0-9]{2})\.([0-9]{4}), ([0-9]{2}:[0-9]{2})")

    def __init__(self,url,webcache=None):
        super(GridTalkEvent,self).__init__()
        self.url=url
        self.categories = self.categories + [ Category("grid-gridtalk") ]
        self.webcache=webcache

    def parseTime(self, s):
        m = self.fromtoRE.search(s)
        self.start = None
        self.end = None

        if m!=None:
            d1 = m.group(1)
            m1 = m.group(2)
            y1 = m.group(3)
            t1 = m.group(4)

            #d2 = m.group(5)
            #m2 = m.group(6)
            #y2 = m.group(7)
            t2 = m.group(8)

            date1 = "%s-%s-%s" % (y1,m1,d1)
            self.start = GridTalkEvent.tz_berlin.localize(parser.parse(date1+" "+t1))
            self.end = GridTalkEvent.tz_berlin.localize(parser.parse(date1+" "+t2))

            if t1==t2:
                self.end += datetime.timedelta(hours=2)

    def fetch(self):
        if self.url == None:
            raise Exception("fetching GridTalkEvent without url set")

        if self.webcache!=None:
            r = self.webcache.fetch(self.url)
        else:
            r = requests.get(self.url)

        if r.status_code == 200:
            tree = html.fromstring(r.text)

            trs = tree.xpath('//div[@id="content"]/div[@class="wrapper"]/table//tr')

            if len(trs)!=4:
                raise HtmlParsingError("GridTalkEvent can't find table rows")

            self.title = trs[0].text_content().strip()

            rawtime = trs[1].text_content().strip()

            self.parseTime(rawtime)

            self.description = trs[3].text_content().strip()

            self.categories += [ Category("grid-gridtalk") ]

    def __str__(self):
        rv = super(GridTalkEvent,self).__str__()

        return rv


class GridTalkFetcher:

    def __init__(self, eventlist, webcache=None):
        self.eventlist=eventlist
        self.webcache=webcache
        self.helper=Helper()

    def fetch(self, limit=0):
        url = "http://www.gridtalk.de/calendar.php"

        numMonths = 2

        while numMonths>0:
            r = self.webcache.fetch(url, 1000, 1800)

            if r.status_code==200:
                tree = html.fromstring(r.text)

                events = tree.xpath('//div[contains(@class,"public_event")]/a')

                for eventNode in events:
                    href = eventNode.get('href')
                    title = eventNode.get('title')
                    event = GridTalkEvent("http://www.gridtalk.de/" + href, self.webcache)
                    event.title = title
                    event.fetch()
                    event = self.helper.customizeEvent(event)
                    if event != None:
                        self.eventlist.add(event)
 
                nextUrlNode = tree.xpath('//div[@class="float_right"]/a[2]/@href')

                if len(nextUrlNode)!=1:
                    raise HtmlParsingError("GridTalkFetcher: unable to find next month link")

                url = "http://www.gridtalk.de/" + nextUrlNode[0]

            numMonths -= 1

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_gridtalk.cache")

    f = GridTalkFetcher(eventlist, cache)

    f.fetch(12)

    cache.flush()

    for event in eventlist:
        print str(event)
