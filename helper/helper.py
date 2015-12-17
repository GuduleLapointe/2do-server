import re
from lib.category import Category
import datetime

class Helper(object):

    expr = {
        'title' : {
            re.compile('(^DJ.*)|(.*\sDgJ\s)', flags=re.I)    : 'music',
            re.compile('\sfair(\s|$)', flags=re.I)          : 'fair',
            re.compile('.*office hours*', flags=re.I)          : 'social',
            re.compile('.*literary.*', flags=re.I)          : 'literature',
            re.compile('.*zombie infection.*', flags=re.I)          : 'fair',
            re.compile('tutorial', flags=re.I)          : 'education',
            re.compile('speedbuild', flags=re.I)          : 'social',
            re.compile('hangout', flags=re.I)          : 'social',
            re.compile('lesung', flags=re.I)          : 'literature',
            re.compile('write-in', flags=re.I)          : 'literature',
            re.compile('in Deutsch', flags=re.I)          : 'lang-Deutsch',
        },
        'description' : {
            re.compile('\[\[Category:Art\]\]', flags=re.I)  : 'art',
            re.compile('\[\[Category:Education\]\]', flags=re.I)  : 'education',
            re.compile('\[\[Category:Fair\]\]', flags=re.I)  : 'fair',
            re.compile('\[\[Category:Lecture\]\]', flags=re.I)  : 'lecture',
            re.compile('\[\[Category:Literature\]\]', flags=re.I)  : 'literature',
            re.compile('\[\[Category:Music\]\]', flags=re.I)    : 'music',
            re.compile('\[\[Category:Roleplay\]\]', flags=re.I)  : 'roleplay',
            re.compile('\[\[Category:Social\]\]', flags=re.I)  : 'social',
            re.compile('(^DJ.*)|(.*\sDJs?\s)', flags=re.I)    : 'music',
            re.compile('(singing|singer|songs)', flags=re.I)    : 'music',
            re.compile('(dancing|dance)', flags=re.I)    : 'music',
            re.compile('(classic rock|jazz|blues|guitar|instrument)', flags=re.I)    : 'music',
            re.compile('role.?play', flags=re.I)  : 'roleplay',
            re.compile('para.?rp', flags=re.I)  : 'roleplay',
            re.compile('music', flags=re.I)  : 'music',
            re.compile('karaoke', flags=re.I)  : 'music',
            re.compile('\sooc\s', flags=re.I)  : 'roleplay',
            re.compile('\stalk\s', flags=re.I)  : 'social',
            re.compile('\smeet\s', flags=re.I)  : 'social',
            re.compile('\sstory\s', flags=re.I)  : 'literature',
            re.compile('avatar repertory theat', flags=re.I)  : 'art',
        },
        'any' : {
            re.compile('community.*(meeting|gathering)', flags=re.I): 'social',
            re.compile('role.?play', flags=re.I)  : 'roleplay',
            re.compile('para.?rp', flags=re.I)  : 'roleplay',
            re.compile('community', flags=re.I)  : 'social',
            re.compile('vernissage', flags=re.I)  : 'art',
            re.compile('exhibition', flags=re.I)  : 'art',
            re.compile('paintings', flags=re.I)  : 'art',
            re.compile('paintings', flags=re.I)  : 'art',
            re.compile('author', flags=re.I)  : 'literature',
            re.compile('Seanchai', flags=re.I)  : 'literature',
        }
    }

    catexpr = re.compile('\[\[Category:[^]]+\]\]', flags=re.I)

    # hgurl extraction
    hgexpr = [
        # (expr, group, prepend)
        ( re.compile('(Taxi|Location)\s*:?\s*(hop://)?([^:]+:[0-9]+(:|/).*)$', re.I | re.M), 3, ""),
        ( re.compile('(Taxi|Location)\s*:?\s*(hop://)?([^:]+:[0-9]+(:|/).*)$', re.I | re.M), 3, ""),
        ( re.compile('hop://([^:]+:[0-9]+(:|/)[^/]*)$', re.I | re.M), 1, ""),
        ( re.compile('hop://([^:]+:[0-9]+(:|/)[^/]*)/', re.I | re.M), 1, ""),
        ( re.compile('OSGrid\s*-\sRegion\s+([^\n]+)$', re.I | re.M), 1, "hg.osgrid.org:80:"),
        ( re.compile('^([^:\n]+:[0-9]+:)(\s|$)', re.I | re.M), 1, ""),
    ]

    # grid extraction
    gridexpr = {
        re.compile('nextlife-world.de', re.I) : Category('grid-nextlife'),
        re.compile('dorenas-world.de', re.I) : Category('grid-dorenas'),
        re.compile('anettes-welt.de', re.I) : Category('grid-anettes'),
        re.compile('world.narasnook.com', re.I) : Category('grid-narasnook'),
        re.compile('login.digiworldz.com', re.I) : Category('grid-digiworldz'),
        re.compile('refugegrid.com', re.I) : Category('grid-refuge'),
        re.compile('hg.lighthousepoint.co.uk', re.I) : Category('grid-lhp'),
        re.compile('hypergrid.org', re.I) : Category('grid-metropolis'),
    }
        

    # guess grid from hgurl
    def getGridFromHgurl(self, event):
        for expr in Helper.gridexpr:
            if expr.search(event.hgurl)!=None:
                event.addCategory(Helper.gridexpr[expr])
                break
        return event

    def getLocationFromDescription(self, event):
        for (expr, group, prepend) in Helper.hgexpr:
            match = expr.search(event.description)
            if match!=None:
                return prepend + match.group(group).replace('/',':')
        return None

    def customizeEvent(self, event):
        for expr in Helper.expr['title'].keys():
            if expr.search(event.title)!=None:
                event.addCategory(Category(Helper.expr['title'][expr]))
        for expr in Helper.expr['description'].keys():
            if expr.search(event.description)!=None:
                event.addCategory(Category(Helper.expr['description'][expr]))
        for expr in Helper.expr['any'].keys():
            if expr.search(event.title)!=None:
                event.addCategory(Category(Helper.expr['any'][expr]))
            if expr.search(event.description)!=None:
                event.addCategory(Category(Helper.expr['any'][expr]))


        event.description = Helper.catexpr.sub('', event.description)

        event = self.getGridFromHgurl(event)

        if event.hgurl==None or event.hgurl=='-' or event.hgurl=='':
            event.hgurl=self.getLocationFromDescription(event)

        if event.start!=None and event.end!=None and event.start==event.end:
            event.end += datetime.timedelta(hours=2)
        
        return event
