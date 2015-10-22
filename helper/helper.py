import re
from lib.category import Category

class Helper(object):

    expr = {
        'title' : {
            re.compile('(^DJ.*)|(.*\sDgJ\s)', flags=re.I)    : 'music',
            re.compile('community.*(meeting|gathering)', flags=re.I): 'social',
            re.compile('\sfair(\s|$)', flags=re.I)          : 'fair',
            re.compile('.*office hours*', flags=re.I)          : 'social',
            re.compile('.*literary.*', flags=re.I)          : 'literature',
            re.compile('.*zombie infection.*', flags=re.I)          : 'fair',
            re.compile('tutorial', flags=re.I)          : 'education',
            re.compile('speedbuild', flags=re.I)          : 'social',
            re.compile('hangout', flags=re.I)          : 'social',
        },
        'description' : {
            re.compile('(^DJ.*)|(.*\sDJs?\s)', flags=re.I)    : 'music',
            re.compile('(singing|singer|songs)', flags=re.I)    : 'music',
            re.compile('(dancing|dance)', flags=re.I)    : 'music',
            re.compile('(classic rock|jazz|blues|guitar|instrument)', flags=re.I)    : 'music',
            re.compile('\[\[Category:Music\]\]', flags=re.I)    : 'music',
            re.compile('\[\[Category:Lecture\]\]', flags=re.I)  : 'lecture',
            re.compile('\[\[Category:Social\]\]', flags=re.I)  : 'social',
            re.compile('role.?play', flags=re.I)  : 'roleplay',
            re.compile('music', flags=re.I)  : 'music',
            re.compile('karaoke', flags=re.I)  : 'music',
            re.compile('\sooc\s', flags=re.I)  : 'roleplay',
            re.compile('\stalk\s', flags=re.I)  : 'social',
            re.compile('\smeet\s', flags=re.I)  : 'social',
            re.compile('\sstory\s', flags=re.I)  : 'literature',
            re.compile('avatar repertory theat', flags=re.I)  : 'art',
            re.compile('community', flags=re.I)  : 'social',
        },
    }

    catexpr = re.compile('\[\[Category:[^]]+\]\]', flags=re.I)

    def customizeEvent(self, event):
        for expr in Helper.expr['title'].keys():
            if expr.search(event.title)!=None:
                event.addCategory(Category(Helper.expr['title'][expr]))
        for expr in Helper.expr['description'].keys():
            if expr.search(event.description)!=None:
                event.addCategory(Category(Helper.expr['description'][expr]))

        event.description = Helper.catexpr.sub('', event.description)
        
        return event
