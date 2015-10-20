import pytz

class Exporter(object):

    def __init__(self, events, tz, before=None, after=None):
        self.tz = tz
        self.before = before
        self.after = after

        self.events = []
        for event in events:
            if before==None or event.start <= before:
                if after==None or event.end >= after:
                    self.events += [event]

    def __str__(self):
        return str(self.events)

