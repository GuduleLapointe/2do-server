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
from dateutil import parser

fetchers = [
    ("kitelyfetcher", "KitelyFetcher", 0),
    ("metropolisfetcher", "MetropolisFetcher", 0),
    ("francogridfetcher", "FrancoGridFetcher", 0),
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ("avatarfestfetcher", "AvatarFestFetcher", 0),
    ]

def main():

    argparser = argparse.ArgumentParser()

    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-f","--fetch",action="store_true")
    group.add_argument("-w","--write",action="store_true")
    group.add_argument("-u","--update",action="store_true")

    argparser.add_argument("-e","--exporter",help="raw or ical")
    argparser.add_argument("-t","--timezone",help="timezone for export, defaults to utc")

    argparser.add_argument("-b","--before",help="only include events before (and including) specified date/time")
    argparser.add_argument("-a","--after",help="only include events after (and including) specified date/time")

    args = argparser.parse_args()

    tz = pytz.utc

    if args.timezone!=None:
        try:
            tz = pytz.timezone(args.timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            print "invalid timezone " + args.timezone
            sys.exit(1)

    after = None
    if args.after!=None:
        after = parser.parse(args.after)
        if after.tzinfo==None or after.tzinfo.utcoffset(after)==None:
            after = tz.localize(after)
        print "after: " + after.strftime("%Y-%m-%d %H:%M %Z")

    before = None
    if args.before!=None:
        before = parser.parse(args.before)
        if before.tzinfo==None or before.tzinfo.utcoffset(before)==None:
            before = tz.localize(before)
        print "before: " + before.strftime("%Y-%m-%d %H:%M %Z")

    if args.update:
        print "not implemented yet"
        sys.exit(1)
    elif args.write:
        datafile = file('data/events.pck')
        events = cPickle.load(datafile)
        datafile.close()

        if args.exporter=="raw":
            exporter = Exporter(events, tz, before, after)
        elif args.exporter=="text":
            exporter = TextExporter(events, tz, before, after)
        elif args.exporter=="json":
            exporter = JsonExporter(events, tz, before, after)
        else: # args.exporter=="ical":
            exporter = IcalExporter(events, tz, before, after)

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

