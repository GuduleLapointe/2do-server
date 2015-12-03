import re
from helper import Helper

class ZanGridHelper(Helper):
    hgexpr = [
        re.compile('hg.zangrid.ch:8002:Aachen', re.I),
        re.compile('hg.zangrid.ch:8002:Nedra', re.I),
        re.compile('hg.zangrid.ch:8002:Partyland', re.I),
    ]

    def customizeEvent(self, event):
        event = super(ZanGridHelper, self).customizeEvent(event)

        if event.hgurl!=None:
            for exp in ZanGridHelper.hgexpr:
                if exp.search(event.hgurl):
                    return event

        return None

if __name__=='__main__':
    pass
