import re
from helper import Helper
from lib.category import Category

class KitelyHelper(Helper):

    dictionary = {
        re.compile('Seanchai Library - Spaceworld', re.I) : 'grid.kitely.com:8002:Spaceworld',
        re.compile('Seanchai' , re.I): 'grid.kitely.com:8002:Seanchai',
        re.compile('^\s*$', re.I) : 'grid.kitely.com:8002:Kitely Welcome Center',
        re.compile('^grid.kitely.com:8002:Never%20Ending%20Story$', re.I) : 'grid.kitely.com:8002:Never Ending Story',
        re.compile('^Blues at the Junkyard with DJ Thunder$', re.I) : 'grid.kitely.com:8002:Cookie II',
        re.compile('^SLexit island in Kitely$', re.I) : 'grid.kitely.com:8002:SLexit',
        re.compile('^grid.kitely.com:8002:Panthalassa take', re.I) : 'grid.kitely.com:8002:Panthalassa',
    }

    titledict = {
        re.compile('^LEN\s+-\s+English Drama', re.I) : 'grid.kitely.com:8002:Learn English Network Academy',
    }

    def customizeEvent(self, event):
        event = super(KitelyHelper, self).customizeEvent(event)

        if event.title!=None:
            for exp in KitelyHelper.titledict.keys():
                if exp.search(event.title):
                    event.hgurl = KitelyHelper.titledict[exp]
        if event.hgurl!=None:
            for exp in KitelyHelper.dictionary.keys():
                if exp.search(event.hgurl):
                    event.hgurl = KitelyHelper.dictionary[exp]
        else:
            event.hgurl = "grid.kitely.com:8002:Kitely Welcome Center"

        if event.hgurl == "grid.kitely.com:8002:Seanchai":
            event.addCategory(Category('literature'))

        return event


if __name__=='__main__':
    pass
