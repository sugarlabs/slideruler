# -*- coding: utf-8 -*-
#Copyright (c) 2009,10 Walter Bender

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
from C import header, footer, stator1, stator2, stator3, stator_offset1, \
    stator_offset2, stator_offset3
import math


def mark(offset, height3, height2, height1, string=None, flip=False,
         scale=1.0):
    """ Plot marks in a range from 1 to 10 along the length of the stator """
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
        svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%d</tspan></text>\n' % (int(string))
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
    svg += '  <path'
    svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
    svg += '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
    print svg


def make_stator(label, offset_function, label_function, x=None):
    """ Generate marks along a stator using passed functions """

    if x is None:
        header(label)
    else:
        header(label, x)

    for i in range(23, 64):
        if int((i / 4) * 4) == i:
            mark(offset_function(i / 4.), stator3, stator2, stator1,
                 label_function(i / 4.))
            if int((i / 8) * 8) == i:
                special_mark(offset_function(i / 4.), stator3 + stator_offset3,
                             stator2, stator1,
                             str(int(label_function(180 - i / 4.))))
        else:
            mark(offset_function(i / 4.), stator3, stator2,
                 stator1 + stator_offset2)

    for i in range(32, 64):
        if int((i / 4) * 4) == i:
            mark(offset_function(i / 2.), stator3, stator2, stator1,
                 label_function(i / 2.))
            if int((i / 8) * 8) == i:
                special_mark(offset_function(i / 2.), stator3 + stator_offset3,
                             stator2, stator1,
                             str(int(label_function(180 - i / 2.))))
        else:
            mark(offset_function(i / 2.), stator3, stator2,
                 stator1 + stator_offset2)

    for i in range(64, 120, 2):
        if int((i / 4) * 4) == i:
            mark(offset_function(i / 2.), stator3, stator2, stator1,
                 label_function(i / 2.))
            if int((i / 8) * 8) == i:
                special_mark(offset_function(i / 2.), stator3 + stator_offset3,
                             stator2, stator1,
                             str(int(label_function(180 - i / 2.))))
        else:
            mark(offset_function(i / 2.), stator3, stator2,
                 stator1 + stator_offset2)

    for i in range(120, 160, 5):
        if int((i / 10) * 10) == i:
            mark(offset_function(i / 2.), stator3, stator2, stator1,
                 label_function(i / 2.))
            if int((i / 20) * 20) == i:
                special_mark(offset_function(i / 2.), stator3 + stator_offset3,
                             stator2, stator1,
                             str(int(label_function(180 - i / 2.))))
        else:
            mark(offset_function(i / 2.), stator3, stator2,
                 stator1 + stator_offset2)

    for i in range(160, 190, 10):
        if int((i / 20) * 20) == i:
            mark(offset_function(i / 2.), stator3, stator2, stator1,
                 label_function(i / 2.))
        else:
            mark(offset_function(i / 2.), stator3, stator2,
                 stator1 + stator_offset2)

    footer()


def main():
    """ Sine scale for stator (bottom scale) """

    def offset_function(x):
        return math.log(10 * math.sin(float(x) * math.pi / 180.), 10)

    def label_function(x):
        return x

    make_stator('S', offset_function, label_function)
    return 0


if __name__ == "__main__":
    main()
