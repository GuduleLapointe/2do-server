import re
from helper import Helper

class AvatarFestHelper(Helper):
    dictionary = {
        ' AvatarFEST' : 'avatarfest.net:6000',
    }

    def customizeEvent(self, event):
        event = super(AvatarFestHelper, self).customizeEvent(event)
        if event.hgurl is None:
            event.hgurl = "avatarfest.net:6000"
        if event.hgurl in AvatarFestHelper.dictionary.keys():
            event.hgurl = AvatarFestHelper.dictionary[event.hgurl]
        return event


if __name__=='__main__':
    pass
