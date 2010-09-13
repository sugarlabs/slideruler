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

log10 = 1 # math.log(10, 10)


class C_slide():
    """ Log scale for slide """
    def __init__(self):
        self.name = 'C'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)

    def mark(self, offset, height3, height2, height1, string=None, flip=False,
             scale=1.0):
        """ Plot marks in a range from 1 to 10 along the length of the slide """
        svg = ''
        if flip:
            log = (log10 - offset) * SCALE * scale + OFFSET
        else:
            log = offset * SCALE * scale + OFFSET
        if string is not None:
            svg += '  <text style="font-size:12px;fill:#000000;">\n'
            svg += '      <tspan\n'
            svg += '       x="%0.2f"\n' % (log)
            svg += '       y="%d"\n' % (height3)
            svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%0.1f</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (log, height1, log, height2)
        svg += '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def special_mark(self, offset, height3, height2, height1, string,
                     flip=False, scale=1.0):
        """ Plot special marks, e.g., e and pi """
        svg = ''
        if flip:
            log = (log10 - offset) * SCALE * scale + OFFSET
        else:
            log = offset * SCALE * scale + OFFSET
        svg += '  <text style="font-size:12px;fill:#0000ff;">\n'
        svg += '      <tspan\n'
        svg += '       x="%0.2f"\n' % (log)
        svg += '       y="%d"\n' % (height3)
        svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (log, height1, log, height2)
        svg += '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def header(self, name, x=5):
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
        return svg

    def footer(self):
        """ The SVG footer """
        svg = ''
        svg += '  </g>\n'
        svg += '</svg>\n'
        return svg

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(100, 200):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(200, 400, 2):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(400, 1005, 5):
            if int((i / 10)* 10) == i:
                if int((i / 50) * 50) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1, flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        svg += self.special_mark(offset_function(math.pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π', flip=flip_flag)
        svg += self.special_mark(offset_function(math.e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e', flip=flip_flag)

        svg += self.footer()
        return svg


class D_stator(C_slide):
    """ Log scale for stator """
    def __init__(self):
        self.name = 'D'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class CI_slide(C_slide):
    """ Inverse Log scale for slide """
    def __init__(self):
        self.name = 'CI'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   flip_flag=True)


class DI_stator(D_stator):
    """ Inverse Log scale for stator """
    def __init__(self):
        self.name = 'DI'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   flip_flag=True)


class A_slide(C_slide):
    """ Log^2 scale for slide """
    def __init__(self):
        self.name = 'A'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10) / 2.

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(100, 200):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(200, 400, 2):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(400, 1000, 5):
            if int((i / 10)* 10) == i:
                if int((i / 100) * 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1, flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(1000, 2000, 10):
            if int((i / 200)* 200) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(2000, 10050, 50):
            if int((i / 1000)* 1000) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        svg += self.special_mark(offset_function(math.pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π', flip=flip_flag)
        svg += self.special_mark(offset_function(math.e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e', flip=flip_flag)

        svg += self.footer()
        return svg


class A_stator(A_slide):
    """ Log^2 scale for slide """
    def __init__(self):
        self.name = 'A'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10) / 2.

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class K_slide(C_slide):
    """ Log^3 scale for slide """
    def __init__(self):
        self.name = 'K'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10) / 3.

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(100, 200, 2):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(200, 400, 4):
            if int((i / 50) * 50) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(400, 1000, 10):
            if int((i / 20)* 20) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1, flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(1000, 2000, 20):
            if int((i / 200)* 200) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(2000, 10050, 100):
            if int((i / 1000)* 1000) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        for i in range(11000, 101000, 1000):
            if int((i / 2000)* 2000) == i:
                if int((i / 20000)* 20000) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.), flip=flip_flag)
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)

        svg += self.special_mark(offset_function(math.pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π', flip=flip_flag)
        svg += self.special_mark(offset_function(math.e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e', flip=flip_flag)

        svg += self.footer()
        return svg


class K_stator(K_slide):
    """ Log^3 scale for slide """
    def __init__(self):
        self.name = 'K'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10) / 3.

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class S_slide(C_slide):
    """ Sine scale for slide """
    def __init__(self):
        self.name = 'S'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(10 * math.sin(float(x) * math.pi / 180.), 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)

    def mark(self, offset, height3, height2, height1, string=None, flip=False,
             scale=1.0):
        """ Plot marks in a range from 1 to 10 along the length of the slide """
        svg = ''
        if flip:
            ln = (log10 - offset) * SCALE * scale + OFFSET
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
        return svg

    def special_mark(self, offset, height3, height2, height1, string,
                     flip=False, scale=1.0):
        """ Plot special marks, e.g., e and pi """
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
        svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%d</tspan></text>\n' % (int(string))
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
        svg += '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        svg += self.mark(0, self.slide3, self.slide2, self.slide1,
                         flip=flip_flag)

        for i in range(24, 64):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 4.), flip=flip_flag)
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 4.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             label_function(180 - i / 4.),
                                             flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(32, 64):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.), flip=flip_flag)
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             label_function(180 - i / 2.),
                                             flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(64, 120, 2):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.), flip=flip_flag)
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             label_function(180 - i / 2.),
                                             flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(120, 160, 5):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.), flip=flip_flag)
                if int((i / 20) * 20) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             label_function(180 - i / 2.),
                                             flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(160, 190, 10):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        svg += self.footer()
        return svg


