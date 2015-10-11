import pytz

class Exporter(object):

    def __init__(self, events, tz, before=None, after=None):
        self.tz = tz
        self.before = before
        self.after = after

        self.events = []
        for event in events:
            if before==None or event.start <= before:
                if after!=None and event.start >= after:
                    self.events += [event]
        print str(len(events)) + " --> " + str(len(self.events))

    def __str__(self):
        return str(self.events)

