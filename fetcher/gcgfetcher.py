import requests
from lib.event import Event
from fetcher.icalfetcher import IcalFetcher
import icalendar
from lib.category import Category
from fetcher.icalfetcher import IcalFetcher
from helper.gcg import GcgHelper

class GcgFetcher(IcalFetcher):
    def __init__(self,webcache=None):
        super(GcgFetcher,self).__init__("http://www.brownbearsw.com/cal/gcgevents?Op=iCalSubscribe",[ Category("grid-gcg") ])
        self.webcache = webcache
        self.helper = GcgHelper()

    def customizeEvent(self,event):
        if self.helper!=None:
            normalized = self.helper.findRegion(event.hgurl)
            if normalized!=None:
                event.hgurl = "login.greatcanadiangrid.ca:8002:" + normalized

        return event


if __name__=='__main__':
    f = GcgFetcher()

    e = f.fetch()

    for ev in e:
        print str(ev)
