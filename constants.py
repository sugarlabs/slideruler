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

OFFSET = 50
SWIDTH = 2400
SHEIGHT = 60
SCALE = SWIDTH - 2 * OFFSET
TABWIDTH = 100
SCREENOFFSET = 50

HTOP1 = 38
HTOP2 = 59
HTOP3 = 35

LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1

SLIDE = 0
STATOR = 1

CUSTOM = {'C': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1'],
          'D': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1'],
          'CI': ['log(10/x,10)', '10/pow(10,x)', 'x', '1', '10', '1'],
          'DI': ['log(10/x,10)', '10/pow(10,x)', 'x', '1', '10', '1'],
          'L': ['x', 'x', 'x', '0', '1', '0.05'],
          'L2': ['x', 'x', 'x', '0', '1', '0.05'],
          'A': ['log(x,10)/2', 'pow(10,x*2)', 'x', '1', '100', '9'],
          'A2': ['log(x,10)/2', 'pow(10,x*2)', 'x', '1', '100', '9'],
          'K': ['log(x,10)/3', 'pow(10,x*3)', 'x', '1', '1000', '99'],
          'K2': ['log(x,10)/3', 'pow(10,x*3)', 'x', '1', '1000', '99'],
          'S': ['log(sin(x*pi/180)*10,10)', 'asin(pow(10,x)/10)*180/pi',
                'x', '5', '90', '5'],
          'S2': ['log(sin(x*pi/180)*10,10)', 'asin(pow(10,x)/10)*180/pi',
                 'x', '5', '90', '5'],
          'T': ['log(tan(x*pi/180)*10,10)', 'atan(pow(10,x)/10)*180/pi',
                'x', '5', '45', '2.5'],
          'T2': ['log(tan(x*pi/180)*10,10)', 'atan(pow(10,x)/10)*180/pi',
                 'x', '5', '45', '2.5'],
          'Log': ['log(x,10)', 'pow(10,x)', 'round(log(x,10),2)',
                  '1', '10', '1'],
          'Log2': ['log(x,10)','pow(10,x)', 'round(log(x,10),2)',
                   '1', '10', '1'],
          'Ln': ['log(x,10)', 'pow(10,x)', 'round(log(x),2)', '1', '10', '1'],
          'Ln2': ['log(x,10)','pow(10,x)', 'round(log(x),2)', '1', '10', '1']}
