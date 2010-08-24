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

from constants import *

import pygtk
pygtk.require('2.0')
import gtk
from gettext import gettext as _
import math

try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from sprite_factory import *
from sprites import *


class SlideRule():

    def __init__(self, canvas, path, parent=None):
        """ Handle launch from both within and without of Sugar environment. """
        self.path = path
        self.activity = parent

        # starting from command line
        # we have to do all the work that was done in CardSortActivity.py
        if parent is None:
            self.sugar = False
            self.canvas = canvas

        # starting from Sugar
        else:
            self.sugar = True
            self.canvas = canvas
            parent.show_all()

        self.canvas.set_flags(gtk.CAN_FOCUS)
        self.canvas.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.canvas.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.canvas.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.canvas.connect("expose-event", self._expose_cb)
        self.canvas.connect("button-press-event", self._button_press_cb)
        self.canvas.connect("button-release-event", self._button_release_cb)
        self.canvas.connect("motion-notify-event", self._mouse_move_cb)
        self.width = gtk.gdk.screen_width()
        self.height = gtk.gdk.screen_height()-GRID_CELL_SIZE
        self.sprites = Sprites(self.canvas)
        self.scale = 1

        # Open the sliders
        y = 50
        self.A = Slider(self.sprites, self.path, 'A',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.C = Slider(self.sprites, self.path, 'C',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.CI = Slider(self.sprites, self.path, 'CI',
                         0, y + 60, SWIDTH, SHEIGHT)
        self.L = Slider(self.sprites, self.path, 'L',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.L2 = Slider(self.sprites, self.path, 'L2',
                         0, y + 60, SWIDTH, SHEIGHT)
        self.D = Slider(self.sprites, self.path, 'D',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.C_tab_left = Slider(self.sprites, self.path, 'tab',
                                 0, y + 3 * SHEIGHT, 100, SHEIGHT, False)
        self.C_tab_right = Slider(self.sprites, self.path, 'tab',
                                  SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT,
                                  False)
        self.CI_tab_left = Slider(self.sprites, self.path, 'tab',
                                  0, y + 3 * SHEIGHT, 100, SHEIGHT, False)
        self.CI_tab_right = Slider(self.sprites, self.path, 'tab',
                                   SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT,
                                   False)
        self.L2_tab_left = Slider(self.sprites, self.path, 'tab',
                                  0, y + 3 * SHEIGHT, 100, SHEIGHT, False)
        self.L2_tab_right = Slider(self.sprites, self.path, 'tab',
                                   SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT,
                                   False)
        self.R = Slider(self.sprites, self.path, 'reticule',
                        0, y + SHEIGHT, 100, 2 * SHEIGHT, False)
        self.R_tab_top = Slider(self.sprites, self.path, 'tab',
                                0, y, 100, 60, False)
        self.R_tab_bot = Slider(self.sprites, self.path, 'tab',
                                0, y + 3 * SHEIGHT, 100, SHEIGHT, False)
        self.slider_on_top = 'C'

        self.R.spr.set_label('')
        self.A.spr.set_label('')
        self.C.spr.set_label('')
        self.CI.spr.set_label('')
        self.D.spr.set_label('')
        self.L.spr.set_label('')
        self.L2.spr.set_label('')
        self.update_slider_labels()
        self.update_results_label()

        self.A.draw_slider(500)
        self.C.draw_slider()
        self.C_tab_left.draw_slider()
        self.C_tab_right.draw_slider()
        self.CI.draw_slider()
        self.CI_tab_left.draw_slider()
        self.CI_tab_right.draw_slider()
        self.D.draw_slider()
        self.R_tab_bot.draw_slider()
        self.R_tab_top.draw_slider()
        self.R.draw_slider(2000)
        self.L.draw_slider()
        self.L2.draw_slider()
        self.L2_tab_left.draw_slider()
        self.L2_tab_right.draw_slider()

        # Start calculating
        self.factor = 1
        self.press = None
        self.dragpos = 0

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
        # redicule doesn't use offset
        dx = x - self.dragpos
        if self.press == self.D.spr or self.press == self.A.spr:
            # everything moves
            self.C.spr.move_relative((dx, 0))
            self.C_tab_left.spr.move_relative((dx, 0))
            self.C_tab_right.spr.move_relative((dx, 0))
            self.CI.spr.move_relative((dx, 0))
            self.CI_tab_left.spr.move_relative((dx, 0))
            self.CI_tab_right.spr.move_relative((dx, 0))
            self.A.spr.move_relative((dx, 0))
            self.D.spr.move_relative((dx, 0))
            self.R_tab_top.spr.move_relative((dx, 0))
            self.R_tab_bot.spr.move_relative((dx, 0))
            self.R.spr.move_relative((dx, 0))
        elif self.press == self.R_tab_top.spr or \
             self.press == self.R_tab_bot.spr or \
             self.press == self.R.spr:
            self.R_tab_top.spr.move_relative((dx, 0))
            self.R_tab_bot.spr.move_relative((dx, 0))
            self.R.spr.move_relative((dx, 0))
        elif self.press == self.C.spr or \
             self.press == self.C_tab_left.spr or \
             self.press == self.C_tab_right.spr:
            self.C.spr.move_relative((dx, 0))
            self.C_tab_left.spr.move_relative((dx, 0))
            self.C_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.CI.spr:
            self.CI.spr.move_relative((dx, 0))
            self.CI_tab_left.spr.move_relative((dx, 0))
            self.CI_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.L.spr:
            self.L.spr.move_relative((dx, 0))
            self.L2.spr.move_relative((dx, 0))
            self.L2_tab_left.spr.move_relative((dx, 0))
            self.L2_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.L2.spr or \
             self.press == self.L2_tab_left.spr or \
             self.press == self.L2_tab_right.spr:
            self.L2.spr.move_relative((dx, 0))
            self.L2_tab_left.spr.move_relative((dx, 0))
            self.L2_tab_right.spr.move_relative((dx, 0))

        # reset drag position
        self.dragpos = x
        self.update_slider_labels()
        self.update_results_label()

    def update_slider_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        self.C_tab_left.spr.set_label(str(self._calc_D()))
        self.C_tab_right.spr.set_label(str(self._calc_D()))
        self.CI_tab_left.spr.set_label(str(self._calc_D()))
        self.CI_tab_right.spr.set_label(str(self._calc_D()))
        self.L2_tab_left.spr.set_label(str(self._calc_L()))
        self.L2_tab_right.spr.set_label(str(self._calc_L()))
        if self.slider_on_top == 'A':
            self.R_tab_top.spr.set_label(str(self._calc_A()))
            self.R_tab_bot.spr.set_label(str(self._calc_DA()))
        elif self.slider_on_top == 'L':
            self.R_tab_top.spr.set_label(str(self._calc_L2()))
            self.R_tab_bot.spr.set_label(str(self._calc_LL()))
        elif self.slider_on_top == 'CI':
            self.R_tab_top.spr.set_label(str(self._calc_CI()))
            self.R_tab_bot.spr.set_label(str(self._calc_DC()))
        else:
            self.R_tab_top.spr.set_label(str(self._calc_C()))
            self.R_tab_bot.spr.set_label(str(self._calc_DC()))
        return True

    def _button_release_cb(self, win, event):
        if self.press == None:
            return True
        self.press = None
        self.update_results_label()

    def update_results_label(self):
        """ Update toolbar label. """
        if self.slider_on_top == 'A':
            # calculate the values for D, A, and D * A (under the redicule)
            s = " √ " + str(self._calc_A()) + " = " + \
                str(self._calc_DA() * self.factor)
        elif self.slider_on_top == 'L':
            # calculate the values for L2, L, and L2 + L (under the redicule)
            if self._calc_L() < 0:
                s = str(self._calc_L2()) + " – " + str(-self._calc_L()) + \
                    " = " + str(self._calc_LL())
            else:
                s = str(self._calc_L2()) + " + " + str(self._calc_L()) + \
                    " = " + str(self._calc_LL())
        elif self.slider_on_top == 'CI':
            # calculate the values for D, CI, and D / CI (under the redicule)
            s = str(self._calc_D()) + " / " + str(self._calc_CI()) + " = " + \
                str(self._calc_DC()/10 * self.factor)
        else:
            # calculate the values for D, C, and D * C (under the redicule)
            s = str(self._calc_D()) + " × " + str(self._calc_C()) + " = " + \
                str(self._calc_DC() * self.factor)
        if self.sugar is True:
            self.activity.results_label.set_text(s)
            self.activity.results_label.show()
        else:
            if hasattr(self, 'win'):
                self.win.set_title("%s: %s" % (_('Sliderule'), s))
        return True

    def _calc_C(self):
        rx, ry = self.R.spr.get_xy()
        cx, cy = self.C.spr.get_xy()
        dx = rx - cx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        C = math.exp(dx / SCALE)
        return float(int(C * 100) / 100.)

    def _calc_CI(self):
        rx, ry = self.R.spr.get_xy()
        cx, cy = self.CI.spr.get_xy()
        dx = rx - cx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        CI = math.exp(dx / SCALE)
        return float(int((10.0 / CI) * 100)) / 100.

    def _calc_A(self):
        rx, ry = self.R.spr.get_xy()
        ax, ay = self.A.spr.get_xy()
        dx = rx - ax
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        A = math.exp(2 * dx / SCALE) # two-decade rule
        return float(int(A * 100) / 100.)

    def _calc_D(self):
        x, y = self.D.spr.get_xy()
        if self.slider_on_top == 'A':
            ax, ay = self.A.spr.get_xy()
            dx = ax - x
        elif self.slider_on_top == 'CI':
            cx, cy = self.CI.spr.get_xy()
            dx = cx - x
        else:
            cx, cy = self.C.spr.get_xy()
            dx = cx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        D = math.exp(dx / SCALE)
        return float(int(D * 100) / 100.)

    def _calc_DC(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.D.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        DC = math.exp(dx / SCALE)
        return float(int(DC * 100) / 100.)

    def _calc_DA(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.D.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(100.) * SCALE + dx
        DA = math.exp(dx / SCALE)
        return float(int(DA * 100) / 100.)

    def _calc_L2(self):
        rx, ry = self.R.spr.get_xy()
        lx, ly = self.L2.spr.get_xy()
        dx = rx - lx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L2 = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L2 = 10 * (dx / SCALE) / math.log(10)
        return float(int(L2 * 100) / 100.)

    def _calc_L(self):
        x, y = self.L.spr.get_xy()
        lx, ly = self.L2.spr.get_xy()
        dx = lx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_LL(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.L.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            LL = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            LL = 10 * (dx / SCALE) / math.log(10)
        return float(int(LL * 100) / 100.)

    def _expose_cb(self, win, event):
        self.sprites.redraw_sprites()
        return True

    def _destroy_cb(self, win, event):
        gtk.main_quit()
