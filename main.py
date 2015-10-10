#!/usr/bin/env python

import sys
from lib.event import Event
import importlib
from time import time,gmtime,asctime
import datetime
import pytz
import icalendar
import argparse
import cPickle
from lib.webcache import WebCache

fetchers = [
    ("kitelyfetcher", "KitelyFetcher", 0),
    ("metropolisfetcher", "MetropolisFetcher", 0),
    ("francogridfetcher", "FrancoGridFetcher", 0),
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ]

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="fetch, update or write")

    args = parser.parse_args()

    if args.command=='update':
        print "not implemented yet"
        sys.exit(1)

    if args.command=='write':

        datafile = file('data/events.pck')
        events = cPickle.load(datafile)
        datafile.close()

        cal = icalendar.Calendar()

        cal.add('PRODID','-//Linkwater//Aggregator//EN')
        cal.add('VERSION','2.0')
        cal.add('CALSCALE','GREGORIAN')

        i=0

        start_after = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
        end_before = start_after + datetime.timedelta(days=365)

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
                ie.add('categories', ','.join(map(lambda c: c.normalize(),e.categories)))
                ie.add('status',icalendar.vText('confirmed'))
        
                cal.add_component(ie)

                i=i+1
                #print str(e)

        file('data/test.ics','w+').write(cal.to_ical())

    if args.command=='fetch':

        webcache = WebCache("data/web.cache")

        events = []

        for (module_name,class_name,limit) in fetchers:
            mod = importlib.import_module("fetcher."+module_name)

            fetcher = getattr(mod, class_name)(webcache)

            events = events + fetcher.fetch(limit)

            webcache.flush()

        events = sorted(events, key=lambda e: e.start)

        datafile = file('data/events.pck', 'w+')
        cPickle.dump(events, datafile, protocol=2)
        datafile.close()

if __name__ == "__main__":
    main()

