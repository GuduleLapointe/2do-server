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
from exporter.exporter import Exporter
from exporter.ical import IcalExporter
from exporter.text import TextExporter
from exporter.web import JsonExporter

fetchers = [
    ("kitelyfetcher", "KitelyFetcher", 0),
    ("metropolisfetcher", "MetropolisFetcher", 0),
    ("francogridfetcher", "FrancoGridFetcher", 0),
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ]

def main():

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f","--fetch",action="store_true")
    group.add_argument("-w","--write",action="store_true")
    group.add_argument("-u","--update",action="store_true")

    parser.add_argument("-e","--exporter",help="raw or ical")
    parser.add_argument("-t","--timezone",help="timezone for export, defaults to utc")

    args = parser.parse_args()

    if args.update:
        print "not implemented yet"
        sys.exit(1)
    elif args.write:
        datafile = file('data/events.pck')
        events = cPickle.load(datafile)
        datafile.close()

        tz = pytz.utc

        if args.timezone!=None:
            try:
                tz = pytz.timezone(args.timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                print "invalid timezone " + args.timezone
                sys.exit(1)

        if args.exporter=="raw":
            exporter = Exporter(events, tz)
        elif args.exporter=="text":
            exporter = TextExporter(events, tz)
        elif args.exporter=="json":
            exporter = JsonExporter(events, tz)
        else: # args.exporter=="ical":
            exporter = IcalExporter(events, tz)

        file('data/test.ics','w+').write(str(exporter))
    elif args.fetch:
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
    else:
        print "must specify at least one of -f, -w and -u"

if __name__ == "__main__":
    main()

