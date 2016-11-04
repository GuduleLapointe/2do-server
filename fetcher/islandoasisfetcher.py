import requests
from lib.event import Event
from dateutil import parser
from lxml import html
import re
import sys
import pytz
import datetime
from lib.category import Category
#from helper.islandoasis import IslandOasisHelper
from helper.islandoasis import IslandOasisHelper
import urllib

class IslandOasisEvent(Event):
    tz_la = pytz.timezone('America/Los_Angeles')
    hgexp = re.compile('secondlife:\/\/([^\/]+)\/')

    def __init__(self,url=None,webcache=None):
        super(IslandOasisEvent,self).__init__()
        self.url = "http://www.islandoasis.biz/" + url
        self.categories = self.categories + [ Category("grid-islandoasis") ]
        self.webcache=webcache

    def fetch(self):
        if self.url == None:
            raise Exception("fetching IslandOasisEvent without url set")

        if self.webcache!=None:
            r = self.webcache.fetch(self.url)
        else:
            r = requests.get(self.url)

        if r.status_code == 200:
            tree = html.fromstring(r.text)

            self.title = tree.xpath('//span[@id="lblEventName2"]')[0].text

            content = tree.xpath('//span[@id="lblWhen"]')[0].text

            datematch = re.search('([0-9]+)/([0-9]+)/([0-9]+)\s+([0-9]+):([0-9]+):([0-9]+)\s+(PM|AM)', content)

            month = datematch.group(1)
            day = datematch.group(2)
            year = datematch.group(3)

            hour = datematch.group(4)
            minute = datematch.group(5)
            second = datematch.group(6)

            ampm = datematch.group(7)

            self.start = self.tz_la.localize(parser.parse("%s-%s-%s %s:%s:%s %s" % (year,month,day,hour,minute,second,ampm)))

            durationstring = tree.xpath('//span[@id="lblDuration"]')[0].text

            durationmatch = re.search('([0-9]+) hour', durationstring, flags=re.I)

            self.end = self.start + datetime.timedelta(hours=int(durationmatch.group(1)))

            self.hgurl = None
            hgurl = tree.xpath('//a[@id="lnkTeleport"]/@href')
            if len(hgurl)>0:
                hgmatch = IslandOasisEvent.hgexp.search(hgurl[0])
                if hgmatch is not None:
                    self.hgurl = 'islandoasisgrid.biz:8002:' + urllib.unquote(hgmatch.group(1))

            #self.categories = self.categories + [Category("lang-"+langmatch)]

            #cats = tree.xpath('//ul[@class="event-categories"]/li/a')
            #for cat in cats:
            #    # cat.pet()
            #    self.categories = self.categories + [ Category(cat.text) ]

            #urls = tree.xpath('//div[@class="entry-content"]//a/@href')

            #for url in urls:
            #    regionmatch = self.hgexp.match(url)
            #    if regionmatch != None:
            #        self.hgurl="hypergrid.org:8002:" + regionmatch.group(1)
            #        break

            self.description = tree.xpath('//textarea[@id="lblEventDesc"]')[0].text_content()

    def __str__(self):
        rv = super(IslandOasisEvent,self).__str__()

        return rv


class IslandOasisFetcher:
    eventurl="http://www.islandoasis.biz/Calendar.aspx"

    def __init__(self, eventlist, webcache=None):
        self.eventlist=eventlist
        self.webcache=webcache
        self.helper=IslandOasisHelper()

    def fetch(self, limit=0):
        print "IslandOasisFetcher: fetch overview page"

        r = self.webcache.fetch(self.eventurl,1000,1800)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            event_urls = tree.xpath('//div[@id="ListView1_Events"]/div/div/div/a/@href')

            nevents = len(event_urls)

            print "IslandOasisFetcher: found "+str(nevents)+" events"

            ievent = 1

            for event_url in event_urls:
                print "IslandOasisFetcher: fetch event [" + str(ievent) + "/" + str(nevents) + "]\r",
                sys.stdout.flush()

                e = IslandOasisEvent(event_url,self.webcache)

                e.fetch()

                customized = self.helper.customizeEvent(e)
                if customized != None:
                    self.eventlist.add(customized)

                ievent = ievent + 1

            print ""


if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    cache = WebCache("data/test_islandoasis.cache")

    f = IslandOasisFetcher(eventlist, cache)

    f.fetch(12)

    cache.flush()

    for event in eventlist:
        print str(event)
