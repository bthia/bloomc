#!/usr/bin/python

import re

#  regex1.py
#  
#
#  Created by Boon Sing Thia on 26/2/18.
#  

mystr = "bra bra bra <meta itemProp=\"name\" content=\"Tencent Holdings Ltd\"/> bra bra bra"
print("mystr = ", mystr)

m = re.match("(.*)<meta itemProp=\"name\" content=\"(?P<mvar>(.*))\"\/>(.*)", mystr)

if m:
    print(m.group("mvar"))
else:
    print("Not found")

# A string.
name = "Clyde Griffiths"

# Match with named groups.
m = re.match("(?P<first>\w+)\W+(?P<last>\w+)", name)

# Print groups using names as id.
if m:
    print(m.group("first"))
    print(m.group("last"))
