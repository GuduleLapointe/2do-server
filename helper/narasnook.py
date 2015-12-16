import re
from helper import Helper
from lib.category import Category

class NarasNookHelper(Helper):

    hopexp = re.compile('hop://([^:]+:[0-9]+)(/([^/]*))?', re.I)
    hgexp = re.compile('([^/:\s]+:[0-9]+)(:[^/]*)?', re.I)

    dictionary = {
        re.compile('dajkda', re.I) : 'grid.kitely.com:8002:NarasNook Welcome Center',
        re.compile('word.narasnook.com:8900$', re.I) : 'world.narasnook.com:8900',
        re.compile('hg.zangrid.ch:8002:Partyland', re.I) : 'hg.zangrid.ch:8002:Partyland',
    }

    def customizeEvent(self, event):

        if event.hgurl!=None:

            event.hgurl = event.hgurl.strip()

            match = NarasNookHelper.hopexp.search(event.hgurl)
            if match!=None:
                event.hgurl = match.group(1) + ":" + match.group(3)
            else:
                match = NarasNookHelper.hgexp.search(event.hgurl)
                if match!=None:
                    if match.group(2)!=None:
                        event.hgurl = match.group(1) + match.group(2)
                    else:
                        event.hgurl = match.group(1)

            for exp in NarasNookHelper.dictionary.keys():
                if exp.search(event.hgurl):
                    event.hgurl = NarasNookHelper.dictionary[exp]

            event.hgurl = event.hgurl.strip()

        event = super(NarasNookHelper, self).customizeEvent(event)

        return event


if __name__=='__main__':
    pass
