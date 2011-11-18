# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA

"""
Modifying slide rule:

The customization feature is intended to handle most cases where you require
a specialized slide or stator. But if you would like to add a new slide to
the toolbar, you need to make changes in three places:

1. In constants.py (this file) you need to add new entries to SLIDE_TABLE,
STATOR_TABLE, SLIDE_DICTIONARY, STATOR_DICTIONARY, and DEFINITIONS so that the
slides appear in the toolbars.

2. In genslides.py, you need to add new class objects to generate the
graphics associated with your slide and stator.

3. In window.py, you need to import the new class objects from #2.
"""

from gettext import gettext as _

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

A_slide = _('log²')
B_slide = A_slide
C_slide = _('log')
D_slide = C_slide
CI_slide = _('1/log')
DI_slide = CI_slide
K_slide = _('log³')
S_slide = _('sin')
T_slide = _('tan')
L_slide = _('linear')
Log_slide = _('log log')
LLn_slide = _('ln')
UD_slide = _('user defined')

SLIDE_TABLE = [L_slide, C_slide, CI_slide, A_slide, K_slide, S_slide, T_slide,
               Log_slide, LLn_slide, UD_slide]

STATOR_TABLE = [L_slide, D_slide, DI_slide, B_slide, K_slide, S_slide, T_slide,
                Log_slide, LLn_slide, UD_slide]

SLIDE_DICTIONARY = {C_slide: 'C', CI_slide: 'CI', A_slide: 'A', K_slide: 'K',
                    S_slide: 'S', T_slide: 'T', L_slide: 'L', Log_slide: 'Log',
                    LLn_slide: 'LLn', UD_slide: 'custom'}

STATOR_DICTIONARY = {D_slide: 'D', DI_slide: 'DI', L_slide: 'L2', B_slide: 'B',
                     K_slide: 'K2', S_slide: 'S2', T_slide: 'T2',
                     Log_slide: 'Log2', LLn_slide: 'LLn2', UD_slide: 'custom2'}

FOFFSET = 0
FRESULT = 1
FDISPLAY = 2
FMIN = 3
FMAX = 4
FSTEP = 5
DEFINITIONS = {'C': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1'],
               'D': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1'],
               'CI': ['log(10/x,10)', '10/pow(10,x)', 'x', '1', '10', '1'],
               'DI': ['log(10/x,10)', '10/pow(10,x)', 'x', '1', '10', '1'],
               'L': ['x', 'x', 'x', '0', '1', '0.05'],
               'L2': ['x', 'x', 'x', '0', '1', '0.05'],
               'A': ['log(x,10)/2', 'pow(10,x*2)', 'x', '1', '100', '9'],
               'B': ['log(x,10)/2', 'pow(10,x*2)', 'x', '1', '100', '9'],
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
               'LLn': ['log(x,10)', 'pow(10,x)', 'round(log(x),2)', '1', '10',
                       '1'],
               'LLn2': ['log(x,10)','pow(10,x)', 'round(log(x),2)', '1', '10',
                        '1'],
               'custom': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1'],
               'custom2': ['log(x,10)', 'pow(10,x)', 'x', '1', '10', '1']}

