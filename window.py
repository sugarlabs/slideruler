# -*- coding: utf-8 -*-
#Copyright (c) 2009-11 Walter Bender

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

1. In constants.py, you need to add new entries to the arrays that
define the toolbars and slides/stators.

2. In genslides.py, you need to add new class objects to generate the
graphics associated with your slide and stator.

3. In window.py (this file) you need to:
   (a) add the classes you added in Step 2 above to the list of
       methods imported from genslides.
   (b) add your new slide and stator to the SLIDES and STATORS dictionaries.
"""

import pygtk
pygtk.require('2.0')
import gtk

import locale
from gettext import gettext as _

from math import *

try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from constants import SHEIGHT, SWIDTH, SCALE, OFFSET, LEFT, RIGHT, TOP, \
    BOTTOM, SCREENOFFSET, SLIDE, STATOR, DEFINITIONS, FOFFSET, FRESULT, \
    FDISPLAY, FMIN, FMAX, FSTEP
from sprite_factory import Slide, Stator, Reticule, CustomSlide, CustomStator
from sprites import Sprites
from genslides import C_slide_generator, D_stator_generator, \
    CI_slide_generator, DI_stator_generator, A_slide_generator, \
    B_stator_generator, K_slide_generator, K_stator_generator, \
    S_slide_generator, S_stator_generator, T_slide_generator, \
    T_stator_generator, L_slide_generator, L_stator_generator, \
    LLn_slide_generator, LLn_stator_generator, Custom_slide_generator, \
    Custom_stator_generator, Log_slide_generator, Log_stator_generator

import traceback
import logging
_logger = logging.getLogger('sliderule-activity')


class SlideRule():

    def __init__(self, canvas, path, parent=None):
        """ Handle launch from both within and without of Sugar environment. """
        self.SLIDES = {'C':[C_slide_generator], 'CI':[CI_slide_generator],
                       'A':[A_slide_generator], 'K':[K_slide_generator],
                       'S':[S_slide_generator], 'T':[T_slide_generator],
                       'L':[L_slide_generator], 'LLn':[LLn_slide_generator],
                       'Log':[Log_slide_generator],
                       'custom':[Custom_slide_generator]}

        self.STATORS = {'D':[D_stator_generator], 'DI':[DI_stator_generator],
                        'B':[B_stator_generator], 'K2':[K_stator_generator],
                        'S2':[S_stator_generator], 'T2':[T_stator_generator],
                        'L2':[L_stator_generator],
                        'LLn2':[LLn_stator_generator],
                        'Log2':[Log_stator_generator],
                        'custom2':[Custom_stator_generator]}

        self.path = path
        self.activity = parent

        if parent is None:
            self.sugar = False
            self.canvas = canvas
            self.parent = None
        else:
            self.sugar = True
            self.canvas = canvas
            self.parent = parent
            parent.show_all()

        self.canvas.set_flags(gtk.CAN_FOCUS)
        self.canvas.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.canvas.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.canvas.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.canvas.connect("expose-event", self._expose_cb)
        self.canvas.connect("button-press-event", self._button_press_cb)
        self.canvas.connect("button-release-event", self._button_release_cb)
        self.canvas.connect("motion-notify-event", self._mouse_move_cb)
        self.canvas.connect("key_press_event", self._keypress_cb)
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height()-GRID_CELL_SIZE
        self.sprites = Sprites(self.canvas)
        self.slides = []
        self.stators = []
        self.scale = 1

        locale.setlocale(locale.LC_NUMERIC, '')
        self.decimal_point = locale.localeconv()['decimal_point']
        if self.decimal_point == '' or self.decimal_point is None:
            self.decimal_point = '.'

        self.error_msg = None
        self.result_function = [None, None]
        self.label_function = [None, None]

        _logger.debug("creating slides, stators, and reticule")
        self.result_label = Stator(self.sprites, self.path, 'label',
                                        int((self.width - 600) / 2),
                                        SCREENOFFSET + 4 * SHEIGHT,
                                        800, SHEIGHT)

        for slide in self.SLIDES:
            self.make_slide(slide, SLIDE)

        for stator in self.STATORS:
            self.make_slide(stator, STATOR)

        self.reticule = Reticule(self.sprites, self.path, 'reticule',
                          150, SCREENOFFSET + SHEIGHT, 100, 2 * SHEIGHT)
        self.reticule.draw(2000)

        self.active_slide = self.name_to_slide('C')
        self.active_stator = self.name_to_stator('D')

        self.update_slide_labels()
        self.update_result_label()

        self.press = None
        self.last = None
        self.dragpos = 0

    def _expose_cb(self, win, event):
        ''' Callback to handle window expose events '''
        self.do_expose_event(event)
        return True

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.canvas.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        # Refresh sprite list
        self.sprites.redraw_sprites(cr=cr)

    def _destroy_cb(self, win, event):
        gtk.main_quit()

    def _keypress_cb(self, area, event):
        """ Keypress: moving the slides with the arrow keys """
        k = gtk.gdk.keyval_name(event.keyval)
        if self.parent is None:
            return
        if k in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period',
                 'minus', 'Return', 'BackSpace', 'comma']:
            if self.last == self.reticule.tabs[TOP].spr or \
               self.last == self.reticule.tabs[BOTTOM].spr or \
               self.last == self.active_slide.tabs[LEFT].spr:
                self._process_numeric_input(self.last, k)
        elif k == 'a':
            self.parent.show_a()
        elif k == 'k':
            self.parent.show_k()
        elif k in ['c', 'asterisk', 'x']:
            self.parent.show_c()
        elif k in ['i', '/']:
            self.parent.show_ci()
        elif k == 's':
            self.parent.show_s()
        elif k == 't':
            self.parent.show_t()
        elif k in ['l', 'plus']:
            self.parent.show_l()
        elif k in ['Left', 'less']:
            if self.last is not None:
                self._move_slides(self.last, -1)
        elif k in ['Right', 'greater']:
            if self.last is not None:
                self._move_slides(self.last, 1)
        elif k in ['Home', 'Pause', 'Up', '^']:
            self._move_slides(self.name_to_stator('D').spr,
                              -self.name_to_stator('D').spr.get_xy()[0])
        elif k == 'r':
            self.reticule.move(150, self.reticule.spr.get_xy()[1])
            self.update_slide_labels()
            self.update_result_label()
        elif k in ['Down', 'v']:
            self.parent.realign_cb()
            self.reticule.move(150, self.reticule.spr.get_xy()[1])
            self.update_slide_labels()
            self.update_result_label()
        return True

    def _process_numeric_input(self, sprite, keyname):
        ''' Make sure numeric input is valid. '''
        CURSOR = '█'

        oldnum = sprite.labels[0].replace(CURSOR, '')
        newnum = oldnum
        if len(oldnum) == 0:
            oldnum = '0'
        if keyname == 'minus':
            if oldnum == '0':
                newnum = '-'
            elif oldnum[0] != '-':
                newnum = '-' + oldnum
            else:
                newnum = oldnum
        elif keyname == 'comma' and self.decimal_point == ',' and \
                ',' not in oldnum:
            newnum = oldnum + ','
        elif keyname == 'period' and self.decimal_point == '.' and \
                '.' not in oldnum:
            newnum = oldnum + '.'
        elif keyname == 'BackSpace':
            if len(oldnum) > 0:
                newnum = oldnum[:len(oldnum)-1]
            else:
                newnum = ''
        elif keyname in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if oldnum == '0':
                newnum = keyname
            else:
                newnum = oldnum + keyname
        elif keyname == 'Return':
            self.enter_value(sprite, newnum.replace(self.decimal_point, '.'))
            return
        else:
            newnum = oldnum
        if newnum == '.':
            newnum = '0.'
        if len(newnum) > 0 and newnum != '-':
            try:
                float(newnum.replace(self.decimal_point, '.'))
            except ValueError, e:
                newnum = oldnum
        sprite.set_label(newnum + CURSOR)

    def enter_value(self, sprite, value):
        if sprite is None:
            return
        sprite.set_label(value.replace('.', self.decimal_point))
        try:
            if sprite == self.reticule.tabs[TOP].spr:
                self._move_reticule_to_slide_value(
                    float(value.replace(self.decimal_point, '.')))
            elif sprite == self.reticule.tabs[BOTTOM].spr:
                self._move_reticule_to_stator_value(
                    float(value.replace(self.decimal_point, '.')))
            else:
                self._move_slide_to_stator_value(
                    float(value.replace(self.decimal_point, '.')))
        except TypeError:
            sprite.set_label('NaN')
        return

    def _process_text_field(self, text_field):
        """ Process input from numeric text fields: could be a function. """
        try:
            my_min = "def f(): return " + text_field.replace('import','')
            userdefined = {}
            exec my_min in globals(), userdefined
            return userdefined.values()[0]()
        except OverflowError, e:
            self.result_label.spr.labels[0] = _('Overflow Error') + \
                ': ' + str(e)
            self.result_label.draw(1000)
        except NameError, e:
            self.result_label.spr.labels[0] = _('Name Error') + ': ' + str(e)
            self.result_label.draw(1000)
        except ZeroDivisionError, e:
            self.result_label.spr.labels[0] = _('Can not divide by zero') + \
                ': ' + str(e)
            self.result_label.draw(1000)
        except TypeError, e:
            self.result_label.spr.labels[0] = _('Type Error') + ': ' + str(e)
            self.result_label.draw(1000)
        except ValueError, e:
            self.result_label.spr.labels[0] = _('Type Error') + ': ' + str(e)
            self.result_label.draw(1000)
        except SyntaxError, e:
            self.result_label.spr.labels[0] = _('Syntax Error') + ': ' + str(e)
            self.result_label.draw(1000)
        except:
            traceback.print_exc()
        return None

    def make_slide(self, name, slide, custom_strings=None):
        """ Create custom slide and stator from text entered on toolbar. """
        if custom_strings is not None:
            result = self._process_text_field(custom_strings[FMIN])
        else:
            result = self._process_text_field(DEFINITIONS[name][FMIN])
        if result is None:
            return
        try:
            min_value = float(result)
        except ValueError, e:
            self.result_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.result_label.draw(1000)
            return

        if custom_strings is not None:
            result = self._process_text_field(custom_strings[FMAX])
        else:
            result = self._process_text_field(DEFINITIONS[name][FMAX])
        if result is None:
            return
        try:
            max_value = float(result)
        except ValueError:
            self.result_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.result_label.draw(1000)
            return

        if custom_strings is not None:
            result = self._process_text_field(custom_strings[FSTEP])
        else:
            result = self._process_text_field(DEFINITIONS[name][FSTEP])
        if result is None:
            return
        try:
            step_value = float(result)
        except ValueError:
            self.result_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.result_label.draw(1000)
            return

        if custom_strings is not None:
            offset_string = custom_strings[FOFFSET]
        else:
            offset_string = DEFINITIONS[name][FOFFSET]

        if custom_strings is not None:
            label_string = custom_strings[FDISPLAY]
        else:
            label_string = DEFINITIONS[name][FDISPLAY]

        if name == 'custom' or name == 'custom2':
            if custom_strings is not None:
                self.result_function[slide] = custom_strings[FRESULT]
                self.label_function[slide] = custom_strings[FDISPLAY]
            else:
                self.result_function[slide] = DEFINITIONS[name][FRESULT]
                self.label_function[slide] = DEFINITIONS[name][FDISPLAY]

        if slide == SLIDE:
            custom_slide = \
                CustomSlide(self.sprites, self.path, name, 0,
                            SCREENOFFSET + SHEIGHT, self.SLIDES[name][0],
                            self._calc_slide_value, offset_string,
                            label_string, min_value, max_value,
                            step_value)
            if custom_slide.error_msg is not None:
                self.result_label.spr.set_label(custom_slide.error_msg)
                self.result_label.draw(1000)

            if self.name_to_slide(name) is not None and \
               self.name_to_slide(name).name == name:
                i = self.slides.index(self.name_to_slide(name))
                active = False
                if self.active_slide == self.slides[i]:
                    active = True
                self.slides[i].hide()
                self.slides[i] = custom_slide
                if active:
                    self.active_slide = self.slides[i]
                self.parent.set_slide()
            else:
                self.slides.append(custom_slide)

            self.active_slide = self.name_to_slide(name)

        else:
            custom_stator = \
                CustomStator(self.sprites, name, 0,
                             SCREENOFFSET + 2* SHEIGHT, self.STATORS[name][0],
                             self._calc_stator_value, self._calc_stator_result,
                             offset_string, label_string,
                             min_value, max_value, step_value)
            if self.name_to_stator(name) is not None and \
               self.name_to_stator(name).name == name:
                i = self.stators.index(self.name_to_stator(name))
                active = False
                if self.active_stator == self.stators[i]:
                    active = True
                self.stators[i].hide()
                self.stators[i] = custom_stator
                if active:
                    self.active_stator = self.stators[i]
                self.parent.set_stator()
            else:
                self.stators.append(custom_stator)

            self.active_stator = self.name_to_stator(name)

        if name == 'custom' and hasattr(self.parent, 'sr'):
            self.parent.show_u(slide)

        if slide == SLIDE and custom_slide.error_msg is not None:
            self.result_label.spr.set_label(custom_slide.error_msg)
            self.result_label.draw(1000)

        if slide == STATOR and custom_stator.error_msg is not None:
            self.result_label.spr.set_label(custom_stator.error_msg)
            self.result_label.draw(1000)
        
    def name_to_slide(self, name):
        for slide in self.slides:
            if name == slide.name:
                return slide
        return None

    def name_to_stator(self, name):
        for stator in self.stators:
            if name == stator.name:
                return stator
        return None

    def sprite_in_stators(self, sprite):
        for stator in self.stators:
            if stator.match(sprite):
                return True
        return False

    def find_stator(self, sprite):
        for stator in self.stators:
            if stator.match(sprite):
                return stator
        return None

    def sprite_in_slides(self, sprite):
        for slide in self.slides:
            if slide.match(sprite):
                return True
        return False

    def find_slide(self, sprite):
        for slide in self.slides:
            if slide.match(sprite):
                return slide
        return None

    def _button_press_cb(self, win, event):
        win.grab_focus()
        x, y = map(int, event.get_coords())
        self.dragpos = x
        spr = self.sprites.find_sprite((x, y))
        self.press = spr
        return True

    def _mouse_move_cb(self, win, event):
        """ Drag a rule with the mouse. """
        if self.press is None:
            self.dragpos = 0
            return True
        win.grab_focus()
        x, y = map(int, event.get_coords())
        dx = x - self.dragpos
        self._move_slides(self.press, dx)
        self.dragpos = x

    def _move_reticule_to_slide_value(self, value):
        rx = self.reticule.spr.get_xy()[0] - self.active_slide.spr.get_xy()[0]
        self.reticule.move_relative(
            self._calc_dx_from_value(value, self.active_slide.name, rx), 0)
        self.update_slide_labels()
        self.update_result_label()

    def _move_reticule_to_stator_value(self, value):
        rx = self.reticule.spr.get_xy()[0] - self.active_stator.spr.get_xy()[0]
        self.reticule.move_relative(
            self._calc_dx_from_value(value, self.active_stator.name, rx), 0)
        self.update_slide_labels()
        self.update_result_label()

    def _move_slide_to_stator_value(self, value):
        rx = self.active_slide.spr.get_xy()[0] - \
            self.active_stator.spr.get_xy()[0]
        self.active_slide.move_relative(
            self._calc_dx_from_value(value, self.active_stator.name, rx), 0)
        self.update_slide_labels()
        self.update_result_label()

    def _calc_dx_from_value(self, value, name, rx):
        if name in ['C', 'D']:
            if value <= 0:
                return 0
            return log(value, 10) * SCALE - rx
        elif name in ['CI', 'DI']:
            if value == 0:
                return 0
            return log(10/value, 10) * SCALE - rx
        elif name in ['A', 'B']:
            if value <= 0:
                return 0
            return log(pow(value, 1/2.), 10) * SCALE - rx
        elif name in ['K', 'K2']:
            if value <= 0:
                return 0
            return log(pow(value, 1/3.), 10) * SCALE - rx
        elif name in ['L', 'L2']:
            return (value / 10.) * SCALE - rx
        elif name in ['LLn', 'LLn2']:
            return log(exp(value), 10) * SCALE - rx
        elif name in ['Log', 'Log2']:
            return pow(10, log(value, 10)) * SCALE - rx
        else:
            return 0

    def align_slides(self):
        """ Move slide to align with stator """
        slidex = self.active_slide.spr.get_xy()[0]
        statorx = self.active_stator.spr.get_xy()[0]
        dx = statorx - slidex
        self.active_slide.move_relative(dx, 0)

    def _move_slides(self, sprite, dx):
        if self.sprite_in_stators(sprite):
            for slide in self.slides:
                slide.move_relative(dx, 0)
            for stator in self.stators:
                stator.move_relative(dx, 0)
            self.reticule.move_relative(dx, 0)
        elif self.reticule.match(sprite):
            self.reticule.move_relative(dx, 0)
        elif self.sprite_in_slides(sprite):
            self.find_slide(sprite).move_relative(dx, 0)
        self.update_slide_labels()
        self.update_result_label()

    def _update_top(self, function):
        v_left = function()
        if self.active_stator.name == 'L2':
            v_right = 10 + v_left
        elif self.active_stator.name == 'D':
            v_right = v_left * 10.
        elif self.active_stator.name == 'B':
            v_right = v_left * 100.
        elif self.active_stator.name == 'K2':
            v_right = v_left * 1000.
        elif self.active_stator.name == 'DI':
            v_right = v_left / 10.
        elif self.active_stator.name == 'LLn2':
            v_right = round(log(10), 2) + v_left
        else:
            v_right = v_left
        for slide in self.slides:
            slide.tabs[LEFT].spr.set_label(str(v_left).replace('.',
                self.decimal_point))
            slide.tabs[RIGHT].spr.set_label(str(v_right).replace('.',
                self.decimal_point))

    def update_slide_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        self._update_top(self.active_stator.calculate)
        self.reticule.tabs[BOTTOM].spr.set_label(
            str(self.active_stator.result()).replace('.', self.decimal_point))
        self.reticule.tabs[TOP].spr.set_label(
            str(self.active_slide.calculate()).replace('.', self.decimal_point))

    def _button_release_cb(self, win, event):
        if self.press == None:
            return True
        if self.press == self.active_slide.spr:
            self.last = self.active_slide.tabs[LEFT].spr
        elif self.press == self.active_stator.spr:
            self.last = None
        else:
            self.last = self.press
        self.press = None
        self.update_result_label()

    def update_result_label(self):
        """ Update toolbar label with result of calculation. """
        s = ''
        if self.active_stator.name == 'D':
            dx = self.name_to_stator('D').spr.get_xy()[0]
            S = self.active_slide.calculate()
            R = self._calc_stator_result('D')
            if self.active_slide.name == 'A':
                if self.name_to_slide('A').spr.get_xy()[0] == dx:
                    s = " √ %0.2f = %0.2f\t\t%0.2f² = %0.2f" % (S, R, R, S)
                elif self.parent is not None:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'K':
                if self.name_to_slide('K').spr.get_xy()[0] == dx:
                    s = " ∛ %0.2f = %0.2f\t\t%0.2f³ = %0.2f" % (S, R, R, S)
                elif self.parent is not None:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'S':
                if self.name_to_slide('S').spr.get_xy()[0] == dx:
                    s = " sin(%0.2f) = %0.2f\t\tasin(%0.2f) = %0.2f" % \
                        (S, R/10, R/10, S)
                elif self.parent is not None:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'T':
                if self.name_to_slide('T').spr.get_xy()[0] == dx:
                    s = " tan(%0.2f) = %0.2f\t\tatan(%0.2f) = %0.2f" % \
                        (S, R/10, R/10, S)
                elif self.parent is not None:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'C':
                D = str(self._calc_stator_value('D'))
                s = "%s × %s = %s\t\t%s / %s = %s" % (D, S, R, R, S, D)
            elif self.active_slide.name == 'CI':
                D = str(self._calc_stator_value('D'))
                s = "%s / %s = %s\t\t%s × %s = %s" % (D, S, R/10, R/10, S, D)
        elif self.active_stator.name == 'L2':
            if self.active_slide.name == 'L':
                # use n dash to display a minus sign
                L2 = self._calc_stator_value('L2')
                if L2 < 0:
                    L2str = "–" + str(-L2)
                else:
                    L2str = str(L2)

                L = self._calc_slide_value('L')
                if L < 0:
                    operator1 = "–"
                    operator2 = "+"
                    Lstr = str(-L)
                else:
                    operator1 = "+"
                    operator2 = "–"
                    Lstr = str(L)

                LL = self._calc_stator_result('L2')
                if LL < 0:
                    LLstr = "–" + str(-LL)
                else:
                    LLstr = str(LL)

                s = "%s %s %s = %s\t\t%s %s %s = %s" % (L2str, operator1, Lstr,
                                                        LLstr, LLstr,
                                                        operator2, Lstr, L2str)
        elif self.active_stator.name == 'LLn2' and \
             self.active_slide.name == 'C':
            dx = self.name_to_stator('LLn2').spr.get_xy()[0]
            S = self.active_slide.calculate()
            R = self._calc_stator_result('LLn2')
            if self.name_to_slide('C').spr.get_xy()[0] == dx:
                s = " ln(%0.2f) = %0.2f\t\texp(%0.2f) = %0.2f" % (S, R, R, S)
            elif self.parent is not None:
                self.parent.set_function_unknown()

        if self.active_slide.name == 'custom' or \
           self.active_stator.name == 'custom2':
            if self.error_msg is not None:
                s = self.error_msg
            else:
                s = ''
            self.result_label.draw(1000)

        self.result_label.spr.set_label(s.replace('.', self.decimal_point))

    def _top_slide_offset(self, x):
        """ Calcualate the offset between the top and bottom slides """
        x2, y2 = self.active_slide.spr.get_xy()
        return x2 - x

    # Calculate the value of individual slides and stators:
    # (a) the offset of the reticule along the slide
    # (b) the offset of the slide along the stator
    # (c) the offset of the reticule along the reticule

    def _r_offset(self, slide):
        return self.reticule.spr.get_xy()[0] - slide.spr.get_xy()[0]

    def _calc_slide_value(self, name=None):
        if name is None:
            name = self.active_slide.name
        return self.function_calc(name, self._r_offset(
                self.name_to_slide(name)), SLIDE)

    def _calc_stator_value(self, name=None):
        if name is None:
            name = self.active_stator.name
        return self.function_calc(name, self._top_slide_offset(
                self.name_to_stator(name).spr.get_xy()[0]), STATOR)

    def _calc_stator_result(self, name=None):
        if name is None:
            name = self.active_stator.name
        return self.function_calc(name, self._r_offset(
                self.name_to_stator(name)), STATOR)

    def function_calc(self, name, dx, slide):
        self.error_msg = None
        
        if name in ['custom', 'custom2']:
            my_result = "def f(x): return " + \
                self.result_function[slide].replace('import','')
            my_label = "def f(x): return " + \
                self.label_function[slide].replace('import','')
        else:
            my_result = "def f(x): return " + DEFINITIONS[name][FRESULT]
            my_label = "def f(x): return " + DEFINITIONS[name][FDISPLAY]

        # Some slides handle wrap-around
        rescale = 1
        offset = 0
        if name in ['C', 'D', 'CI', 'DI', 'LLn', 'LLn2', 'Log', 'Log2']:
            if dx < 0:
                rescale = 0.1
                dx += SCALE
        elif name in ['A', 'B']:
            if dx < 0:
                rescale = 0.01
                dx += SCALE
        elif name in ['K', 'K2']:
            if dx < 0:
                rescale = 0.001
                dx += SCALE
        elif name in ['L', 'L2']:
            rescale = 10
            if dx < 0:
                dx += SCALE
                offset = -10

        userdefined = {}
        try:
            exec my_result in globals(), userdefined
            result = userdefined.values()[0](float(dx) / SCALE) * rescale +\
                offset
        except OverflowError, e:
            self.error_msg = _('Overflow Error') + ': ' + str(e)
            return '?'
        except NameError, e:
            self.error_msg = _('Name Error') + ': ' + str(e)
            return '?'
        except ZeroDivisionError, e:
            self.error_msg = _('Can not divide by zero') + ': ' + str(e)
            return '?'
        except TypeError, e:
            self.error_msg = _('Type Error') + ': ' + str(e)
            return '?'
        except ValueError, e:
            self.error_msg = _('Type Error') + ': ' + str(e)
            return '?'
        except SyntaxError, e:
            self.error_msg = _('Syntax Error') + ': ' + str(e)
            return '?'
        except:
            traceback.print_exc()
            return None

        # Some special cases to fine-tune the label display precision
        precision = 2
        if name in ['A', 'B', 'K', 'K2']:
            if result > 50:
                precision = 1
        elif name in ['S', 'S2']:
            if result > 60:
                precision = 1
        if name in ['K', 'K2']:
            if result > 500:
                precision = 0

        userdefined = {}
        try:
            exec my_label in globals(), userdefined
            label = userdefined.values()[0](result)
            if type(label) == float:
                return round(label, precision)
            else:
                return label
        except OverflowError, e:
            self.error_msg = _('Overflow Error') + ': ' + str(e)
        except NameError, e:
            self.error_msg = _('Name Error') + ': ' + str(e)
        except ZeroDivisionError, e:
            self.error_msg = _('Can not divide by zero') + ': ' + str(e)
        except TypeError, e:
            self.error_msg = _('Type Error') + ': ' + str(e)
        except ValueError, e:
            self.error_msg = _('Type Error') + ': ' + str(e)
        except SyntaxError, e:
            self.error_msg = _('Syntax Error') + ': ' + str(e)
        except:
            traceback.print_exc()
            return None

        return '??'
