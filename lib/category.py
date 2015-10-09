class Category(object):

    dict = {
                'Kunstevent'    : 'art',
                'Social Event'  : 'social',
                'lesung'        : 'lecture',
                'vhs'           : 'education',
                'Special'       : 'entertainment'
            }


    def __init__(self, t):
        self.name = t

    def normalize(self):
        if self.name in self.dict.keys():
            return self.dict[self.name]
        return self.name

    def __str__(self):
        return self.name + "(" + self.normalize() + ")"
       

if __name__ == "__main__":
    print "Kunstevent -> "+ Category("Kunstevent").normalize()
    print "foo -> "+ Category("foo").normalize()
    print "education -> "+ Category("education").normalize()

