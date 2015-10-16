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
from exporter.htmlexporter import HtmlExporter
from dateutil import parser

fetchers = [
    ("craftfetcher", "CraftFetcher", 0),
    ("gcgfetcher", "GcgFetcher", 0),
    ("kitelyfetcher", "KitelyFetcher", 0),
    ("metropolisfetcher", "MetropolisFetcher", 0),
    ("francogridfetcher", "FrancoGridFetcher", 0),
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ("avatarfestfetcher", "AvatarFestFetcher", 0),
    ("lfgridfetcher", "LfGridFetcher", 0),
    ]

def main():

    argparser = argparse.ArgumentParser()

    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-f","--fetch",action="store_true")
    group.add_argument("-w","--write",action="store_true")
    group.add_argument("-u","--update",action="store_true")

    argparser.add_argument("-e","--exporter",help="raw, ical, text, html or json")
    argparser.add_argument("-t","--timezone",help="timezone for export, defaults to utc")

    argparser.add_argument("-b","--before",help="only include events before (and including) specified date/time")
    argparser.add_argument("-a","--after",help="only include events after (and including) specified date/time")

    argparser.add_argument("-o","--output",help="output file name")

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

    before = None
    if args.before!=None:
        before = parser.parse(args.before)
        if before.tzinfo==None or before.tzinfo.utcoffset(before)==None:
            before = tz.localize(before)

    if args.update:
        print "not implemented yet"
        sys.exit(1)
    elif args.write:
        datafile = file('data/events.pck')
        events = cPickle.load(datafile)
        datafile.close()

        if args.exporter=="raw":
            exporter = Exporter(events, tz, before, after)
            filename = "data/output.raw"
        elif args.exporter=="text":
            exporter = TextExporter(events, tz, before, after)
            filename = "data/output.txt"
        elif args.exporter=="json":
            exporter = JsonExporter(events, tz, before, after)
            filename = "data/output.json"
        elif args.exporter=="html":
            exporter = HtmlExporter(events, tz, before, after)
            filename = "data/output.html"
        else: # args.exporter=="ical":
            exporter = IcalExporter(events, tz, before, after)
            filename = "data/output.ics"

        if args.output != None:
            filename = args.output

        if filename == "-":
            f = sys.stdout
        else:
            f = file(filename,'w+')

        f.write(str(exporter))
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
        print ""
        argparser.print_help()

if __name__ == "__main__":
    main()

