from time import gmtime,asctime
from lib.category import Category
import hashlib

class Event(object):
    def __init__(self):
        self.title = "Untitled event"
        self.hgurl = "-"
        self.grid = "-"
        self.description = "Undescribed event.."
        self.start = 0
        self.end = 0
        self.categories = []

    def hash(self):
        msg = repr(self.title) + str(self.start) + repr(self.hgurl)
        return hashlib.md5(msg).hexdigest()

    def __str__(self):
        rv = "Event "+self.hash()+" :\n"
        rv = rv + " title       " + repr(self.title) + "\n"
        rv = rv + " hgurl       " + repr(self.hgurl) + "\n"
        rv = rv + " grid        " + repr(self.grid) + "\n"
        rv = rv + " description " + repr(self.description) + "\n"
        rv = rv + " start       " + str(self.start) + "\n"
        rv = rv + " end         " + str(self.end) + "\n"
        rv = rv + " categories  " + str(self.categories) + "\n"

        return rv       

    def addCategory(self,newcat):
        if type(newcat)==type([]):
            for cat in newcat:
                self.addCategory(cat)
        else:
            if not newcat in self.categories:
                self.categories += [newcat]
