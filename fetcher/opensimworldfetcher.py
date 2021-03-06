import requests
from lib.event import Event
from datetime import timedelta
from dateutil import parser
from lxml import html
import re
import sys
import pytz
from lib.category import Category
from helper.opensimworld import OpensimworldHelper

class OpenSimWorldEvent(Event):
    tz_pacific = pytz.timezone('US/Pacific')
    detailurl = "http://3rdrockgrid.com/new/event-details/?id="

    descre = re.compile('Details:(.*)[0-9]+.*like', re.S)
    timere = re.compile('(.*) SLT')

    def __init__(self, webcache=None, url=None):
        super(OpenSimWorldEvent,self).__init__()
        self.id = None
        self.categories += [ Category("grid-opensimworld") ]
        self.webcache = webcache
        self.url = url

    def fetchHGUrl(self,url):
        fullurl = "http://opensimworld.com" + url
        if self.webcache==None:
            r = requests.get(fullurl)
        else:
            r = self.webcache.fetch(fullurl,24*3600,48*3600)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            self.hgurl = tree.xpath('//div[@class="span5"]//input/@value')[0]

    def fetch(self):
        if self.url==None:
            raise Exception("Fetch on unitialized OpenSimWorldEvent")

        if self.webcache==None:
            r = requests.get(self.url)
        else:
            r = self.webcache.fetch(self.url,1800,3600)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            self.title = tree.xpath('//div[@class="bbox"]/div[@class="cont"]/h4[1]/text()')[0]

            details = tree.xpath('//div[@class="bbox"]/div[@class="cont"]')[0].text_content()

            descmatch = OpenSimWorldEvent.descre.search(details)
            self.description = descmatch.group(1).strip()

            timematch = OpenSimWorldEvent.timere.search(details)
            self.start = OpenSimWorldEvent.tz_pacific.localize(parser.parse(timematch.group(1)))
            self.end = self.start + timedelta(hours=2)

            regionurl = tree.xpath('//div[@class="cont"]/a[1]/@href')[0]
            self.fetchHGUrl(regionurl)

    def __str__(self):
        rv = super(OpenSimWorldEvent,self).__str__()

        return rv


class OpenSimWorldFetcher:
    eventurl="http://opensimworld.com/events"
    tz_pacific = pytz.timezone('US/Pacific')

    def __init__(self, eventlist, webcache):
        self.eventlist = eventlist
        self.webcache = webcache
        self.helper = OpensimworldHelper()

    def fetch(self, limit=0):
        print "OpenSimWorldFetcher: fetch overview.."

        r = self.webcache.fetch(self.eventurl,900,1800)

        if r.status_code==200:
            tree = html.fromstring(r.text)

            eventurls = tree.xpath('//tr//td[2]/b/a/@href')

            nevents = len(eventurls)
            
            ievent = 0
            print "OpenSimWorldFetcher: fetching "+str(nevents)+" events"
            print "OpenSimWorldFetcher: [0/"+str(nevents)+"]    ",
            sys.stdout.flush()

            for url in eventurls:
                print "\rOpenSimWorldFetcher: ["+str(ievent+1)+"/"+str(nevents)+"]        ",
                print "\r",
                sys.stdout.flush()

                ievent = ievent + 1

                e = OpenSimWorldEvent(self.webcache, "http://opensimworld.com" + url)

                e.fetch()

                e = self.helper.customizeEvent(e)

                if e!=None:
                    self.eventlist.add(e)

                if limit>0 and ievent>=limit:
                    break
            print ""

if __name__=='__main__':
    from lib.webcache import WebCache
    from lib.eventlist import EventList

    eventlist = EventList()

    webcache = WebCache("data/test_opensimworld.cache")

    f = OpenSimWorldFetcher(eventlist, webcache)

    f.fetch()

    webcache.flush()

    for event in eventlist:
        print str(event)
