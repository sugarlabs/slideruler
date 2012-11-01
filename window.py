# -*- coding: utf-8 -*-
#Copyright (c) 2009-11 Walter Bender
#Copyright (c) 2012 Ignacio Rodriguez

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
from gi.repository import Gtk, Gdk, GdkPixbuf
from gi.repository import Pango, PangoCairo
import locale
from gettext import gettext as _

from math import *

try:
    from sugar3.graphics import style
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


def _get_screen_dpi():
    xft_dpi = Gtk.Settings.get_default().get_property('gtk-xft-dpi')
    dpi = float(xft_dpi / 1024)
    # HACKITY HACK for XO hardware
    if dpi == 200:
        return 133
    return dpi


class SlideRule():

    def __init__(self, canvas, path, parent=None, sugar=True):
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

        self.sugar = sugar
        self.canvas = canvas
        self.parent = parent
        parent.show_all()

        self.canvas.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.canvas.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.canvas.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.canvas.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.canvas.connect("draw", self.__draw_cb)
        self.canvas.connect("button-press-event", self._button_press_cb)
        self.canvas.connect("button-release-event", self._button_release_cb)
        self.canvas.connect("motion-notify-event", self._mouse_move_cb)
        self.canvas.connect("key-press-event", self._keypress_cb)
        self.canvas.set_can_focus(True)
        self.canvas.grab_focus()
        self.width = Gdk.Screen.width()
        self.height = Gdk.Screen.height() - GRID_CELL_SIZE
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

        self.press = None
        self.last = None
        self.dragpos = 0

        # We need textviews for keyboard input from the on-screen keyboard
        self._set_screen_dpi()
        font_desc = Pango.font_description_from_string('12')
        self.text_entries = []
        self.text_buffers = []

        w = self.reticule.tabs[0].spr.label_safe_width()
        h = int(self.reticule.tabs[0].spr.label_safe_height() / 2)
        for i in range(4):  # Reticule top & bottom; Slider left & right
            self.text_entries.append(Gtk.TextView())
            self.text_entries[-1].set_justification(Gtk.Justification.CENTER)
            self.text_entries[-1].set_pixels_above_lines(4)
            ''' Not necessary (and doesn't work on OS8)
            self.text_entries[-1].override_background_color(
                Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 0, 0))
            '''
            self.text_entries[-1].modify_font(font_desc)
            self.text_buffers.append(self.text_entries[-1].get_buffer())
            self.text_entries[-1].set_size_request(w, h)
            self.text_entries[-1].show()
            self.parent.fixed.put(self.text_entries[-1], 0, 0)
            self.parent.fixed.show()
            self.text_entries[-1].connect('focus-out-event',
                                          self._text_focus_out_cb)
        self.reticule.add_textview(self.text_entries[0], i=BOTTOM)
        self.reticule.add_textview(self.text_entries[1], i=TOP)
        self.reticule.set_fixed(self.parent.fixed)
        for slide in self.slides:
            slide.add_textview(self.text_entries[2], i=LEFT)
            slide.add_textview(self.text_entries[3], i=RIGHT)
            slide.set_fixed(self.parent.fixed)

        if not self.sugar:
            self.update_textview_y_offset(self.parent.menu_height)

        self.active_slide = self.name_to_slide('C')
        self.active_stator = self.name_to_stator('D')
        self.update_slide_labels()
        self.update_result_label()

    def update_textview_y_offset(self, dy):
        ''' Need to account for menu height in GNOME '''
        self.reticule.tabs[0].textview_y_offset += dy
        self.reticule.tabs[1].textview_y_offset += dy
        for slide in self.slides:
            slide.tabs[0].textview_y_offset += dy
            slide.tabs[1].textview_y_offset += dy

    def _text_focus_out_cb(self, widget=None, event=None):
        ''' One of the four textviews was in focus '''
        i = None
        if widget in self.text_entries:
            i = self.text_entries.index(widget)
            bounds = self.text_buffers[i].get_bounds()
            text = self.text_buffers[i].get_text(bounds[0], bounds[1], True)
            text = text.strip()
            self._process_numeric_input(i, text)

    def _set_screen_dpi(self):
        dpi = _get_screen_dpi()
        font_map_default = PangoCairo.font_map_get_default()
        font_map_default.set_resolution(dpi)

    def __draw_cb(self, canvas, cr):
        self.sprites.redraw_sprites(cr=cr)

    # Handle the expose-event by drawing
    def do_expose_event(self, event):

        # Create the cairo context
        cr = self.canvas.window.cairo_create()
        print 'set cr in do_expose'
        self.sprites.set_cairo_context(cr)

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        # Refresh sprite list
        self.sprites.redraw_sprites(cr=cr)

    def _destroy_cb(self, win, event):
        Gtk.main_quit()

    def _keypress_cb(self, area, event):
        """ Keypress: moving the slides with the arrow keys """
        k = Gdk.keyval_name(event.keyval)
        if not self.sugar:
            return
        if k == 'a':
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
                              - self.name_to_stator('D').spr.get_xy()[0])
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

    def _process_numeric_input(self, i, text):
        try:
            n = float(text.replace(self.decimal_point, '.'))
            if i == 0:
                self._move_reticule_to_stator_value(n)                    
            elif i == 1:
                self._move_reticule_to_slide_value(n)
            elif i == 2:
                self._move_slide_to_stator_value(n)
            elif i == 3:
                self._move_slide_to_stator_value(self._left_from_right(n))
        except ValueError:
            self.result_label.spr.labels[0] = _('NaN') + ' ' + text
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
                if self.sugar:
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
                if self.sugar:
                    self.parent.set_stator()
            else:
                self.stators.append(custom_stator)

            self.active_stator = self.name_to_stator(name)

        if self.sugar and name == 'custom' and hasattr(self.parent, 'sr'):
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
        print 'calling active slide', dx, 0
        self.active_slide.move_relative(dx, 0)

    def _move_slides(self, sprite, dx):
        if self.sprite_in_stators(sprite):
            self.active_stator.move_relative(dx, 0)
            self.active_slide.move_relative(dx, 0)
            self.reticule.move_relative(dx, 0)
        elif self.reticule.match(sprite):
            self.reticule.move_relative(dx, 0)
        elif self.sprite_in_slides(sprite):
            self.find_slide(sprite).move_relative(dx, 0)
        self.update_slide_labels()
        self.update_result_label()

    def _left_from_right(self, v_right):
        if self.active_stator.name == 'L2':
            return v_right - 10
        elif self.active_stator.name == 'D':
            return v_right / 10.
        elif self.active_stator.name == 'B':
            return v_right / 100.
        elif self.active_stator.name == 'K2':
            return v_right / 1000.
        elif self.active_stator.name == 'DI':
            return v_right * 10.
        elif self.active_stator.name == 'LLn2':
            return v_right - round(log(10), 2)
        else:
            return v_right
        
    def _right_from_left(self, v_left):
        if self.active_stator.name == 'L2':
            return 10 + v_left
        elif self.active_stator.name == 'D':
            return v_left * 10.
        elif self.active_stator.name == 'B':
            return v_left * 100.
        elif self.active_stator.name == 'K2':
            return v_left * 1000.
        elif self.active_stator.name == 'DI':
            return v_left / 10.
        elif self.active_stator.name == 'LLn2':
            return round(log(10), 2) + v_left
        else:
            return v_left
        
    def update_slide_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        v_left = self.active_stator.calculate()
        v_right = self._right_from_left(v_left)
        label_left = str(v_left).replace('.', self.decimal_point)
        label_right = str(v_right).replace('.', self.decimal_point)
        self.active_slide.label(label_left, i=LEFT)
        self.active_slide.label(label_right, i=RIGHT)
        self.reticule.label(
            str(self.active_stator.result()).replace('.', self.decimal_point),
            i=BOTTOM)
        self.reticule.label(
            str(self.active_slide.calculate()).replace('.', self.decimal_point),
            i=TOP)

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
                elif self.sugar:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'K':
                if self.name_to_slide('K').spr.get_xy()[0] == dx:
                    s = " ∛ %0.2f = %0.2f\t\t%0.2f³ = %0.2f" % (S, R, R, S)
                elif self.sugar:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'S':
                if self.name_to_slide('S').spr.get_xy()[0] == dx:
                    s = " sin(%0.2f) = %0.2f\t\tasin(%0.2f) = %0.2f" % \
                        (S, R/10, R/10, S)
                elif self.sugar:
                    self.parent.set_function_unknown()
            elif self.active_slide.name == 'T':
                if self.name_to_slide('T').spr.get_xy()[0] == dx:
                    s = " tan(%0.2f) = %0.2f\t\tatan(%0.2f) = %0.2f" % \
                        (S, R/10, R/10, S)
                elif self.sugar:
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
            elif self.sugar:
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
