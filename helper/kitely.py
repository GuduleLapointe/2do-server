import re
from helper import Helper
from lib.category import Category

class KitelyHelper(Helper):

    dictionary = {
        re.compile('Seanchai Library - Spaceworld', re.I) : 'grid.kitely.com:8002:Spaceworld',
        re.compile('Seanchai' , re.I): 'grid.kitely.com:8002:Seanchai',
        re.compile('^\s*$', re.I) : 'grid.kitely.com:8002:Kitely Welcome Center',
    }

    def customizeEvent(self, event):
        event = super(KitelyHelper, self).customizeEvent(event)

        if event.title=="Kitely Merchant Fair":
            event.hgurl = "grid.kitely.com:8002:Kitely Hypergrid Merchant Fair"
        elif event.hgurl!=None:
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
