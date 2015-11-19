import re
import pickle
from datetime import timedelta
from helper import Helper

class PiratesAtollHelper(Helper):
    hgre = re.compile("^[^:]+:[0-9]+:[^:]+$")
    hgre_obscured = re.compile("^(.*[^\s])\s*(@|on)\s*Pirates.*$",re.I)

    def findRegion(self, data):
	if PiratesAtollHelper.hgre.search(data)!=None:
		return data
	match = PiratesAtollHelper.hgre_obscured.search(data)
	if match!=None:
		return 'piratesatoll.com:9032:'+match.group(1)
        if data=='' or data=='-':
        	return None


    def customizeEvent(self, event):
        event = super(PiratesAtollHelper, self).customizeEvent(event)

        hgurl = self.findRegion(event.hgurl)

        if hgurl != None:
            event.hgurl = hgurl
        else:
            return None

        return event

