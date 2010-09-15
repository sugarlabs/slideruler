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

import pygtk
pygtk.require('2.0')
import gtk

from gettext import gettext as _

from math import *

try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from constants import SHEIGHT, SWIDTH, SCALE, OFFSET, LEFT, RIGHT, TOP, \
    BOTTOM, SCREENOFFSET, SLIDE, STATOR, CUSTOM
from sprite_factory import Slide, Stator, Reticule, CustomSlide, CustomStator
from sprites import Sprites
from genslides import C_slide, D_stator, CI_slide, DI_stator, A_slide, \
    A_stator, K_slide, K_stator, S_slide, S_stator, T_slide, T_stator, \
    L_slide, L_stator, LL0_slide, LL0_stator, LLn_slide, LLn_stator, \
    Custom_slide, Custom_stator, Log_slide, Log_stator

import traceback
import logging
_logger = logging.getLogger('sliderule-activity')


def round(x, precision=2):
    if precision == 2:
        return(float(int(x * 100 + 0.5) / 100.))
    elif precision == 1:
        return(float(int(x * 10 + 0.5) / 10.))
    elif precision == 0:
        return(int(x + 0.5))
    else:
        y = pow(10, precision)
        return(float(int(x * y + 0.5) / y))


def _calc_log(dx):
    """ C and D scales """
    rescale = 1
    if dx < 0:
        rescale = 0.1
        dx += SCALE
    return round(pow(10, float(dx) / SCALE) * rescale)


def _calc_inverse_log(dx):
    """ CI and DI scales """
    rescale = 1
    if dx < 0:
        rescale = 0.1
        dx += SCALE
    return round(10.0 / pow(10, float(dx) / SCALE) * rescale)


def _calc_log_squared(dx):
    """ A and B scales """
    rescale = 1
    if dx < 0:
        dx += SCALE
        rescale = 0.01
    A = pow(10, 2 * float(dx) / SCALE) * rescale
    if A > 50:
        return round(A, 1)
    else:
        return round(A)


def _calc_log_cubed(dx):
    """ K scale """
    rescale = 1
    if dx < 0:
        rescale = 0.001
        dx += SCALE
    K = pow(10, 3 * float(dx) / SCALE) * rescale
    if K > 500:
        return round(K, 0)
    elif K > 50:
        return round(K, 1)
    else:
        return round(K)


def _calc_log_log(dx):
    """ LL0 scale """
    rescale = 1.0
    if dx < 0:
        rescale = 0.1
        dx += SCALE
    Log = log(pow(10, (float(dx) / SCALE) * rescale), 10)
    return round(Log)


def _calc_ln_log(dx):
    """ LL0 scale """
    rescale = 1.0
    if dx < 0:
        rescale = 0.1
        dx += SCALE
    LL0 = exp(pow(10, (float(dx) / SCALE) * rescale) / 1000)
    if LL0 > 1.002:
        return round(LL0, 5)
    else:
        return round(LL0, 6)


def _calc_linear(dx):
    """ L scale """
    if dx < 0:
        dx += SCALE
        return round(10 * (float(dx) / SCALE) - 10.0)
    else:
        return round(10 * (float(dx) / SCALE))


def _calc_sine(dx):
    """ S scale """
    s = pow(10, float(dx) / SCALE) / 10
    if s > 1.0:
        s = 1.0
    S = 180.0 * asin(s) / pi
    if S > 60:
        return round(S, 1)
    else:
        return round(S)


def _calc_tangent(dx):
    """ T scale """
    t = pow(10, float(dx) / SCALE) / 10
    if t > 1.0:
        t = 1.0
    return round(180.0 * atan(t) / pi)


def _calc_ln(dx):
    rescale = 1
    if dx < 0:
        rescale = 0.1
        dx += SCALE
    return round(log((pow(10, float(dx) / SCALE) * rescale)))


