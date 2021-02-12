#!/usr/bin/env python

import sys
from lib.event import Event
import importlib
from time import time,gmtime,asctime
import datetime
import pytz
import icalendar
import argparse
import pickle
from lib.webcache import WebCache
from exporter.exporter import Exporter
from exporter.ical import IcalExporter
from exporter.text import TextExporter
from exporter.web import JsonExporter
from exporter.htmlexporter import HtmlExporter
from exporter.lslexporter import LslExporter
from exporter.lsl2exporter import Lsl2Exporter
from dateutil import parser
from lib.category import Category
from lib.skiplist import Skiplist
from lib.eventlist import EventList

# sorted in order of preference
# fetchers are run from begin of list to end, and events
# added by later fetchers that are already fetched earlier
# will be discarded
fetchers = [
    ("speculoosworldfetcher", "SpeculoosWorldFetcher", 0),
    ("thefactoryfetcher", "TheFactoryFetcher", 0),
    ("virtualgaypridefetcher", "VirtualGayPrideFetcher", 0),
    ("oceangridfetcher", "OceanGridFetcher", 0),
    ("tranquilitygridfetcher", "TranquilityGridFetcher", 0),
    ("discoverygridfetcher", "DiscoveryGridFetcher", 0),
    ("thirdlifefetcher", "ThirdLifeFetcher", 0),
    ("arcanafetcher", "ArcanaFetcher", 0),
    ("oscc15fetcher", "OSCC15Fetcher", 0),
    ("islandoasisfetcher", "IslandOasisFetcher", 0),
    ("theencoreescapefetcher", "TheEncoreEscapeFetcher", 0),
    ("avatarfestfetcher", "AvatarFestFetcher", 0),
    ("opensimlifefetcher", "OpenSimLifeFetcher", 0),
    ("kitelyfetcher", "KitelyFetcher", 0),
    ("metropolisfetcher", "MetropolisFetcher", 0),
    ("francogridfetcher", "FrancoGridFetcher", 0),
    ("thirdrockfetcher", "ThirdRockFetcher", 0),
    ("lfgridfetcher", "LfGridFetcher", 0),
    ("kalasiddhifetcher", "KalasiddhiFetcher", 0),
    ("phaandoriafetcher", "PhaandoriaFetcher", 0),
    ("vhsfetcher", "VHSFetcher", 0),
    ("exolifefetcher", "ExoLifeFetcher", 0),
    ("nextlifefetcher", "NextLifeFetcher", 0),
    ("piratesatollfetcher", "PiratesAtollFetcher", 0),
    ("narasnookfetcher", "NarasNookFetcher", 0),
    ("snikyfetcher", "SnikyFetcher", 0),
    ("miscfetcher", "MiscFetcher", 0),
    ("opensimworldfetcher", "OpenSimWorldFetcher", 0),

    ## disabled, not working
    # ("gridtalkfetcher", "GridTalkFetcher", 0),
    # ("japanopenfetcher", "JapanOpenFetcher", 0),
    # ("gcgfetcher", "GcgFetcher", 0),
    ]

def main():

    argparser = argparse.ArgumentParser()

    group = argparser.add_mutually_exclusive_group()
    group.add_argument("-f","--fetch",action="store_true")
    group.add_argument("-w","--write",action="store_true")
    group.add_argument("-u","--update",action="store_true")

    argparser.add_argument("-e","--exporter",help="raw, ical, text, lsl, lsl2, html or json")
    argparser.add_argument("-t","--timezone",help="timezone for export, defaults to utc")

    argparser.add_argument("-b","--before",help="only include events before (and including) specified date/time")
    argparser.add_argument("-a","--after",help="only include events after (and including) specified date/time")

    argparser.add_argument("-o","--output",help="output file name")

    argparser.add_argument("-ns","--noskiplist",help="do not process skiplist",action="store_true")

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

    useskiplist = True
    if args.noskiplist:
        useskiplist = False

    if args.update:
        print "not implemented yet"
        sys.exit(1)
    elif args.write:
        datafile = file('data/events.pck')
        events = pickle.load(datafile)
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
        elif args.exporter=="lsl":
            exporter = LslExporter(events, tz, before, after)
            filename = "data/output.lsl"
        elif args.exporter=="lsl2":
            exporter = Lsl2Exporter(events, tz, before, after)
            filename = "data/output.lsl2"
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
        skiplist = None
        if useskiplist:
            skiplist = Skiplist('skiplist')

        webcache = WebCache("data/web.cache")

        eventlist = EventList(skiplist)

        for (module_name,class_name,limit) in fetchers:
            mod = importlib.import_module("fetcher."+module_name)

            fetcher = getattr(mod, class_name)(eventlist, webcache)

            try:
                fetcher.fetch(limit)
            except Exception as e:
                print "! fetcher "+module_name+" failed with exception:"
                print str(e)

            webcache.flush()

            print "webcache status = " + str(webcache)

        #for event in inevents:
        #    if not skiplist.contains(event):
        #        if event.start!=None and event.end!=None and event.hgurl!=None:
        #            events += [event]
        #        else:
        #            print "WARNING dropping invalid event:"
        #            print str(event)

        eventlist.sort()

        datafile = file('data/events.pck', 'w+')
        eventlist.write(datafile)
        datafile.close()
    else:
        print "must specify at least one of -f, -w and -u"
        print ""
        argparser.print_help()

if __name__ == "__main__":
    main()
