import re
from helper import Helper
from lib.category import Category

class LfHelper(Helper):
    hgexp = re.compile('^lfgrid.com:8002:([^:]+)', flags=re.I)

    expr = {
        re.compile("bondage ranch",flags=re.I)      : 'lfgrid.com:8002:Bondage Ranch',
        re.compile("luminaria",flags=re.I)          : 'lfgrid.com:8002:Luminaria',
        re.compile("festival of lights",flags=re.I) : 'lfgrid.com:8002:Luminaria',
    }

    def customizeEvent(self, event):
        event = super(LfHelper, self).customizeEvent(event)

        if event.hgurl!=None and event.hgurl.strip()!="":
            if LfHelper.hgexp.search(event.hgurl)==None:
                for exp in LfHelper.expr:
                    if exp.search(event.hgurl):
                        event.hgurl = LfHelper.expr[exp]
                        break

        if event.hgurl==None or LfHelper.hgexp.search(event.hgurl)==None:
            for exp in LfHelper.expr:
                if exp.search(event.title):
                    event.hgurl = LfHelper.expr[exp]
                    break

        return event


if __name__=='__main__':
    pass
