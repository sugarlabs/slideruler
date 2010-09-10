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
from C import header, footer, slide1, slide2, slide3, slide_offset1, \
    slide_offset2, slide_offset3, mark, special_mark
import math


def make_slide(label, offset_function, label_function, x=None):
    """ Generate marks along a slide using passed functions """

    if x is None:
        header(label)
    else:
        header(label, x)

    for i in range(100, 200, 2):
        if int((i / 20) * 20) == i:
            mark(offset_function(i / 100.), slide3, slide2, slide1,
                 label_function(i / 100.))
        elif int((i / 5) * 5) == i:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset2)

    for i in range(200, 400, 4):
        if int((i / 50) * 50) == i:
            mark(offset_function(i / 100.), slide3, slide2, slide1,
                 label_function(i / 100.))
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    for i in range(400, 1000, 10):
        if int((i / 10)* 10) == i:
            if int((i / 100) * 100) == i:
                mark(offset_function(i / 100.), slide3, slide2, slide1,
                     label_function(i / 100.))
            else:
                mark(offset_function(i / 100.), slide3, slide2, slide1)
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    for i in range(1000, 2000, 20):
        if int((i / 200) * 200) == i:
            mark(offset_function(i / 100.), slide3, slide2, slide1,
                 label_function(i / 100.))
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    for i in range(2000, 10050, 100):
        if int((i / 1000) * 1000) == i:
            if int((i / 100) * 100) == i:
                mark(offset_function(i / 100.), slide3, slide2, slide1,
                     label_function(i / 100.))
            else:
                mark(offset_function(i / 100.), slide3, slide2, slide1)
        else:
            mark(offset_function(i / 100.), slide3, slide2,
                 slide1 + slide_offset1)

    for i in range(10000, 101000, 1000):
        if int((i / 2000) * 2000) == i:
            if int((i / 20000) * 20000) == i:
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


def main():
    """ Log^3 scale for slide (top scale) """

    def offset_function(x):
        return math.log(x, 10) / 3.

    def label_function(x):
        return x

    make_slide('K', offset_function, label_function)
    return 0


if __name__ == "__main__":
    main()
