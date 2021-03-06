class Category(object):

    # art, social, lecture, education, entertainment, music, fair, reading, roleplay
    dict = {
                'Kunstevent'    : 'art',
                'Social Event'  : 'social',
                'Lesung'        : 'lecture',
                'VHS'           : 'education',
                'Special'       : 'entertainment',
                'Live'          : 'music',
            }


    def __init__(self, t):
        self.name = t

    def normalize(self):
        if self.name in self.dict.keys():
            return self.dict[self.name]
        return self.name

    def __str__(self):
        return self.normalize()

    def __repr__(self):
        return self.name + "(" + self.normalize() + ")"

    def __eq__(self, other):
        return self.name == other.name
       

if __name__ == "__main__":
    print "Kunstevent -> "+ Category("Kunstevent").normalize()
    print "foo -> "+ Category("foo").normalize()
    print "education -> "+ Category("education").normalize()

    print str(Category("lesung"))

