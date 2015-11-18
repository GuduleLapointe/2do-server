import datetime
from dateutil import rrule
import pytz
from icalendar.caselessdict import CaselessDict
from icalendar.prop import vRecur,vDDDLists

def fixDateTime(dt):
    if type(dt)==datetime.date:
        return datetime.datetime.combine(dt, datetime.time())
    return dt.replace(tzinfo=None)

class RRULEExpander:
    def __init__(self, rule, start, exdate=None, rrlimit=None):
        self.rule = rule

        self.tz = pytz.timezone(start.tzinfo.zone)

        # TODO: what if zones differ? replace end w/ len in function signature
        self.start = start.replace(tzinfo=None)

        if rrlimit==None:
            rrlimit = pytz.utc.localize(datetime.datetime.now()) + datetime.timedelta(days=30)

        self.rrlimit = rrlimit

        self.exdate = exdate

            # fix until
        until = rule.get('UNTIL')

        if until!=None:
            newuntil = []
            for entry in until:
                if type(entry)==datetime.date:
                    entry = datetime.datetime.combine(entry, datetime.time())
                else:
                    entry = entry.replace(tzinfo=None)
                newuntil += [entry]
            rule['UNTIL'] = newuntil
        else:
            # work around for https://bugs.launchpad.net/dateutil/+bug/1517568
            rule['UNTIL'] = [rrlimit.replace(tzinfo=None)]


        rrset = rrule.rruleset()
        rrset.rrule( rrule.rrulestr( rule.to_ical(), dtstart = self.start ) )

        exdate = self.exdate

        if type(exdate)==type([]):
            if exdate!=None:
                for date in exdate:
                    for dd in date.dts:
                        rrset.exdate(fixDateTime(dd.dt))
        elif type(exdate)==vDDDLists:
                    for dd in exdate.dts:
                        rrset.exdate(fixDateTime(dd.dt))

        self.rrset = iter(list(rrset))

    def __iter__(self):
        return self

    def next(self):
        instance = self.rrset.next()

        instance = self.tz.localize(instance)

        #instance = instance.tzinfo.normalize(instance)

        if instance > self.rrlimit:
            raise StopIteration()

        return instance


if __name__=='__main__':
    pacific = pytz.timezone('US/Pacific')
    eastern = pytz.timezone('US/Eastern')
    central = pytz.timezone('US/Central')


    print "----------------------------------------------"

    start = datetime.datetime(2015, 1, 11, 15, 0, tzinfo=central)

    e = RRULEExpander(
            vRecur({'BYDAY': ['SU'], 'FREQ': ['WEEKLY']}),
            start,
        )

    for d in e:
        print "> " + str(d) + " - " + str(d.tzinfo.normalize(d))

    print "----------------------------------------------"

    start = datetime.datetime(2015, 10, 1, 19, 0, tzinfo=pacific)

    e = RRULEExpander(
            vRecur({'BYDAY': ['TH'], 'FREQ': ['MONTHLY'], 'UNTIL': [datetime.datetime(2015, 12, 31, 23, 0, tzinfo=pacific)]}),
            start,
        )

    for d in e:
        print "> " + str(d) + " - " + str(d.tzinfo.normalize(d))

    print "----------------------------------------------"

    start = datetime.datetime(2015, 10, 1, 19, 0, tzinfo=pacific)

    e = RRULEExpander(
            vRecur({'BYDAY': ['TH'], 'FREQ': ['WEEKLY']}),
            start,
        )

    for d in e:
        print "> " + str(d) + " - " + str(d.tzinfo.normalize(d))


