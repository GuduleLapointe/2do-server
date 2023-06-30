import re
from helper import Helper

class ZanGridHelper(Helper):
    hgexpr = {
        re.compile('hg.zangrid.ch:8002:Aachen', flags=re.I)		: "hg.zangrid.ch:8002:Aachen",
        re.compile('hg.zangrid.ch:8002:Nedra', flags=re.I)		: "hg.zangrid.ch:8002:Nedra",
        re.compile('hg.zangrid.ch:8002:Partyland', flags=re.I)		: "hg.zangrid.ch:8002:Partyland",
        re.compile('hg.zangrid.ch:8002:HyperZan', flags=re.I)		: "hg.zangrid.ch:8002:HyperZan",
        re.compile('hg.zangrid.ch:8002:Greece', flags=re.I)		: "hg.zangrid.ch:8002:Greece",
        re.compile('login.zangrid.ch:8002:Aachen', flags=re.I)		: "hg.zangrid.ch:8002:Aachen",
        re.compile('login.zangrid.ch:8002:Nedra', flags=re.I)		: "hg.zangrid.ch:8002:Nedra",
        re.compile('login.zangrid.ch:8002:Partyland', flags=re.I)	: "hg.zangrid.ch:8002:Partyland",
        re.compile('login.zangrid.ch:8002:HyperZan', flags=re.I)	: "hg.zangrid.ch:8002:HyperZan",
        re.compile('login.zangrid.ch:8002:Greece', flags=re.I)		: "hg.zangrid.ch:8002:Greece",
    }

    def customizeEvent(self, event):
        event = super(ZanGridHelper, self).customizeEvent(event)

        if event.hgurl!=None:
            for exp in ZanGridHelper.hgexpr:
                if exp.search(event.hgurl):
                    event.hgurl = ZanGridHelper.hgexpr[exp]
                    return event

        return None

if __name__=='__main__':
    pass
