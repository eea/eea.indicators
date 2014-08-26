#!/usr/bin/python
""" Save the links file and this script to the same directory.

Execute as python name_of_script.py path_to_links_file.txt
It will download all links as xml text files to the current directory


To generate all links to the latest version of each indicator create a
Script (Python) into ZODB with the following code:

    Products.CMFCore.utils import getToolByName

    res = {}
    cat = getToolByName(context, 'portal_catalog', None)

    ass = cat.searchResults(portal_type="Assessment", review_state="published")
    for a in ass:
        print a.getURL()

    return printed

"""

import sys
import urllib


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print "You need to provide a path to the input filename"
        sys.exit(1)

    inp = sys.argv[1]
    with open(inp) as f:
        links = f.readlines()

    for l in links:
        if l.strip():
            parts = l.split("/")
            fname = "%s_%s.xml" % (parts[-3], parts[-2])
            print "Saving %s from %s..." % (fname, l.strip()),
            req = urllib.urlopen(l)
            data = req.read()

            #links are http://site/path/indicator-id/assessment-id/@@esms.xml
            with open(fname, 'w') as f:
                f.write(data)
            print "done."

