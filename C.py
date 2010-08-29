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

from constants import SWIDTH, SHEIGHT, OFFSET, SCALE, HTOP1, HTOP2, HTOP3
import math


htop1 = HTOP1
htop2 = HTOP2
htop3 = HTOP3
offset1 = 5
offset2 = 7
offset3 = -12

def mark(offset, height3, height2, height1, string=None, flip=False):
    ln = float(int((offset * SCALE + OFFSET) * 10) / 10.)
    if flip:
        ln = SWIDTH - ln
    if string is not None:
        print '  <text style="font-size:12px;fill:#000000;">'
        print '      <tspan'
        print '       x="%f"' % (ln)
        print '       y="%d"' % (height3)
        print '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>' % (string)
    print '  <path'
    print '       d="M %f,%d,%f,%d"' % (ln, height1, ln, height2)
    print '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />'


def special_mark(offset, height3, height2, height1, string, flip=False):
    ln = float(int((offset * SCALE + OFFSET) * 10) / 10.)
    if flip:
        ln = SWIDTH - ln
    print '  <text style="font-size:12px;fill:#0000ff;">'
    print '      <tspan'
    print '       x="%f"' % (ln)
    print '       y="%d"' % (height3)
    print '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>' % (string)
    print '  <path'
    print '       d="M %f,%d,%f,%d"' % (ln, height1, ln, height2)
    print '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />'


def header(name):
    print '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    print '<!-- Created with Emacs -->'
    print '<svg'
    print '   xmlns:svg="http://www.w3.org/2000/svg"'
    print '   xmlns="http://www.w3.org/2000/svg"'
    print '   version="1.0"'
    print '   width="%s"' % (SWIDTH)
    print '   height="%s">' % (SHEIGHT)
    print '  <g>'
    print '  <path'
    print '       d="M 0,0 L 0,60 L 2400,60 L 2400,0 Z"'
    print '       style="fill:#ffffff;stroke:none;stroke-width:0px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />'
    print '  <text style="font-size:12px;fill:#000000;">'
    print '      <tspan'
    print '       x="5"'
    print '       y="32"'
    print '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>' % (name)


def footer():
    print '  </g>'
    print '</svg>'

def main():

    header('C')

    for i in range(100,200):
        if int((i / 10) * 10) == i:
            mark(math.log(i / 100.), htop3, htop2, htop1,
                 str(float(int(i) * 10 / SCALE)))
        elif int((i / 5) * 5) == i:
            mark(math.log(i / 100.), htop3, htop2, htop1 + offset1)
        else:
            mark(math.log(i / 100.), htop3, htop2, htop1 + offset2)

        for i in range(200,400,2):
            if int((i / 10)*10) == i:
                mark(math.log(i / 100.), htop3, htop2, htop1,
                     str(float(int(i) * 10 / SCALE)))
            else:
                mark(math.log(i/100.), htop3, htop2, htop1 + offset1)

        for i in range(400,1005,5):
            if int((i / 10)* 10) == i:
                if int((i / 50) * 50) == i:
                    mark(math.log(i / 100.), htop3, htop2,
                         htop1, str(float(int(i) * 10 / SCALE)))
                else:
                    mark(math.log(i / 100.), htop3, htop2, htop1)
            else:
                mark(math.log(i / 100.), htop3, htop2, htop1 + offset1)

    special_mark(math.log(math.pi), htop3 + offset3, htop2, htop1, 'π')
    special_mark(math.log(math.e), htop3 + offset3, htop2, htop1, 'e')

    footer()
    return 0

if __name__ == "__main__":
    main()
