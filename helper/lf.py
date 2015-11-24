import re
from helper import Helper
from lib.category import Category

class LfHelper(Helper):
    bondagere = re.compile("bondage ranch",re.I)

    def customizeEvent(self, event):
        event = super(LfHelper, self).customizeEvent(event)

        if event.hgurl!=None and event.hgurl.strip()=="":
            if LfHelper.bondagere.search(event.title):
                event.hgurl = "Lfgrid.Com:8002:Bondage Ranch"

        return event


if __name__=='__main__':
    pass
