#!/usr/bin/python
import re

line = u'Magi - Labyrinth of Magic 252'

# http://stackoverflow.com/questions/14550526/regex-for-both-integer-and-float
searchObj = re.search(ur'^.+ (?=.)([+-]?([0-9]*)(\.([0-9]+))?)$', line, re.M|re.I)

if searchObj:
   print "searchObj.group() : ", searchObj.group()
   print "searchObj.group(1) : ", searchObj.group(1)
   print "searchObj.group(2) : ", searchObj.group(2)
else:
   print "Nothing found!!"
