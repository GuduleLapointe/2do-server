import re
from helper import Helper
from lib.category import Category
from dateutil import parser
import pytz
from datetime import timedelta

class NextLifeHelper(Helper):
    tz_berlin = pytz.timezone('Europe/Berlin')
    timeexp = re.compile('Ab\s+([0-9]+)([\.:]([0-9]+))?(\s+Uhr\s+)?(\s+bis\s+([0-9]+)([\.:]([0-9]+))?)?', re.I)

    def customizeEvent(self, event):
        event = super(NextLifeHelper, self).customizeEvent(event)

        match = NextLifeHelper.timeexp.search(event.description)
        if match != None:
            start = match.group(1) + ":"
            if match.group(3) == None:
                start += "00"
            else:
                start += match.group(3)

            start = event.start.strftime("%Y-%m-%d ") + start
            event.start = NextLifeHelper.tz_berlin.localize(parser.parse(start))

            event.end = event.start + timedelta(hours=2)

            if match.group(6)!=None:
                end = match.group(6) + ":"
                if match.group(8)==None:
                    end += "00"
                else:
                    end += match.group(8)

                end = event.start.strftime("%Y-%m-%d ") + end
                event.end = NextLifeHelper.tz_berlin.localize(parser.parse(end))

        return event


if __name__=='__main__':
    pass
