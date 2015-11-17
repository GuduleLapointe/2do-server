from datetime import datetime,timedelta
from dateutil import rrule
import pytz
from icalendar.caselessdict import CaselessDict
from icalendar.prop import vRecur,vDDDLists

class RRULEExpander:
    def __init__(self, rule, start, end, rrlimit=None, exdate=None):
        self.rule = rule

        self.tz = start.tzinfo.zone

        # TODO: what if zones differ? replace end w/ len in function signature
        #self.start = start.replace(tzinfo=None)
        #self.end = end.replace(tzinfo=None)
        self.start = start
        self.end = end

        if rrlimit==None:
            rrlimit = pytz.utc.localize(datetime.now()) + timedelta(days=30)

        self.rrlimit = rrlimit.replace(tzinfo=None)

        self.rrlimit = rrlimit
        self.exdate = exdate

            # calc event length
        eventlen = end - start

            # fix until
        until = rule.get('UNTIL')

        if until!=None:
            newuntil = []
            for entry in until:
                if type(entry)==datetime.date:
                    entry = datetime.combine(entry, datetime.time())
                    entry = pytz.utc.localize(entry)
                newuntil += [entry]
            rule['UNTIL'] = newuntil

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

        #instance = instance.tzinfo.normalize(instance)

        if instance > self.rrlimit:
            raise StopIteration()

        return instance


if __name__=='__main__':
    pacific = pytz.timezone('US/Pacific')


    print "----------------------------------------------"

    start = datetime(2015, 10, 1, 19, 0, tzinfo=pacific)
    end = datetime(2015, 10, 1, 21, 0, tzinfo=pacific)

    e = RRULEExpander(
            vRecur({'BYDAY': ['TH'], 'FREQ': ['MONTHLY'], 'UNTIL': [datetime(2015, 12, 31, 23, 0, tzinfo=pytz.utc)]}),
            start,
            end
        )

    for d in e:
        print "> " + str(d) + " - " + str(d.tzinfo.normalize(d))

    print "----------------------------------------------"

    start = datetime(2015, 10, 1, 19, 0, tzinfo=pacific)
    end = datetime(2015, 10, 1, 21, 0, tzinfo=pacific)

    e = RRULEExpander(
            vRecur({'BYDAY': ['TH'], 'FREQ': ['WEEKLY']}),
            start,
            end
        )

    for d in e:
        print "> " + str(d) + " - " + str(d.tzinfo.normalize(d))


