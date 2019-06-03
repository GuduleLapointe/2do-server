import re
from helper import Helper
from lib.category import Category

class TranquilityGridHelper(Helper):
    hgexp = re.compile('^tranquility-grid.info:8002:([^:]+)', flags=re.I)

    expr = {
        re.compile(".*The Pier.*",flags=re.I)      : 'tranquility-grid.info:8002:The Pier',
        re.compile(".*Fantasy Island.*",flags=re.I)          : 'tranquility-grid.info:8002:Fantasy Island',
        re.compile(".*Fallout Shelter.*",flags=re.I)          : 'tranquility-grid.info:8002:Fantasy Island',
        re.compile(".*Tranquility Welcome.*",flags=re.I) : 'tranquility-grid.info:8002:Tranquility Welcome',
        re.compile(".*Tranquility Events.*",flags=re.I) : 'tranquility-grid.info:8002:Tranquility Events',
        re.compile(".*Welcome.*",flags=re.I)      : 'tranquility-grid.info:8002:Welcome',
        re.compile(".*H20.*",flags=re.I) : 'tranquility-grid.info:8002',
    }

    def customizeEvent(self, event):
        event = super(TranquilityGridHelper, self).customizeEvent(event)

        if event.hgurl!=None and event.hgurl.strip()!="":
            if TranquilityGridHelper.hgexp.search(event.hgurl)==None:
                event.hgurl = 'tranquility-grid.info:8002:' + event.hgurl
                for exp in TranquilityGridHelper.expr:
                    if exp.search(event.hgurl):
                        event.hgurl = TranquilityGridHelper.expr[exp]
                        break

        if event.hgurl==None or TranquilityGridHelper.hgexp.search(event.hgurl)==None:
            for exp in TranquilityGridHelper.expr:
                if exp.search(event.title):
                    event.hgurl = TranquilityGridHelper.expr[exp]
                    break

        return event


if __name__=='__main__':
    pass