class SlideRule():

    def __init__(self, canvas, path, parent=None):
        """ Handle launch from both within and without of Sugar environment. """
        SLIDES = {'C':[C_slide, self._calc_C], 'CI':[CI_slide, self._calc_CI],
                  'A':[A_slide, self._calc_A], 'K':[K_slide, self._calc_K],
                  'S':[S_slide, self._calc_S], 'T':[T_slide, self._calc_T],
                  'L':[L_slide, self._calc_L],
                  'LLn':[LLn_slide, self._calc_LLn],
                  'Log':[Log_slide, self._calc_Log]}
        # 'LL0':[LL0_slide, self._calc_LL0],

        STATORS = {'D':[D_stator, self._calc_D, self._calc_D_result],
                   'DI':[DI_stator, self._calc_DI, self._calc_DI_result],
                   'B':[A_stator, self._calc_B, self._calc_B_result],
                   'K2':[K_stator, self._calc_K2, self._calc_K2_result],
                   'S2':[S_stator, self._calc_S2, self._calc_S2_result],
                   'T2':[T_stator, self._calc_T2, self._calc_T2_result],
                   'L2':[L_stator, self._calc_L2, self._calc_L2_result],
                   'LLn2':[LLn_stator, self._calc_LLn2, self._calc_LLn2_result],
                   'Log2':[Log_stator, self._calc_Log2, self._calc_Log2_result]}
        # 'LL02':[LL0_stator, self._calc_LL02, self._calc_LL02_result],

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

        self.error_msg = None
        self.results_function = [None, None]
        self.results_label_function = [None, None]

        _logger.debug("creating slides, stators, and reticule")
        self.results_label = Stator(self.sprites, self.path, 'label',
                                        int((self.width - 600) / 2),
                                        SCREENOFFSET + 4 * SHEIGHT,
                                        800, SHEIGHT)

        for slide in SLIDES:
            self.slides.append(self._make_slide(slide, SCREENOFFSET + SHEIGHT,
                SLIDES[slide][0], SLIDES[slide][1]))

        for stator in STATORS:
            self.stators.append(self._make_stator(stator,
                                                  SCREENOFFSET + 2 * SHEIGHT,
                STATORS[stator][0], STATORS[stator][1], STATORS[stator][2]))

        self.make_custom_slide(CUSTOM['C'][0], CUSTOM['C'][1], CUSTOM['C'][2],
                               CUSTOM['C'][3], CUSTOM['C'][4], CUSTOM['C'][5],
                               CUSTOM['C'][6], SLIDE)
        self.make_custom_slide(CUSTOM['D'][0], CUSTOM['D'][1], CUSTOM['D'][2],
                               CUSTOM['D'][3], CUSTOM['D'][4], CUSTOM['D'][5],
                               CUSTOM['D'][6], STATOR)

        self.reticule = Reticule(self.sprites, self.path, 'reticule',
                          150, SCREENOFFSET + SHEIGHT, 100, 2 * SHEIGHT)
        self.reticule.draw(2000)

        self.active_slide = self.name_to_slide('C')
        self.active_stator = self.name_to_stator('D')

        self.update_slide_labels()
        self.update_results_label()

        self.press = None
        self.last = None
        self.dragpos = 0

    def _expose_cb(self, win, event):
        # self.sprite_list.refresh(event)
        self.sprites.redraw_sprites()
        return True

    def _destroy_cb(self, win, event):
        gtk.main_quit()

    def _keypress_cb(self, area, event):
        """ Keypress: moving the slides with the arrow keys """
        k = gtk.gdk.keyval_name(event.keyval)
        if self.parent is None:
            return
        if k in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period',
                 'minus', 'Return', 'BackSpace']:
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
            self.update_results_label()
        elif k in ['Down', 'v']:
            self.parent.realign_cb()
            self.reticule.move(150, self.reticule.spr.get_xy()[1])
            self.update_slide_labels()
            self.update_results_label()
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
        elif keyname == 'period' and '.' not in oldnum:
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
            sprite.set_label(newnum)
            try:
                if sprite == self.reticule.tabs[TOP].spr:
                    self._move_reticule_to_slide_value(float(newnum))
                elif sprite == self.reticule.tabs[BOTTOM].spr:
                    self._move_reticule_to_stator_value(float(newnum))
                else:
                    self._move_slide_to_stator_value(float(newnum))
            except TypeError:
                sprite.set_label('NaN')
            return
        else:
            newnum = oldnum
        if newnum == '.':
            newnum = '0.'
        if len(newnum) > 0 and newnum != '-':
            try:
                float(newnum)
            except ValueError, e:
                newnum = oldnum
        sprite.set_label(newnum + CURSOR)

    def _make_slide(self, name, y, svg_engine, calculate=None):
        slide = Slide(self.sprites, self.path, name, 0, y, SWIDTH, SHEIGHT,
                      svg_engine, calculate)
        slide.spr.set_label('')
        slide.draw()
        return slide

    def _make_stator(self, name, y, svg_engine, calculate=None, result=None):
        stator = Stator(self.sprites, None, name, 0, y, SWIDTH, SHEIGHT,
                        svg_engine, calculate, result)
        stator.spr.set_label('')
        stator.draw()
        return stator

    def _process_text_field(self, text_field):
        """ Process input from numeric text fields: could be a function. """
        try:
            my_min = "def f(): return " + text_field.replace('import','')
            userdefined = {}
            exec my_min in globals(), userdefined
            return userdefined.values()[0]()
        except OverflowError, e:
            self.results_label.spr.labels[0] = _('Overflow Error') + \
                ': ' + str(e)
            self.results_label.draw(1000)
        except NameError, e:
            self.results_label.spr.labels[0] = _('Name Error') + ': ' + str(e)
            self.results_label.draw(1000)
        except ZeroDivisionError, e:
            self.results_label.spr.labels[0] = _('Zero-division Error') + \
                ': ' + str(e)
            self.results_label.draw(1000)
        except TypeError, e:
            self.results_label.spr.labels[0] = _('Type Error') + ': ' + str(e)
            self.results_label.draw(1000)
        except ValueError, e:
            self.results_label.spr.labels[0] = _('Type Error') + ': ' + str(e)
            self.results_label.draw(1000)
        except SyntaxError, e:
            self.results_label.spr.labels[0] = _('Syntax Error') + ': ' + str(e)
            self.results_label.draw(1000)
        except:
            traceback.print_exc()
        return None

    def make_custom_slide(self, offset_text, label_text, results_function,
                          results_label, min_text, max_text, step_text, slide):
        """ Create custom slide and stator from text entered on toolbar. """

        results = self._process_text_field(min_text)
        if results is None:
            return
        try:
            min_value = float(results)
        except ValueError, e:
            self.results_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.results_label.draw(1000)
            return

        results = self._process_text_field(max_text)
        if results is None:
            return
        try:
            max_value = float(results)
        except ValueError:
            self.results_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.results_label.draw(1000)
            return

        results = self._process_text_field(step_text)
        if results is None:
            return
        try:
            step_value = float(results)
        except ValueError:
            self.results_label.spr.labels[0] = _('Value Error') + ': ' + str(e)
            self.results_label.draw(1000)
            return

        def custom_offset_function(x):
            my_offset = "def f(x): return " + offset_text.replace('import','')
            userdefined = {}
            exec my_offset in globals(), userdefined
            return userdefined.values()[0](x)

        def custom_label_function(x):
            my_label = "def f(x): return " + label_text.replace('import','')
            userdefined = {}
            exec my_label in globals(), userdefined
            return userdefined.values()[0](x)

        self.results_function[slide] = results_function
        self.results_label_function[slide] = results_label

        if slide == SLIDE:
            custom_slide = CustomSlide(self.sprites, self.path, 'custom',
                                       0, SCREENOFFSET + SHEIGHT, Custom_slide,
                                       self._calc_custom,
                                       custom_offset_function,
                                       custom_label_function,
                                       min_value, max_value, step_value)
            if custom_slide.error_msg is not None:
                self.results_label.spr.set_label(custom_slide.error_msg)
                self.results_label.draw(1000)

            if self.name_to_slide('custom').name == 'custom':
                i = self.slides.index(self.name_to_slide('custom'))
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

            self.active_slide = self.name_to_slide('custom')

        else:
            custom_stator = CustomStator(self.sprites, 'custom2',
                                         0, SCREENOFFSET + 2* SHEIGHT,
                                         Custom_stator,
                                         self._calc_custom2,
                                         self._calc_custom2_result,
                                         custom_offset_function,
                                         custom_label_function,
                                         min_value, max_value, step_value)
            if self.name_to_stator('custom2').name == 'custom2':
                i = self.stators.index(self.name_to_stator('custom2'))
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

            self.active_stator = self.name_to_stator('custom2')

        if hasattr(self.parent, 'sr'):
            self.parent.show_u(slide)

        if slide == SLIDE and custom_slide.error_msg is not None:
            self.results_label.spr.set_label(custom_slide.error_msg)
            self.results_label.draw(1000)

        if slide == STATOR and custom_stator.error_msg is not None:
            self.results_label.spr.set_label(custom_stator.error_msg)
            self.results_label.draw(1000)
        
    def name_to_slide(self, name):
        for slide in self.slides:
            if name == slide.name:
                return slide
        return self.slides[0]

    def name_to_stator(self, name):
        for stator in self.stators:
            if name == stator.name:
                return stator
        return self.stators[0]

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
        self.update_results_label()

    def _move_reticule_to_stator_value(self, value):
        rx = self.reticule.spr.get_xy()[0] - self.active_stator.spr.get_xy()[0]
        self.reticule.move_relative(
            self._calc_dx_from_value(value, self.active_stator.name, rx), 0)
        self.update_slide_labels()
        self.update_results_label()

    def _move_slide_to_stator_value(self, value):
        rx = self.active_slide.spr.get_xy()[0] - \
            self.active_stator.spr.get_xy()[0]
        self.active_slide.move_relative(
            self._calc_dx_from_value(value, self.active_stator.name, rx), 0)
        self.update_slide_labels()
        self.update_results_label()

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
        self.update_results_label()

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
            v_right = round(log(10)) + v_left
        else:
            v_right = v_left
        for slide in self.slides:
            slide.tabs[LEFT].spr.set_label(str(v_left))
            slide.tabs[RIGHT].spr.set_label(str(v_right))

    def update_slide_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        self._update_top(self.active_stator.calculate)
        self.reticule.tabs[BOTTOM].spr.set_label(
                str(self.active_stator.result()))
        self.reticule.tabs[TOP].spr.set_label(
            str(self.active_slide.calculate()))

    def _button_release_cb(self, win, event):
        if self.press == None:
            return True
        self.last = self.press
        self.press = None
        self.update_results_label()

    def update_results_label(self):
        """ Update toolbar label with results of calculation. """
        s = ''
        if self.active_stator.name == 'D':
            dx = self.name_to_stator('D').spr.get_xy()[0]
            S = self.active_slide.calculate()
            R = self._calc_D_result()
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
                D = str(self._calc_D())
                s = "%s × %s = %s\t\t%s / %s = %s" % (D, S, R, R, S, D)
            elif self.active_slide.name == 'CI':
                D = str(self._calc_D())
                s = "%s / %s = %s\t\t%s × %s = %s" % (D, S, R/10, R/10, S, D)
        elif self.active_stator.name == 'L2':
            if self.active_slide.name == 'L':
                # use n dash to display a minus sign
                L2 = self._calc_L2()
                if L2 < 0:
                    L2str = "–" + str(-L2)
                else:
                    L2str = str(L2)

                L = self._calc_L()
                if L < 0:
                    operator1 = "–"
                    operator2 = "+"
                    Lstr = str(-L)
                else:
                    operator1 = "+"
                    operator2 = "–"
                    Lstr = str(L)

                LL = self._calc_L2_result()
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
            R = self._calc_LLn2_result()
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
            self.results_label.draw(1000)

        self.results_label.spr.set_label(s)

    def _top_slide_offset(self, x):
        """ Calcualate the offset between the top and bottom slides """
        x2, y2 = self.active_slide.spr.get_xy()
        return x2 - x

    # Calculate the value of individual slides and stators

    def _r_offset(self, slide):
        return self.reticule.spr.get_xy()[0] - slide.spr.get_xy()[0]

    def _calc_C(self):
        return _calc_log(self._r_offset(self.name_to_slide('C')))
        
    def _calc_D(self):
        return _calc_log(self._top_slide_offset(
                self.name_to_stator('D').spr.get_xy()[0]))

    def _calc_D_result(self):
        return _calc_log(self._r_offset(self.name_to_stator('D')))

    def _calc_CI(self):
        return _calc_inverse_log(self._r_offset(self.name_to_slide('CI')))

    def _calc_DI(self):
        return _calc_inverse_log(
            self._top_slide_offset(self.name_to_stator('DI').spr.get_xy()[0]))

    def _calc_DI_result(self):
        return _calc_inverse_log(self._r_offset(self.name_to_stator('DI')))

    def _calc_LLn(self):
        return _calc_ln(self._r_offset(self.name_to_slide('LLn')))

    def _calc_LLn2(self):
        return _calc_ln(self._top_slide_offset(
                self.name_to_stator('LLn2').spr.get_xy()[0]))

    def _calc_LLn2_result(self):
        return _calc_ln(self._r_offset(self.name_to_stator('D')))

    def _calc_Log(self):
        return _calc_log_log(self._r_offset(self.name_to_slide('Log')))

    def _calc_Log2(self):
        return _calc_log_log(self._top_slide_offset(
                self.name_to_stator('Log2').spr.get_xy()[0]))

    def _calc_Log2_result(self):
        return _calc_log_log(self._r_offset(self.name_to_stator('D')))

    def _calc_LL0(self):
        return _calc_ln_log(self._r_offset(self.name_to_slide('LL0')))

    def _calc_LL02(self):
        return _calc_ln_log(self._top_slide_offset(
                self.name_to_stator('LL02').spr.get_xy()[0]))

    def _calc_LL02_result(self):
        return _calc_ln_log(self._r_offset(self.name_to_stator('D')))

    def _calc_A(self):
        return _calc_log_squared(self._r_offset(self.name_to_slide('A')))

    def _calc_B(self):
         return _calc_log_squared(
             self._top_slide_offset(self.name_to_stator('B').spr.get_xy()[0]))

    def _calc_B_result(self):
         return _calc_log_squared(self._r_offset(self.name_to_stator('B')))

    def _calc_S(self):
        return _calc_sine(self._r_offset(self.name_to_slide('S')))

    def _calc_S2(self):
        return _calc_sine(self._top_slide_offset(
                self.name_to_stator('S2').spr.get_xy()[0]))

    def _calc_S2_result(self):
        return _calc_sine(self._r_offset(self.name_to_stator('S2')))

    def _calc_T(self):
        return _calc_tangent(self._r_offset(self.name_to_slide('T')))

    def _calc_T2(self):
        return _calc_tangent(self._top_slide_offset(
                self.name_to_stator('T2').spr.get_xy()[0]))

    def _calc_T2_result(self):
        return _calc_tangent(self._r_offset(self.name_to_stator('T2')))

    def _calc_K(self):
        return _calc_log_cubed(self._r_offset(self.name_to_slide('K')))

    def _calc_K2(self):
        return _calc_log_cubed(self._top_slide_offset(
                self.name_to_stator('K2').spr.get_xy()[0]))

    def _calc_K2_result(self):
        return _calc_log_cubed(self._r_offset(self.name_to_stator('K2')))

    def _calc_L(self):
        return _calc_linear(self._r_offset(self.name_to_slide('L')))

    def _calc_L2(self):
        return _calc_linear(self._top_slide_offset(
                self.name_to_stator('L2').spr.get_xy()[0]))

    def _calc_L2_result(self):
        return _calc_linear(self._r_offset(self.name_to_stator('L2')))

    def _calc_custom(self):
        return self.custom_calc(self._r_offset(self.name_to_slide('custom')),
                                SLIDE)

    def _calc_custom2(self):
        return self.custom_calc(self._top_slide_offset(
                self.name_to_stator('custom2').spr.get_xy()[0]), STATOR)

    def _calc_custom2_result(self):
        return self.custom_calc(self._r_offset(self.name_to_stator('custom2')),
                                STATOR)

    def custom_calc(self, dx, slide):
        self.error_msg = None
        my_results = "def f(x): return " + \
            self.results_function[slide].replace('import','')
        my_label = "def f(x): return " + \
            self.results_label_function[slide].replace('import','')

        userdefined = {}
        try:
            exec my_results in globals(), userdefined
            results = round(userdefined.values()[0](float(dx) / SCALE))
        except OverflowError, e:
            self.error_msg = _('Overflow Error') + ': ' + str(e)
            return '?'
        except NameError, e:
            self.error_msg = _('Name Error') + ': ' + str(e)
            return '?'
        except ZeroDivisionError, e:
            self.error_msg = _('Zero-division Error') + ': ' + str(e)
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

        userdefined = {}
        try:
            exec my_label in globals(), userdefined
            return userdefined.values()[0](results)
        except OverflowError, e:
            self.error_msg = _('Overflow Error') + ': ' + str(e)
        except NameError, e:
            self.error_msg = _('Name Error') + ': ' + str(e)
        except ZeroDivisionError, e:
            self.error_msg = _('Zero-division Error') + ': ' + str(e)
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
