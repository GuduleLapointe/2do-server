class Skiplist:
    def __init__(self, filename):
        self.hashes = file(filename).read().strip().split("\n")

    def contains(self, event):
        return event.hash() in self.hashes


