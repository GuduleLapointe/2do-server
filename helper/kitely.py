import re
from helper import Helper
from lib.category import Category

class KitelyHelper(Helper):

    dictionary = {
        'Seanchai Library ~ Grid.Kitely.Com:8002:Seanchai' : 'grid.kitely.com:8002:Seanchai',
        'Seanchai Library - Spaceworld (Grid.Kitely.Com:8002/Spaceworld)' : 'grid.kitely.com:8002:Spaceworld',
        'One Day Ahead Of The Moon At The Seanchai Library' : 'grid.kitely.com:8002:Seanchai',
        'In The Shadows At The Seanchai Library' : 'grid.kitely.com:8002:Seanchai',
        '' : 'grid.kitely.com:8002:Kitely Welcome Center',
        ' ' : 'grid.kitely.com:8002:Kitely Welcome Center',
    }

    def customizeEvent(self, event):
        event = super(KitelyHelper, self).customizeEvent(event)

        if event.title=="Kitely Merchant Fair":
            event.hgurl = "grid.kitely.com:8002:Kitely Hypergrid Merchant Fair"
        elif event.hgurl in KitelyHelper.dictionary.keys():
            event.hgurl = KitelyHelper.dictionary[event.hgurl]

        if event.hgurl == "grid.kitely.com:8002:Seanchai":
            event.addCategory(Category('literature'))

        return event


if __name__=='__main__':
    pass
