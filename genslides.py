# -*- coding: utf-8 -*-
#Copyright (c) 2009, 2010 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""
Modifying slide rule:

The customization feature is intended to handle most cases where you require
a specialized slide or stator. But if you would like to add a new slide to
the toolbar, you need to make changes in three places:

1. In SlideruleActivity.py, you need to add new entries to the arrays that
define the toolbars.

2. In genslides.py (this file), you need to add new class objects to
generate the graphics associated with your slide and stator. In most
cases, you can simply inherit from the C_slide and C_stator classes.
The make_slide() method iterates across the domain of the offset_function().

NOTE that most of the make_slide() methods ignore min, max, and step.

3. In window.py, you need to add methods to calculate values for your
slide and stator.

"""

from math import *

import traceback

from gettext import gettext as _

from constants import SWIDTH, SHEIGHT, OFFSET, SCALE, HTOP1, HTOP2, HTOP3


class C_slide_generator():
    """ Log scale for slide """
    def __init__(self, name, offset_text, label_text, min, max, step):
        self.name = name
        self.offset_text = offset_text.replace('import','')
        self.label_text = label_text.replace('import','')
        self.min = min
        self.max = max
        self.step = step
        self.error_msg = None
        self.precision = 1

        self.setup_svg()

        def offset_function(x):
            my_offset = "def f(x): return " + self.offset_text
            userdefined = {}
            exec my_offset in globals(), userdefined
            return userdefined.values()[0](x)

        def label_function(x):
            my_label = "def f(x): return " + self.label_text
            userdefined = {}
            exec my_label in globals(), userdefined
            return userdefined.values()[0](x)

        self.svg = self.make_slide(self.name, offset_function, label_function,
                                   self.min, self.max, self.step)

    def setup_svg(self):
        self.setup_slide()

    def setup_slide(self):
        self.slide1 = HTOP1
        self.slide2 = HTOP2
        self.slide3 = HTOP3
        self.slide_offset1 = 5
        self.slide_offset2 = 7
        self.slide_offset3 = -12

    def setup_stator(self):
        self.slide1 = SHEIGHT - HTOP1
        self.slide2 = SHEIGHT - HTOP2
        self.slide3 = SHEIGHT - HTOP3 + 12
        self.slide_offset1 = - 5
        self.slide_offset2 = - 7
        self.slide_offset3 = 12

    def mark(self, offset, height3, height2, height1, value=None):
        """ Plot marks in a range from 1 to 10 along the length of the slide """
        svg = ''
        log = offset * SCALE + OFFSET
        if value is not None:
            if type(value) == str:
                string = value
            else:
                format = '%0.' + str(self.precision) + 'f'
                string = format % (value)
            svg += '  <text style="font-size:12px;fill:#000000;">\n'
            svg += '      <tspan\n'
            svg += '       x="%0.2f"\n' % (log)
            svg += '       y="%d"\n' % (height3)
            svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (log, height1, log, height2)
        svg += '       style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def special_mark(self, offset, height3, height2, height1, value):
        """ Plot special marks, e.g., e and pi """
        if type(value) == str:
            string = value
        else:
            format = '%0.' + str(self.precision) + 'f'
            string = format % (value)
        svg = ''
        log = offset * SCALE + OFFSET
        svg += '  <text style="font-size:12px;fill:#0000ff;">\n'
        svg += '      <tspan\n'
        svg += '       x="%0.2f"\n' % (log)
        svg += '       y="%d"\n' % (height3)
        svg += '       style="font-size:12px;text-align:center;text-anchor:middle;font-family:Bitstream Vera Sans;">%s</tspan></text>\n' % (string)
        svg += '  <path\n'
        svg += '       d="M %0.2f,%d,%0.2f,%d"\n' % (log, height1, log, height2)
        svg += '       style="fill:none;stroke:#0000ff;stroke-width:1px;stroke-linecap:square;stroke-linejoin:miter;stroke-opacity:1" />\n'
        return svg

    def header(self, name):
        """ The SVG header """
        if name == 'custom' or name == 'custom2':
            name = 'XO'
        x = len(name)*5

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

    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(100, 200):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(200, 400, 2):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(400, 1005, 5):
            if int((i / 10)* 10) == i:
                if int((i / 50) * 50) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        svg += self.special_mark(offset_function(pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π')
        svg += self.special_mark(offset_function(e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e')

        svg += self.footer()
        return svg


class D_stator_generator(C_slide_generator):
    """ Log scale for stator """
    def setup_svg(self):
        self.setup_stator()


class CI_slide_generator(C_slide_generator):
    """ Inverse Log scale for slide """


class DI_stator_generator(D_stator_generator):
    """ Inverse Log scale for stator """


class A_slide_generator(C_slide_generator):
    """ Log^2 scale for slide """
    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(100, 200):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(200, 400, 2):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(400, 1000, 5):
            if int((i / 10)* 10) == i:
                if int((i / 100) * 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(1000, 2000, 10):
            if int((i / 200)* 200) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(2000, 10050, 50):
            if int((i / 1000)* 1000) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        svg += self.special_mark(offset_function(pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π')
        svg += self.special_mark(offset_function(e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e')

        svg += self.footer()
        return svg


class B_stator_generator(A_slide_generator):
    """ Log^2 scale for slide """
    def setup_svg(self):
        self.setup_stator()


class K_slide_generator(C_slide_generator):
    """ Log^3 scale for slide """
    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(100, 200, 2):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(200, 400, 4):
            if int((i / 50) * 50) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(400, 1000, 10):
            if int((i / 20)* 20) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(1000, 2000, 20):
            if int((i / 200)* 200) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(2000, 10050, 100):
            if int((i / 1000)* 1000) == i:
                if int((i / 100)* 100) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        for i in range(11000, 101000, 1000):
            if int((i / 2000)* 2000) == i:
                if int((i / 20000)* 20000) == i:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1,
                                     label_function(i / 100.))
                else:
                    svg += self.mark(offset_function(i / 100.), self.slide3,
                                     self.slide2, self.slide1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)

        svg += self.special_mark(offset_function(pi),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π')
        svg += self.special_mark(offset_function(e),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e')

        svg += self.footer()
        return svg


class K_stator_generator(K_slide_generator):
    """ Log^3 scale for slide """
    def setup_svg(self):
        self.setup_stator()


class S_slide_generator(C_slide_generator):
    """ Sine scale for slide """
    def setup_svg(self):
        self.precision = 0
        self.setup_slide()

    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        svg += self.mark(0, self.slide3, self.slide2, self.slide1)

        for i in range(24, 64):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 4.))
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 4.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             str(int(label_function(180 - i / 4.))))
            else:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(32, 64):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.))
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             str(int(label_function(180 - i / 2.))))
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(64, 120, 2):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.))
                if int((i / 8) * 8) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             str(int(label_function(180 - i / 2.))))
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(120, 160, 5):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.))
                if int((i / 20) * 20) == i:
                    svg += self.special_mark(offset_function(i / 2.),
                                             self.slide3 + self.slide_offset3,
                                             self.slide2, self.slide1,
                                             str(int(label_function(180 - i / 2.))))
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        for i in range(160, 190, 10):
            if int((i / 20) * 20) == i:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 2.))
            else:
                svg += self.mark(offset_function(i / 2.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        svg += self.footer()
        return svg


class S_stator_generator(S_slide_generator):
    """ Sine scale for slide """
    def setup_svg(self):
        self.precision = 0
        self.setup_stator()


class T_slide_generator(S_slide_generator):
    """ Tangent scale for slide """
    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        svg += self.mark(0, self.slide3, self.slide2, self.slide1)

        for i in range(23, 181):
            if int((i / 4) * 4) == i:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 4.))
            else:
                svg += self.mark(offset_function(i / 4.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        svg += self.footer()
        return svg


class T_stator_generator(T_slide_generator):
    """ Tangent scale for slide """
    def setup_svg(self):
        self.setup_stator()


class L_slide_generator(C_slide_generator):
    """ Linear scale for slide """
    def make_slide(self, label, offset_function, label_function, min, max, 
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(0, 101):
            if int((i / 10) * 10) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i / 10.))
            elif int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset1)
            else:
                svg += self.mark(offset_function(i / 100.), self.slide3,
                                 self.slide2,
                                 self.slide1 + self.slide_offset2)

        svg += self.special_mark(offset_function(pi / 10.),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'π')
        svg += self.special_mark(offset_function(e / 10.),
                                 self.slide3 + self.slide_offset3, self.slide2,
                                 self.slide1, 'e')

        svg += self.footer()
        return svg


class L_stator_generator(L_slide_generator):
    """ Linear scale for slide """
    def setup_svg(self):
        self.setup_stator()


# TODO: use definition from CUSTOM array
class LLn_slide_generator(C_slide_generator):
    """ Ln scale for slide """
    def __init__(self, name, offset_text, label_text, min, max, step):
        self.name = name
        self.offset_text = offset_text.replace('import','')
        self.label_text = label_text.replace('import','')
        self.error_msg = None
        self.precision = 2

        self.setup_slide()

        def offset_function(x):
            return x

        def label_function(x):
            return x * log(10) / 100

        self.svg = self.make_slide(self.name, offset_function, label_function)

    def make_slide(self, label, offset_function, label_function):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(0, int(100 * log(10)) + 1):
            if int((i / 5) * 5) == i:
                svg += self.mark(offset_function(i / (100. * log(10))),
                                 self.slide3, self.slide2, self.slide1,
                                 label_function(i / log(10)))
            else:
                svg += self.mark(offset_function(i / (100. * log(10))),
                                 self.slide3, self.slide2,
                                 self.slide1 + self.slide_offset2)

        svg += self.mark(offset_function(1),
                         self.slide3, self.slide2,
                         self.slide1 + self.slide_offset2)

        svg += self.footer()
        return svg


class LLn_stator_generator(LLn_slide_generator):
    """ Ln scale for slide """
    def __init__(self, name, offset_text, label_text, min, max, step):
        self.name = name
        self.offset_text = offset_text.replace('import','')
        self.label_text = label_text.replace('import','')
        self.error_msg = None
        self.precision = 2

        self.setup_stator()

        def offset_function(x):
            return x

        def label_function(x):
            return x * log(10) / 100

        self.svg = self.make_slide(self.name, offset_function, label_function)


class Log_slide_generator(C_slide_generator):
    """ Ln scale for slide """
    def setup_svg(self):
        self.precision = 2
        self.setup_slide()

    def make_slide(self, label, offset_function, label_function, min, max,
                   step):
        """ Generate marks along a slide using passed functions """

        svg = ''
        svg += self.header(label)

        for i in range(100, 1010, 10):
            if int((i / 50) * 50) == i:
                svg += self.mark(offset_function(i / 100.),
                                 self.slide3, self.slide2, self.slide1,
                                 label_function(i / 100.))
            else:
                svg += self.mark(offset_function(i / 100.),
                                 self.slide3, self.slide2,
                                 self.slide1 + self.slide_offset2)

        svg += self.footer()
        return svg


class Log_stator_generator(Log_slide_generator):
    """ Log log scale for slide """
    def setup_svg(self):
        self.precision = 2
        self.setup_stator()


class Custom_slide_generator(C_slide_generator):
    """ User-defined scale for slide """
    def setup_svg(self):
        self.precision = 2
        self.setup_slide()

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
            try:
                svg += self.mark(offset_function(i), self.slide3,
                                 self.slide2, self.slide1,
                                 label_function(i))
            except OverflowError, e:
                self.error_msg = _('Overflow Error') + ': ' + str(e)
            except NameError, e:
                self.error_msg = _('Name Error') + ': ' + str(e)
            except ZeroDivisionError, e:
                self.error_msg = _('Zero Division Error') + ' ' + str(e)
            except TypeError, e:
                self.error_msg = _('Type Error') + ': ' + str(e)
            except ValueError, e:
                self.error_msg = _('Value Error') + ': ' + str(e)
            except SyntaxError, e:
                self.error_msg = _('Syntax Error') + ': ' + str(e)
            except:
                traceback.print_exc()
            i += step

        svg += self.footer()
        return svg


class Custom_stator_generator(Custom_slide_generator):
    """ user-defined scale for slide """
    def setup_svg(self):
        self.precision = 2
        self.setup_stator()


def main():
    """ Log scale for slide and stator """

    print C_slide().svg
    return 0


if __name__ == "__main__":
    main()
