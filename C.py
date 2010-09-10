# -*- coding: utf-8 -*-
#Copyright (c) 2009,2010 Walter Bender

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

# position constants for SLIDE
slide1 = HTOP1
slide2 = HTOP2
slide3 = HTOP3
slide_offset1 = 5
slide_offset2 = 7
slide_offset3 = -12

# position constants for STATOR
stator1 = SHEIGHT - HTOP1
stator2 = SHEIGHT - HTOP2
stator3 = SHEIGHT - HTOP3 + 12
stator_offset1 = - 5
stator_offset2 = - 7
stator_offset3 = 12

log10 = 1 # math.log(10, 10)


def mark(offset, height3, height2, height1, string=None, flip=False,
         scale=1.0):
    """ Plot marks in a range from 1 to 10 along the length of the slide """
    svg = ''
    scale *= float(SWIDTH - 2 * OFFSET) / SCALE
    if flip:
        ln = float((log10 - offset) * SCALE + OFFSET)
    else:
        ln = offset * SCALE * scale + OFFSET
    if string is not None:
        svg += '  <text style="font-size:12px;fill:#000000;">\n'
        svg += '      <tspan\n'
        svg += '       x="%0.2f"\n' % (ln)
        svg += '       y="%d"\n' % (height3)
        svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%0.1f</tspan></text>\n' % (string)
    svg += '  <path\n'
    svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
    svg += '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
    print svg


def special_mark(offset, height3, height2, height1, string, flip=False,
                 scale=1.0):
    """ Plot special marsk, e.g., e and pi """
    svg = ''
    scale *= float(SWIDTH - 2 * OFFSET) / SCALE
    if flip:
        ln = (log10 - offset) * SCALE * scale + OFFSET
    else:
        ln = offset * SCALE * scale + OFFSET
    svg += '  <text style="font-size:12px;fill:#0000ff;">\n'
    svg += '      <tspan\n'
    svg += '       x="%0.2f"\n' % (ln)
    svg += '       y="%d"\n' % (height3)
    svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>\n' % (string)
    svg += '  <path\n'
    svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
    svg += '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
    print svg


def header(name, x=5):
    """ The SVG header """
    svg = ''
    svg += '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    svg += '<!-- Created with Emacs -->\n'
    svg += '<svg\n'
    svg += '   xmlns:svg="http://www.w3.org/2000/svg"\n'
    svg += '   xmlns="http://www.w3.org/2000/svg"\n'
    svg += '   version="1.0"\n'
    svg += '   width="%s"\n' % (SWIDTH)
    svg += '   height="%s">\n' % (SHEIGHT)
    svg += '  <g>\n'
    svg += '  <path\n'
    svg += '       d="M 0,0 L 0,60 L 2400,60 L 2400,0 Z"\n'
    svg += '       style="fill:#ffffff;stroke:none;stroke-width:0px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
    svg += '  <text style="font-size:12px;fill:#000000;">\n'
    svg += '      <tspan\n'
    svg += '       x="%d"\n' % (x)
    svg += '       y="32"\n'
    svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>' % (name)
    print svg


def footer():
    """ The SVG footer """
    svg = ''
    svg += '  </g>\n'
    svg += '</svg>\n'
    print svg


def make_slide(label, offset_function, label_function, x=None):
    """ Generate marks along a slide using passed functions """

    if x is None:
        header(label)
    else:
        header(label, x)

    for i in range(100, 200):
        if int((i / 10) * 10) == i:
            mark(offset_function(i / 100.), slide3, slide2, slide1,
                 label_function(i / 100.))
        elif int((i / 5) * 5) == i:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset2)

    for i in range(200, 400, 2):
        if int((i / 10) * 10) == i:
            mark(offset_function(i / 100.), slide3, slide2, slide1,
                 label_function(i / 100.))
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    for i in range(400, 1005, 5):
        if int((i / 10)* 10) == i:
            if int((i / 50) * 50) == i:
                mark(offset_function(i / 100.), slide3, slide2, slide1,
                     label_function(i / 100.))
            else:
                mark(offset_function(i / 100.), slide3, slide2, slide1)
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    special_mark(offset_function(math.pi), slide3 + slide_offset3,
                 slide2, slide1, 'π')
    special_mark(offset_function(math.e), slide3 + slide_offset3,
                 slide2, slide1, 'e')

    footer()


def make_stator(label, offset_function, label_function, x=None):
    """ Generate marks along a stator using passed functions """

    if x is None:
        header(label)
    else:
        header(label, x)

    for i in range(100, 200):
        if int((i / 10) * 10) == i:
            mark(offset_function(i / 100.), stator3, stator2, stator1,
                 label_function(i / 100.))
        elif int((i / 5) * 5) == i:
            mark(offset_function(i / 100.), stator3, stator2,
                 stator1 + stator_offset1)
        else:
            mark(offset_function(i / 100.), stator3, stator2,
                 stator1 + stator_offset2)

    for i in range(200, 400, 2):
        if int((i / 10) * 10) == i:
            mark(offset_function(i / 100.), stator3, stator2, stator1,
                 label_function(i / 100.))
        else:
            mark(offset_function(i / 100.), stator3, stator2,
                 stator1 + stator_offset1)

    for i in range(400, 1005, 5):
        if int((i / 10)* 10) == i:
            if int((i / 50) * 50) == i:
                mark(offset_function(i / 100.), stator3, stator2, stator1,
                     label_function(i / 100.))
            else:
                mark(offset_function(i / 100.), stator3, stator2, stator1)
        else:
            mark(offset_function(i / 100.), stator3, stator2,
                 stator1 + stator_offset1)

    special_mark(offset_function(math.pi), stator3 + stator_offset3,
                 stator2, stator1, 'π')
    special_mark(offset_function(math.e), stator3 + stator_offset3,
                 stator2, stator1, 'e')

    footer()


def main():
    """ Log scale for slide (top scale) """

    def offset_function(x):
        return math.log(x, 10)

    def label_function(x):
        return x

    make_slide('C', offset_function, label_function)
    return 0


if __name__ == "__main__":
    main()
