import hashlib
import logging
import pickle
import pytz
from icalendar.prop import vText

class EventList:
    def __init__(self, skiplist=None):
        self.skiplist = skiplist
        self.events = []
        self.hashes = []
        logging.basicConfig(filename='eventlist.log', level=logging.DEBUG)

    def add(self, new_event):
        if self.skiplist!=None and self.skiplist.contains(new_event):
            logging.debug("Discarding event in skiplist '" + repr(new_event.title) + "', hash " + new_event.hash() + ', cat ' + str(new_event.categories))
            return

        if new_event.hgurl==None:
            logging.info('Discarding event without hgurl:')
            logging.info(str(new_event))
            return
        
        event_start = (new_event.start - new_event.start.utcoffset()).replace(tzinfo=pytz.utc)

        if type(new_event.hgurl)==vText:
            hgurl = str(new_event.hgurl.title().encode('ascii', 'ignore')).lower()
        else:
            hgurl = str(new_event.hgurl.encode('ascii', 'ignore')).lower()

        #print new_event.hgurl
        new_hash = hashlib.md5( str(event_start) + hgurl ).hexdigest()

        #print repr(new_event.title) + ": '" + str(event_start) + "' '" + hgurl + "' " + new_hash

        if not new_hash in self.hashes:
            self.events += [ new_event ]
            self.hashes += [ new_hash ]
        else:
            logging.debug("Discarding duplicate event '" + repr(new_event.title) + "', hash " + new_event.hash() + ', cat ' + str(new_event.categories))

    def sort(self):
        self.events = sorted(self.events, key=lambda e: e.start)

    def write(self, datafile):
        pickle.dump(self.events, datafile, protocol=2)

    def __getitem__(self, index):
        return self.events[index]

    def __len__(self):
        return len(self.events)