class S_stator(S_slide):
    """ Sine scale for slide """
    def __init__(self):
        self.name = 'S'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(10 * math.sin(float(x) * math.pi / 180.), 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class T_slide(S_slide):
    """ Tangent scale for slide """
    def __init__(self):
        self.name = 'T'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(10 * math.tan(float(x) * math.pi / 180.), 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        svg += self.mark(0, self.slide3, self.slide2, self.slide1,
                         flip=flip_flag)

        for i in range(23, 181):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 4.), flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        svg += self.footer()
        return svg


class T_stator(T_slide):
    """ Tangent scale for slide """
    def __init__(self):
        self.name = 'T'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(10 * math.tan(float(x) * math.pi / 180.), 10)

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class L_slide(C_slide):
    """ Linear scale for slide """
    def __init__(self):
        self.name = 'L'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return x

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(0, 101):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 10.), flip=flip_flag)
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        svg += self.special_mark(offset_function(math.pi / 10.),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π', flip=flip_flag)
        svg += self.special_mark(offset_function(math.e / 10.),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e', flip=flip_flag)

        svg += self.footer()
        return svg


class L_stator(L_slide):
    """ Linear scale for slide """
    def __init__(self):
        self.name = 'L'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return x

        def label_function(x):
            return x

        self.svg = self.make_slide(self.name, offset_function, label_function)


class LL0_slide(C_slide):
    """ Log Log scale for slide """
    def __init__(self):
        self.name = 'LL0'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return math.exp(x / 1000.)

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)

    def mark(self, offset, height3, height2, height1, string=None, flip=False,
             scale=1.0):
        """ Plot marks in a range from 1 to 10 along the length of the slide """
        svg = ''
        if flip:
            ln = (log10 - offset) * SCALE * scale + OFFSET
        else:
            ln = offset * SCALE * scale + OFFSET
        if string is not None:
            svg += '  <text style="font-size:12px;fill:#000000;">\n'
            svg += '      <tspan\n'
            svg += '       x="%0.2f"\n' % (ln)
            svg += '       y="%d"\n' % (height3)
            svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%0.4f</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
        svg += '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(100, 200):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(200, 400, 2):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        for i in range(400, 1005, 5):
            if int((i / 50) * 50) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.), flip=flip_flag)
            elif int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1,
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)


        svg += self.footer()
        return svg


class LL0_stator(LL0_slide):
    """ Log Log scale for slide """
    def __init__(self):
        self.name = 'LL0'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return math.pow(10, x / 1000.)

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)


class LLn_slide(C_slide):
    """ Ln scale for slide """
    def __init__(self):
        self.name = 'LLn'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return x

        def label_function(x):
            return x * math.log(10) / 100

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)

    def mark(self, offset, height3, height2, height1, string=None, flip=False,
             scale=1.0):
        """ Plot marks in a range from 1 to 10 along the length of the slide """
        svg = ''
        scale *= float(SWIDTH - 2 * OFFSET) / SCALE
        if flip:
            ln = (log10 - offset) * SCALE * scale + OFFSET
        else:
            ln = offset * SCALE * scale + OFFSET
        if string is not None:
            svg += '  <text style="font-size:12px;fill:#000000;">\n'
            svg += '      <tspan\n'
            svg += '       x="%0.2f"\n' % (ln)
            svg += '       y="%d"\n' % (height3)
            svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%0.2f</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (ln, height1, ln, height2)
        svg += '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(0, int(100 * math.log(10)) + 1):
            if int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / (100. * math.log(10))),
                                 self.slide3, self.slide2, self.slide1,
                                 label_function(i / math.log(10)),
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / (100. * math.log(10))),
                                 self.slide3, self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        svg += self.mark(offset_function(1),
                         self.slide3, self.slide2,
                         self.slide1 + self.slide_offset2,
                         flip=flip_flag)

        svg += self.footer()
        return svg


class LLn_stator(LLn_slide):
    """ Ln scale for slide """
    def __init__(self):
        self.name = 'LLn'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return x

        def label_function(x):
            return x * math.log(10) / 100

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)


class Log_slide(LLn_slide):
    """ Ln scale for slide """
    def __init__(self):
        self.name = 'Log'
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return math.log(x, 10)

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)

    def make_slide(self, label, offset_function, label_function, x=None,
                   flip_flag=False):
        """ Generate marks along a slide using passed functions """

        svg = ''
        if x is None:
            svg += self.header(label)
        else:
            svg += self.header(label, x)

        for i in range(100, 1010, 10):
            if int((i / 50) * 50) == i:
                svg += self.mark(offset_function(i / 100.),
                                 self.slide3, self.slide2, self.slide1,
                                 label_function(i / 100.),
                                 flip=flip_flag)
            else:
                svg += self.mark(offset_function(i / 100.),
                                 self.slide3, self.slide2,
                                 self.slide1 + self.slide_offset2,
                                 flip=flip_flag)

        svg += self.footer()
        return svg


class Log_stator(Log_slide):
    """ Log log scale for slide """
    def __init__(self):
        self.name = 'Log'
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        def offset_function(x):
            return math.log(x, 10)

        def label_function(x):
            return math.log(x, 10)

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   x=10)


class Custom_slide(C_slide):
    """ User-defined scale for slide """
    def __init__(self, offset_function, label_function, min, max, step):
        self.name = ''
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   min, max, step)

    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        # TODO: more sophisticated bounds-checking
        if step == 0:
            step = 1
        if  step < 0:
            step = -step
        if min > max:
            i = max
            max = min
            min = i
        else:
            i = min
        while i < max + step:
            svg += self.mark(offset_function(i), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i))
            i += step

        svg += self.footer()
        return svg


class Custom_stator(Custom_slide):
    """ user-defined scale for slide """
    def __init__(self, offset_function, label_function, min, max, step):
        self.name = ''
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   min, max, step)


def main():
    """ Log scale for slide and stator """

    print C_slide().svg
    return 0


if __name__ == "__main__":
    main()
