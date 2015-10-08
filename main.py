#!/usr/bin/env python

import sys
from lib.event import Event
import importlib
from time import time,gmtime,asctime
import datetime
import pytz
import icalendar

fetchers = [
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ("kitelyfetcher", "KitelyFetcher", 0)
    ]

def main():
    print "Hello, world..."

    events = []

    for (module_name,class_name,limit) in fetchers:
        mod = importlib.import_module("fetcher."+module_name)

        fetcher = getattr(mod, class_name)()

        events = events + fetcher.fetch(limit)

    events = sorted(events, key=lambda e: e.start)

    start_after = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)

    end_before = start_after + datetime.timedelta(days=365)


    cal = icalendar.Calendar()

    cal.add('PRODID','-//Linkwater//Aggregator//EN')
    cal.add('VERSION','2.0')
    cal.add('CALSCALE','GREGORIAN')

    i=0

    for e in events:
        if e.start > start_after and e.end < end_before:
            ie = icalendar.Event()
            ie.add('dtstart', e.start.astimezone(pytz.utc))
            ie.add('dtend', e.end.astimezone(pytz.utc))
            ie.add('dtstamp', pytz.utc.localize(datetime.datetime.utcnow()))
            #ie.add('uid', i)
            ie.add('summary', icalendar.vText(e.title))
            ie.add('description', icalendar.vText(e.description))
            ie.add('location', icalendar.vText(e.hgurl))
            ie.add('categories', icalendar.vText("grid:"+e.grid))
            ie.add('status',icalendar.vText('confirmed'))
    
            cal.add_component(ie)

            i=i+1
            #print str(e)

    file('test.ical','w+').write(cal.to_ical())

if __name__ == "__main__":
    main()

