#!/usr/bin/python
""" 
To generate all links to the latest version of each indicator call
/@@assessments_latest_versions_links method.

Save the links file and this script to the same directory.

Execute as python name_of_script.py path_to_links_file.txt
It will download all links as xml text files to the current directory
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

