#!/usr/bin/env python

import sys
import pystache

def main():
    template = file(sys.argv[1], 'r').read().decode('utf-8')
    events = file(sys.argv[2], 'r').read().decode('utf-8')

    print pystache.render(template, {'hypevents-nojs':events}).encode('utf-8')

if __name__=='__main__':
    main()
