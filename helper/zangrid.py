import re
from helper import Helper

class ZanGridHelper(Helper):
    hgexpr = [
        re.compile('hg.zangrid.ch:8002:Aachen', re.I),
    ]

    def customizeEvent(self, event):
        event = super(ZanGridHelper, self).customizeEvent(event)

        if event.hgurl!=None:
            whitelisted = False
            for exp in ZanGridHelper.hgexpr:
                if exp.search(event.hgurl):
                    whitelisted=True
                    break
            if not whitelisted:
                return None
        else:
            return None

        return event

if __name__=='__main__':
    pass
