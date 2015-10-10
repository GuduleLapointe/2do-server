import pytz

class Exporter(object):

    def __init__(self, events, tz):
        self.events = events
        self.tz = tz

    def __str__(self):
        return str(self.events)

