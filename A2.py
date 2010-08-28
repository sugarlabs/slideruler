# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from constants import *
import math

# header
print "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>"
print "<!-- Created with Emacs -->"
print "<svg"
print "   xmlns:svg=\"http://www.w3.org/2000/svg\""
print "   xmlns=\"http://www.w3.org/2000/svg\""
print "   version=\"1.0\""
print "   width=\"" + str(SWIDTH) + "\""
print "   height=\"" + str(SHEIGHT) + "\">"
print "  <g>"

print "   <path"
print "       d=\"M 0.0,30 L 2400,30\""
print "       style=\"fill:none;stroke:#ffffff;stroke-width:60px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"

print "  <text style=\"font-size:12px;fill:#000000;\">"
print "      <tspan"
print "       x=\"5\""
print "       y=\"32\""
print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">A</tspan></text>"


ln = str(float(int( (math.log(math.pi)*SCALE/2 + OFFSET)*10 )/10.))
h1 = "0"; h2 = "19"; h3 = "32"
print "  <text style=\"font-size:12px;fill:#000000;\">"
print "      <tspan"
print "       x=\"" + str(ln) + "\""
print "       y=\"" + h3 + "\""
print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">π</tspan></text>"
print "   <path"
print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
print "       style=\"fill:none;stroke:#FF0000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"

ln = str(float(int( (math.log(math.e)*SCALE/2 + OFFSET)*10 )/10.))
h1 = "0"; h2 = "19"; h3 = "32"
print "  <text style=\"font-size:12px;fill:#000000;\">"
print "      <tspan"
print "       x=\"" + str(ln) + "\""
print "       y=\"" + h3 + "\""
print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">e</tspan></text>"
print "   <path"
print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
print "       style=\"fill:none;stroke:#FF0000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"

for i in range(100,200):
    ln = str(float(int( (math.log(i/100.)*SCALE/2 + OFFSET)*10 )/10.))
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(int(i*10/SCALE)) + "</tspan></text>"
    elif int((i/5)*5) == i:
        h1 = "0"; h2 = "17";
    else:
        h1 = "0"; h2 = "15";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(200,400,2):
    ln = str(float(int( (math.log(i/100.)*SCALE/2 + OFFSET)*10 )/10.))
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(int(i*10/SCALE)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(400,1000,5):
    ln = str(float(int( (math.log(i/100.)*SCALE/2 + OFFSET)*10 )/10.))
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(int(i*10/SCALE)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(1000,2000,10):
    ln = str(float(int( (math.log(i/100.)*SCALE/2 + OFFSET)*10 )/10.))
    if int((i/10)*10) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(int(i*10/SCALE)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"
for i in range(2000,10050,50):
    ln = str(float(int( (math.log(i/100.)*SCALE/2 + OFFSET)*10 )/10.))
    if int((i/500)*500) == i:
        h1 = "0"; h2 = "19"; h3 = "32"
        if int((i/100)*100) == i:
            print "  <text style=\"font-size:12px;fill:#000000;\">"
            print "      <tspan"
            print "       x=\"" + str(ln) + "\""
            print "       y=\"" + h3 + "\""
            print "       style=\"font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;\">" + str(int(i*10/SCALE)) + "</tspan></text>"
    else:
        h1 = "0"; h2 = "17";
    print "   <path"
    print "       d=\"M " + ln + "," + h1 + " L " + ln + "," + h2 + "\""
    print "       style=\"fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1\" />"

# footer
print "  </g>"
print "</svg>"
