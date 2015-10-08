from time import gmtime,asctime

class Event(object):
    def __init__(self):
        self.title = "Untitled event"
        self.hgurl = "-"
        self.grid = "-"
        self.description = "Undescribed event.."
        self.start = 0
        self.end = 0

    def __str__(self):
        rv = "Event:\n"
        rv = rv + " title       " + repr(self.title) + "\n"
        rv = rv + " hgurl       " + repr(self.hgurl) + "\n"
        rv = rv + " grid        " + repr(self.grid) + "\n"
        rv = rv + " description " + repr(self.description) + "\n"
        rv = rv + " start       " + str(self.start) + "\n"
        rv = rv + " end         " + str(self.end) + "\n"

        return rv       
