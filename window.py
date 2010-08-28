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

from sprite_factory import Slider, Tab
from sprites import Sprites


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
        self.results_label = Slider(self.sprites, self.path, 'label',
                                        int((self.width - 600) / 2),
                                        y + 4 * SHEIGHT,
                                        600, SHEIGHT)

        self.A = Slider(self.sprites, self.path, 'A',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.K = Slider(self.sprites, self.path, 'K',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.S = Slider(self.sprites, self.path, 'S',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.T = Slider(self.sprites, self.path, 'T',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.C = Slider(self.sprites, self.path, 'C',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.CI = Slider(self.sprites, self.path, 'CI',
                        0, y + 60, SWIDTH, SHEIGHT)
        self.L = Slider(self.sprites, self.path, 'L',
                         0, y + 60, SWIDTH, SHEIGHT)

        self.DI = Slider(self.sprites, self.path, 'DI',
                         0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.D = Slider(self.sprites, self.path, 'D',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.L2 = Slider(self.sprites, self.path, 'L2',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.A2 = Slider(self.sprites, self.path, 'A2',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.K2 = Slider(self.sprites, self.path, 'K2',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.S2 = Slider(self.sprites, self.path, 'S2',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)
        self.T2 = Slider(self.sprites, self.path, 'T2',
                        0, y + 2 * SHEIGHT, SWIDTH, SHEIGHT)

        self.C_tab_left = Tab(self.sprites, self.path, 'tab',
                              0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.C_tab_right = Tab(self.sprites, self.path, 'tab',
                               SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.CI_tab_left = Tab(self.sprites, self.path, 'tab',
                               0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.CI_tab_right = Tab(self.sprites, self.path, 'tab',
                                SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.A_tab_left = Tab(self.sprites, self.path, 'tab',
                              0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.A_tab_right = Tab(self.sprites, self.path, 'tab',
                               SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.K_tab_left = Tab(self.sprites, self.path, 'tab',
                              0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.K_tab_right = Tab(self.sprites, self.path, 'tab',
                               SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.S_tab_left = Tab(self.sprites, self.path, 'tab',
                              0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.S_tab_right = Tab(self.sprites, self.path, 'tab',
                               SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.T_tab_left = Tab(self.sprites, self.path, 'tab',
                              0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.T_tab_right = Tab(self.sprites, self.path, 'tab',
                               SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.L_tab_left = Tab(self.sprites, self.path, 'tab',
                               0, y + 3 * SHEIGHT, 100, SHEIGHT)
        self.L_tab_right = Tab(self.sprites, self.path, 'tab',
                                SWIDTH-100, y + 3 * SHEIGHT, 100, SHEIGHT)

        self.R = Slider(self.sprites, self.path, 'reticule',
                        150, y + SHEIGHT, 100, 2 * SHEIGHT)
        self.R_tab_top = Tab(self.sprites, self.path, 'tab',
                             150, y, 100, 60)
        self.R_tab_bot = Tab(self.sprites, self.path, 'tab',
                             150, y + 3 * SHEIGHT, 100, SHEIGHT)

        self.slider_on_top = 'C'
        self.slider_on_bottom = 'D'

        self.R.spr.set_label('')
        self.A.spr.set_label('')
        self.K.spr.set_label('')
        self.S.spr.set_label('')
        self.T.spr.set_label('')
        self.C.spr.set_label('')
        self.CI.spr.set_label('')
        self.D.spr.set_label('')
        self.DI.spr.set_label('')
        self.L2.spr.set_label('')
        self.A2.spr.set_label('')
        self.K2.spr.set_label('')
        self.S2.spr.set_label('')
        self.T2.spr.set_label('')
        self.L.spr.set_label('')

        self.A.draw_slider(500)
        self.A_tab_left.draw_slider()
        self.A_tab_right.draw_slider()
        self.K.draw_slider()
        self.K_tab_left.draw_slider()
        self.K_tab_right.draw_slider()
        self.S.draw_slider()
        self.S_tab_left.draw_slider()
        self.S_tab_right.draw_slider()
        self.T.draw_slider()
        self.T_tab_left.draw_slider()
        self.T_tab_right.draw_slider()
        self.C.draw_slider()
        self.C_tab_left.draw_slider()
        self.C_tab_right.draw_slider()
        self.CI.draw_slider()
        self.CI_tab_left.draw_slider()
        self.CI_tab_right.draw_slider()
        self.D.draw_slider()
        self.DI.draw_slider()
        self.R_tab_bot.draw_slider()
        self.R_tab_top.draw_slider()
        self.R.draw_slider(2000)
        self.L2.draw_slider()
        self.L.draw_slider()
        self.L_tab_left.draw_slider()
        self.L_tab_right.draw_slider()
        self.A2.draw_slider()
        self.K2.draw_slider()
        self.S2.draw_slider()
        self.T2.draw_slider()

        self.update_slider_labels()
        self.update_results_label()

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
        if self.press in [self.D.spr, self.DI.spr, self.L2.spr, self.T2.spr,
                          self.A2.spr, self.K2.spr, self.S2.spr]:
            self.C.spr.move_relative((dx, 0))
            self.C_tab_left.spr.move_relative((dx, 0))
            self.C_tab_right.spr.move_relative((dx, 0))
            self.CI.spr.move_relative((dx, 0))
            self.CI_tab_left.spr.move_relative((dx, 0))
            self.CI_tab_right.spr.move_relative((dx, 0))
            self.DI.spr.move_relative((dx, 0))
            self.A.spr.move_relative((dx, 0))
            self.A_tab_left.spr.move_relative((dx, 0))
            self.A_tab_right.spr.move_relative((dx, 0))
            self.K.spr.move_relative((dx, 0))
            self.K_tab_left.spr.move_relative((dx, 0))
            self.K_tab_right.spr.move_relative((dx, 0))
            self.S.spr.move_relative((dx, 0))
            self.S_tab_left.spr.move_relative((dx, 0))
            self.S_tab_right.spr.move_relative((dx, 0))
            self.T.spr.move_relative((dx, 0))
            self.T_tab_left.spr.move_relative((dx, 0))
            self.T_tab_right.spr.move_relative((dx, 0))
            self.L2.spr.move_relative((dx, 0))
            self.T2.spr.move_relative((dx, 0))
            self.S2.spr.move_relative((dx, 0))
            self.A2.spr.move_relative((dx, 0))
            self.K2.spr.move_relative((dx, 0))
            self.L.spr.move_relative((dx, 0))
            self.L_tab_left.spr.move_relative((dx, 0))
            self.L_tab_right.spr.move_relative((dx, 0))
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
        elif self.press == self.CI.spr or \
             self.press == self.CI_tab_left.spr or \
             self.press == self.CI_tab_right.spr:
            self.CI.spr.move_relative((dx, 0))
            self.CI_tab_left.spr.move_relative((dx, 0))
            self.CI_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.A.spr or \
             self.press == self.A_tab_left.spr or \
             self.press == self.A_tab_right.spr:
            self.A.spr.move_relative((dx, 0))
            self.A_tab_left.spr.move_relative((dx, 0))
            self.A_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.K.spr or \
             self.press == self.K_tab_left.spr or \
             self.press == self.K_tab_right.spr:
            self.K.spr.move_relative((dx, 0))
            self.K_tab_left.spr.move_relative((dx, 0))
            self.K_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.S.spr or \
             self.press == self.S_tab_left.spr or \
             self.press == self.S_tab_right.spr:
            self.S.spr.move_relative((dx, 0))
            self.S_tab_left.spr.move_relative((dx, 0))
            self.S_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.T.spr or \
             self.press == self.T_tab_left.spr or \
             self.press == self.T_tab_right.spr:
            self.T.spr.move_relative((dx, 0))
            self.T_tab_left.spr.move_relative((dx, 0))
            self.T_tab_right.spr.move_relative((dx, 0))
        elif self.press == self.L.spr or \
             self.press == self.L_tab_left.spr or \
             self.press == self.L_tab_right.spr:
            self.L.spr.move_relative((dx, 0))
            self.L_tab_left.spr.move_relative((dx, 0))
            self.L_tab_right.spr.move_relative((dx, 0))

        # reset drag position
        self.dragpos = x
        self.update_slider_labels()
        self.update_results_label()

    def _update_top(self, function):
        self.C_tab_left.spr.set_label(str(function()))
        self.C_tab_right.spr.set_label(str(function()))
        self.CI_tab_left.spr.set_label(str(function()))
        self.CI_tab_right.spr.set_label(str(function()))
        self.A_tab_left.spr.set_label(str(function()))
        self.A_tab_right.spr.set_label(str(function()))
        self.K_tab_left.spr.set_label(str(function()))
        self.K_tab_right.spr.set_label(str(function()))
        self.S_tab_left.spr.set_label(str(function()))
        self.S_tab_right.spr.set_label(str(function()))
        self.T_tab_left.spr.set_label(str(function()))
        self.T_tab_right.spr.set_label(str(function()))
        self.L_tab_left.spr.set_label(str(function()))
        self.L_tab_right.spr.set_label(str(function()))

    def update_slider_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        if self.slider_on_bottom == 'D':
            self._update_top(self._calc_D)
            self.R_tab_bot.spr.set_label(str(self._calc_D_results()))
        elif self.slider_on_bottom == 'DI':
            self._update_top(self._calc_DI)
            self.R_tab_bot.spr.set_label(str(self._calc_DI_results()))
        elif self.slider_on_bottom == 'A2':
            self._update_top(self._calc_A2)
            self.R_tab_bot.spr.set_label(str(self._calc_A2_results()))
        elif self.slider_on_bottom == 'K2':
            self._update_top(self._calc_K2)
            self.R_tab_bot.spr.set_label(str(self._calc_K2_results()))
        elif self.slider_on_bottom == 'S2':
            self._update_top(self._calc_S2)
            self.R_tab_bot.spr.set_label(str(self._calc_S2_results()))
        elif self.slider_on_bottom == 'T2':
            self._update_top(self._calc_T2)
            self.R_tab_bot.spr.set_label(str(self._calc_T2_results()))
        else:
            self._update_top(self._calc_L2)
            self.R_tab_bot.spr.set_label(str(self._calc_L2_results()))

        if self.slider_on_top == 'A':
            self.R_tab_top.spr.set_label(str(self._calc_A()))
        elif self.slider_on_top == 'K':
            self.R_tab_top.spr.set_label(str(self._calc_K()))
        elif self.slider_on_top == 'S':
            self.R_tab_top.spr.set_label(str(self._calc_S()))
        elif self.slider_on_top == 'T':
            self.R_tab_top.spr.set_label(str(self._calc_T()))
        elif self.slider_on_top == 'L':
            self.R_tab_top.spr.set_label(str(self._calc_L()))
        elif self.slider_on_top == 'CI':
            self.R_tab_top.spr.set_label(str(self._calc_CI()))
        else:
            self.R_tab_top.spr.set_label(str(self._calc_C()))

    def _button_release_cb(self, win, event):
        if self.press == None:
            return True
        self.press = None
        self.update_results_label()

    def update_results_label(self):
        """ Update toolbar label with results of calculation. """
        s = ''
        if self.slider_on_bottom == 'D':
            dx, dy = self.D.spr.get_xy()
            if self.slider_on_top == 'A':
                x, y = self.A.spr.get_xy()
                if x == dx:
                    A = str(self._calc_A())
                    DA = str(self._calc_D_results() * self.factor)
                    s = " √ %s = %s\t\t%s² = %s" % (A, DA, DA, A)
            elif self.slider_on_top == 'K':
                x, y = self.K.spr.get_xy()
                if x == dx:
                    K = str(self._calc_K())
                    DK = str(self._calc_D_results() * self.factor)
                    s = " ∛ %s = %s\t\t%s³ = %s" % (K, DK, DK, K)
            elif self.slider_on_top == 'S':
                x, y = self.S.spr.get_xy()
                if x == dx:
                    S = str(self._calc_S())
                    DS = str(self._calc_D_results() / 10)
                    s = " sin(%s) = %s\t\tasin(%s) = %s" % (S, DS, DS, S)
            elif self.slider_on_top == 'T':
                x, y = self.T.spr.get_xy()
                if x == dx:
                    T = str(self._calc_T())
                    DT = str(self._calc_D_results() / 10)
                    s = " tan(%s) = %s\t\tatan(%s) = %s" % (T, DT, DT, T)
            elif self.slider_on_top == 'C':
                D = str(self._calc_D())
                C = str(self._calc_C())
                DC = str(self._calc_D_results() * self.factor)
                s = "%s × %s = %s\t\t%s / %s = %s" % (D, C, DC, DC, C, D)
            elif self.slider_on_top == 'CI':
                D = str(self._calc_D())
                CI = str(self._calc_CI())
                DCI = str(self._calc_D_results() * self.factor / 10.)
                s = "%s / %s = %s\t\t%s × %s = %s" % (D, CI, DCI, DCI, CI, D)
        elif self.slider_on_bottom == 'L2':
            if self.slider_on_top == 'L':
                # use ndash to display a minus sign
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

                LL = self._calc_L2_results()
                if LL < 0:
                    LLstr = "–" + str(-LL)
                else:
                    LLstr = str(LL)

                s = "%s %s %s = %s\t\t%s %s %s = %s" % (L2str, operator1, Lstr,
                                                        LLstr, LLstr,
                                                        operator2, Lstr, L2str)
        self.results_label.spr.set_label(s)

    # Calculate the value of individual scales
    def _calc_C(self):
        """ C scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        cx, cy = self.C.spr.get_xy()
        dx = rx - cx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        C = math.exp(dx / SCALE)
        return float(int(C * 100) / 100.)

    def _calc_CI(self):
        """ CO scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        cx, cy = self.CI.spr.get_xy()
        dx = rx - cx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        CI = math.exp(dx / SCALE)
        return float(int((10./CI) * 100) / 100.)

    def _calc_A(self):
        """ A scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        ax, ay = self.A.spr.get_xy()
        dx = rx - ax
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        A = math.exp(2 * dx / SCALE)
        return float(int(A * 10) / 10.)

    def _calc_S(self):
        """ S scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        sx, sy = self.S.spr.get_xy()
        dx = rx - sx
        dx /= SCALE
        s = math.exp(dx)/10
        if s > 1.0:
            s = 1.0
        r = math.asin(s)
        S = 180.0 * r / math.pi
        return float(int(S * 10) / 10.)

    def _calc_T(self):
        """ T scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        tx, ty = self.T.spr.get_xy()
        dx = rx - tx
        dx /= SCALE
        t = math.exp(dx)/10
        if t > 1.0:
            t = 1.0
        r = math.atan(t)
        T = 180.0 * r / math.pi
        return float(int(T * 10) / 10.)

    def _calc_K(self):
        """ K scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        kx, ky = self.K.spr.get_xy()
        dx = rx - kx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        K = math.exp(3 * dx / SCALE)
        return float(int(K * 10) / 10.)

    def _calc_L(self):
        """ L scale is read from the reticule. """
        rx, ry = self.R.spr.get_xy()
        lx, ly = self.L.spr.get_xy()
        dx = rx - lx
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_dx(self, x):
        """ Calcualate the offset between the top and bottom sliders """
        if self.slider_on_top == 'A':
            x2, y2 = self.A.spr.get_xy()
        elif self.slider_on_top == 'C':
            x2, y2 = self.C.spr.get_xy()
        elif self.slider_on_top == 'CI':
            x2, y2 = self.CI.spr.get_xy()
        elif self.slider_on_top == 'K':
            x2, y2 = self.K.spr.get_xy()
        elif self.slider_on_top == 'S':
            x2, y2 = self.S.spr.get_xy()
        elif self.slider_on_top == 'T':
            x2, y2 = self.T.spr.get_xy()
        elif self.slider_on_top == 'L':
            x2, y2 = self.L.spr.get_xy()
        else:
            x2 = x
        return x2 - x

    def _calc_D(self):
        """ D scale is read from the position of the top slider """
        x, y = self.D.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        D = math.exp(dx / SCALE)
        return float(int(D * 100) / 100.)

    def _calc_DI(self):
        """ DI scale is read from the position of the top slider """
        x, y = self.DI.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 0.1
        else:
            self.factor = 1
        DI = math.exp(dx / SCALE)
        return float(int((10.0 / DI) * 100)) / 100.

    def _calc_L2(self):
        """ L scale is read from the position of the top slider """
        x, y = self.L2.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_A2(self):
        """ A2 scale is read from the position of the top slider """
        x, y = self.A2.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        A2 = math.exp(2 * dx / SCALE)
        return float(int(A2 * 100) / 100.)

    def _calc_K2(self):
        """ K2 scale is read from the position of the top slider """
        x, y = self.K2.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        K2 = math.exp(3 * dx / SCALE)
        return float(int(K2 * 100) / 100.)

    def _calc_S2(self):
        """ S2 scale is read from the position of the top slider """
        x, y = self.S2.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        dx /= SCALE
        s = math.exp(dx)/10
        if s > 1.0:
            s = 1.0
        r = math.asin(s)
        S = 180.0 * r / math.pi
        return float(int(S * 10) / 10.)

    def _calc_T2(self):
        """ T2 scale is read from the position of the top slider """
        x, y = self.T2.spr.get_xy()
        dx = self._calc_dx(x)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        dx /= SCALE
        t = math.exp(dx)/10
        if t > 1.0:
            t = 1.0
        r = math.atan(t)
        T = 180.0 * r / math.pi
        return float(int(T * 10) / 10.)

    # Calculate results under redicule
    def _calc_D_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.D.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        D = math.exp(dx / SCALE)
        return float(int(D * 100) / 100.)

    def _calc_DI_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.DI.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        DI = math.exp(dx / SCALE)
        return float(int((10.0 / DI) * 100) / 100.)

    def _calc_L2_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.L2.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_A2_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.A2.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        A2 = math.exp(2 * dx / SCALE)
        return float(int(A2 * 100) / 100.)

    def _calc_K2_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.K2.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        K2 = math.exp(3 * dx / SCALE)
        return float(int(K2 * 100) / 100.)

    def _calc_S2_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.S2.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        dx /= SCALE
        s = math.exp(dx)/10
        if s > 1.0:
            s = 1.0
        r = math.asin(s)
        S = 180.0 * r / math.pi
        return float(int(S * 10) / 10.)

    def _calc_T2_results(self):
        rx, ry = self.R.spr.get_xy()
        x, y = self.T2.spr.get_xy()
        dx = rx - x
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        dx /= SCALE
        t = math.exp(dx)/10
        if t > 1.0:
            t = 1.0
        r = math.atan(t)
        T = 180.0 * r / math.pi
        return float(int(T * 10) / 10.)

    def _expose_cb(self, win, event):
        self.sprites.redraw_sprites()
        return True

    def _destroy_cb(self, win, event):
        gtk.main_quit()
