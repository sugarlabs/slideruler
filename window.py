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

from constants import SHEIGHT, SWIDTH, SCALE

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


def move_slider_and_tabs(slider, tab_left, tab_right, dx, dy):
    slider.spr.move_relative((dx, dy))
    tab_left.spr.move_relative((dx, dy))
    tab_right.spr.move_relative((dx, dy))


def draw_slider_and_tabs(slider, tab_left, tab_right, layer=1000):
    slider.draw_slider(layer)
    tab_left.draw_slider(layer)
    tab_right.draw_slider(layer)


def hide_slider_and_tabs(slider, tab_left, tab_right):
    slider.spr.hide()
    tab_left.spr.hide()
    tab_right.spr.hide()


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
            self.parent = None

        # starting from Sugar
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
        self.scale = 1

        # Open the sliders
        y = 50
        self.results_label = Slider(self.sprites, self.path, 'label',
                                        int((self.width - 600) / 2),
                                        y + 4 * SHEIGHT,
                                        600, SHEIGHT)

        self.C = self._make_slider('C', y + 60)
        self.CI = self._make_slider('CI', y + 60)
        self.L = self._make_slider('L', y + 60)
        self.A = self._make_slider('A', y + 60)
        self.K = self._make_slider('K', y + 60)
        self.S = self._make_slider('S', y + 60)
        self.T = self._make_slider('T', y + 60)
        self.LLn = self._make_slider('LLn', y + 60)
        self.LL0 = self._make_slider('LL0', y + 60)

        self.D = self._make_slider('D', y + 2 * SHEIGHT)
        self.DI = self._make_slider('DI', y + 2 * SHEIGHT)
        self.L2 = self._make_slider('L2', y + 2 * SHEIGHT)
        self.A2 = self._make_slider('A2', y + 2 * SHEIGHT)
        self.K2 = self._make_slider('K2', y + 2 * SHEIGHT)
        self.S2 = self._make_slider('S2', y + 2 * SHEIGHT)
        self.T2 = self._make_slider('T2', y + 2 * SHEIGHT)
        self.LLn2 = self._make_slider('LLn2', y + 2 * SHEIGHT)
        self.LL02 = self._make_slider('LL02', y + 2 * SHEIGHT)

        self.C_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.C_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.CI_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.CI_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.L_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.L_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.A_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.A_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.K_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.K_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.S_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.S_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.T_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.T_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.LLn_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.LLn_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.LL0_tab_left = self._make_tab(0, y + 3 * SHEIGHT)
        self.LL0_tab_right =  self._make_tab(SWIDTH - 100, y + 3 * SHEIGHT)
        self.R_tab_top = self._make_tab(150, y)
        self.R_tab_bottom = self._make_tab(150, y + 3 * SHEIGHT)

        self.R = Slider(self.sprites, self.path, 'reticule',
                        150, y + SHEIGHT, 100, 2 * SHEIGHT)
        self.R.draw_slider(2000)

        self.slider_on_top = 'C'
        self.slider_on_bottom = 'D'

        self.update_slider_labels()
        self.update_results_label()

        self.factor = 1
        self.press = None
        self.last = None
        self.dragpos = 0

    def _keypress_cb(self, area, event):
        """ Keypress: moving the sliders with the arrow keys """
        k = gtk.gdk.keyval_name(event.keyval)
        if self.parent == None:
            return
        if k == 'a':
            self.parent.show_a()
        elif k == 'k':
            self.parent.show_k()
        elif k == 'c' or k == 'asterisk' or k == 'x':
            self.parent.show_c()
        elif k == 'i':
            self.parent.show_ci()
        elif k == 's':
            self.parent.show_s()
        elif k == 't':
            self.parent.show_t()
        elif k == 'l' or k == 'plus':
            self.parent.show_l()
        elif k == 'Left' or k == 'comma':
            self._move_slides(self.last, -1)
        elif k == 'Right' or k == 'period':
            self._move_slides(self.last, 1)
        elif k == 'Home' or k == 'Pause':
            self._move_slides(self.D.spr, -self.D.spr.get_xy()[0])
        elif k == 'r':
            self.R_tab_top.spr.move((150, self.R_tab_top.spr.get_xy()[1]))
            self.R_tab_bottom.spr.move((150, self.R_tab_bottom.spr.get_xy()[1]))
            self.R.spr.move((150, self.R.spr.get_xy()[1]))
            self.update_slider_labels()
            self.update_results_label()
        elif k == 'Return' or k == 'BackSpace':
            self.parent.realign_cb()
            self.R_tab_top.spr.move((150, self.R_tab_top.spr.get_xy()[1]))
            self.R_tab_bottom.spr.move((150, self.R_tab_bottom.spr.get_xy()[1]))
            self.R.spr.move((150, self.R.spr.get_xy()[1]))
            self.update_slider_labels()
            self.update_results_label()
        return True

    def _make_slider(self, name, y):
        slider = Slider(self.sprites, self.path, name, 0, y, SWIDTH, SHEIGHT)
        slider.spr.set_label('')
        slider.draw_slider()
        return slider

    def _make_tab(self, x, y):
        tab = Tab(self.sprites, self.path, 'tab', x, y, 100, SHEIGHT)
        tab.draw_slider()
        return tab

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
        self._move_slides(self.press, dx)
        self.dragpos = x

    def _move_slides(self, sprite, dx):
        if sprite in [self.D.spr, self.DI.spr, self.L2.spr, self.T2.spr,
                      self.A2.spr, self.K2.spr, self.S2.spr, self.LLn2.spr]:
            move_slider_and_tabs(self.C, self.C_tab_left,
                                 self.C_tab_right, dx, 0)
            move_slider_and_tabs(self.CI, self.CI_tab_left,
                                 self.CI_tab_right, dx, 0)
            move_slider_and_tabs(self.L, self.L_tab_left,
                                 self.L_tab_right, dx, 0)
            move_slider_and_tabs(self.A, self.A_tab_left,
                                 self.A_tab_right, dx, 0)
            move_slider_and_tabs(self.K, self.K_tab_left,
                                 self.K_tab_right, dx, 0)
            move_slider_and_tabs(self.S, self.S_tab_left,
                                 self.S_tab_right, dx, 0)
            move_slider_and_tabs(self.T, self.T_tab_left,
                                 self.T_tab_right, dx, 0)
            move_slider_and_tabs(self.LLn, self.LLn_tab_left,
                                 self.LLn_tab_right, dx, 0)
            move_slider_and_tabs(self.LL0, self.LLn_tab_left,
                                 self.LL0_tab_right, dx, 0)
            self.D.spr.move_relative((dx, 0))
            self.DI.spr.move_relative((dx, 0))
            self.L2.spr.move_relative((dx, 0))
            self.T2.spr.move_relative((dx, 0))
            self.S2.spr.move_relative((dx, 0))
            self.A2.spr.move_relative((dx, 0))
            self.K2.spr.move_relative((dx, 0))
            self.LLn2.spr.move_relative((dx, 0))
            self.LL02.spr.move_relative((dx, 0))
            move_slider_and_tabs(self.R, self.R_tab_top,
                                 self.R_tab_bottom, dx, 0)
        elif sprite == self.R_tab_top.spr or \
             sprite == self.R_tab_bottom.spr or \
             sprite == self.R.spr:
            move_slider_and_tabs(self.R, self.R_tab_top,
                                 self.R_tab_bottom, dx, 0)
        elif sprite == self.C.spr or \
             sprite == self.C_tab_left.spr or \
             sprite == self.C_tab_right.spr:
            move_slider_and_tabs(self.C, self.C_tab_left,
                                 self.C_tab_right, dx, 0)
        elif sprite == self.CI.spr or \
             sprite == self.CI_tab_left.spr or \
             sprite == self.CI_tab_right.spr:
            move_slider_and_tabs(self.CI, self.CI_tab_left,
                                 self.CI_tab_right, dx, 0)
        elif sprite == self.A.spr or \
             sprite == self.A_tab_left.spr or \
             sprite == self.A_tab_right.spr:
            move_slider_and_tabs(self.A, self.A_tab_left,
                                 self.A_tab_right, dx, 0)
        elif sprite == self.K.spr or \
             sprite == self.K_tab_left.spr or \
             sprite == self.K_tab_right.spr:
            move_slider_and_tabs(self.K, self.K_tab_left,
                                 self.K_tab_right, dx, 0)
        elif sprite == self.S.spr or \
             sprite == self.S_tab_left.spr or \
             sprite == self.S_tab_right.spr:
            move_slider_and_tabs(self.S, self.S_tab_left,
                                 self.S_tab_right, dx, 0)
        elif sprite == self.T.spr or \
             sprite == self.T_tab_left.spr or \
             sprite == self.T_tab_right.spr:
            move_slider_and_tabs(self.T, self.T_tab_left,
                                 self.T_tab_right, dx, 0)
        elif sprite == self.L.spr or \
             sprite == self.L_tab_left.spr or \
             sprite == self.L_tab_right.spr:
            move_slider_and_tabs(self.L, self.L_tab_left,
                                 self.L_tab_right, dx, 0)
        elif sprite == self.LLn.spr or \
             sprite == self.LLn_tab_left.spr or \
             sprite == self.LLn_tab_right.spr:
            move_slider_and_tabs(self.LLn, self.LLn_tab_left,
                                 self.LLn_tab_right, dx, 0)
        elif sprite == self.LL0.spr or \
             sprite == self.LL0_tab_left.spr or \
             sprite == self.LL0_tab_right.spr:
            move_slider_and_tabs(self.LL0, self.LL0_tab_left,
                                 self.LL0_tab_right, dx, 0)

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
        self.LLn_tab_left.spr.set_label(str(function()))
        self.LLn_tab_right.spr.set_label(str(function()))
        self.LL0_tab_left.spr.set_label(str(function()))
        self.LL0_tab_right.spr.set_label(str(function()))

    def update_slider_labels(self):
        """ Based on the current alignment of the rules, calculate labels. """
        if self.slider_on_bottom == 'L2':
            self._update_top(self._calc_L2)
            self.R_tab_bottom.spr.set_label(str(self._calc_L2_results()))
        elif self.slider_on_bottom == 'DI':
            self._update_top(self._calc_DI)
            self.R_tab_bottom.spr.set_label(str(self._calc_DI_results()))
        elif self.slider_on_bottom == 'A2':
            self._update_top(self._calc_A2)
            self.R_tab_bottom.spr.set_label(str(self._calc_A2_results()))
        elif self.slider_on_bottom == 'K2':
            self._update_top(self._calc_K2)
            self.R_tab_bottom.spr.set_label(str(self._calc_K2_results()))
        elif self.slider_on_bottom == 'S2':
            self._update_top(self._calc_S2)
            self.R_tab_bottom.spr.set_label(str(self._calc_S2_results()))
        elif self.slider_on_bottom == 'T2':
            self._update_top(self._calc_T2)
            self.R_tab_bottom.spr.set_label(str(self._calc_T2_results()))
        elif self.slider_on_bottom == 'LLn2':
            self._update_top(self._calc_LLn2)
            self.R_tab_bottom.spr.set_label(str(self._calc_LLn2_results()))
        elif self.slider_on_bottom == 'LL02':
            self._update_top(self._calc_LL02)
            self.R_tab_bottom.spr.set_label(str(self._calc_LL02_results()))
        else:
            self._update_top(self._calc_D)
            self.R_tab_bottom.spr.set_label(str(self._calc_D_results()))

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
        elif self.slider_on_top == 'LLn':
            self.R_tab_top.spr.set_label(str(self._calc_LLn()))
        elif self.slider_on_top == 'LL0':
            self.R_tab_top.spr.set_label(str(self._calc_LL0()))
        else:
            self.R_tab_top.spr.set_label(str(self._calc_C()))

    def _button_release_cb(self, win, event):
        if self.press == None:
            return True
        self.last = self.press
        self.press = None
        self.update_results_label()

    def update_results_label(self):
        """ Update toolbar label with results of calculation. """
        s = ''
        if self.slider_on_bottom == 'D':
            dx, dy = self.D.spr.get_xy()
            if self.slider_on_top == 'A':
                if self.A.spr.get_xy()[0] == dx:
                    A = str(self._calc_A())
                    DA = str(self._calc_D_results() * self.factor)
                    s = " √ %s = %s\t\t%s² = %s" % (A, DA, DA, A)
            elif self.slider_on_top == 'K':
                if self.K.spr.get_xy()[0] == dx:
                    K = str(self._calc_K())
                    DK = str(self._calc_D_results() * self.factor)
                    s = " ∛ %s = %s\t\t%s³ = %s" % (K, DK, DK, K)
            elif self.slider_on_top == 'S':
                if self.S.spr.get_xy()[0] == dx:
                    S = str(self._calc_S())
                    DS = str(self._calc_D_results() / 10)
                    s = " sin(%s) = %s\t\tasin(%s) = %s" % (S, DS, DS, S)
            elif self.slider_on_top == 'T':
                if self.T.spr.get_xy()[0] == dx:
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
    def _r_offset(self, slider):
        return self.R.spr.get_xy()[0] - slider.spr.get_xy()[0]

    def _calc_C(self):
        """ C scale is read from the reticule. """
        dx = self._r_offset(self.C)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        C = math.exp(dx / SCALE)
        return float(int(C * 100) / 100.)

    def _calc_LLn(self):
        """ LLn scale is read from the reticule. """
        dx = self._r_offset(self.LLn)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        LLn = (dx / SCALE)
        return float(int(LLn * 100) / 100.)

    def _calc_LL0(self):
        """ LL0 scale is read from the reticule. """
        dx = self._r_offset(self.LL0)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        LL0 = (dx / SCALE)
        return float(int(LL0 * 100) / 100.)

    def _calc_CI(self):
        """ CO scale is read from the reticule. """
        dx = self._r_offset(self.CI)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        CI = math.exp(dx / SCALE)
        return float(int((10./CI) * 100) / 100.)

    def _calc_A(self):
        """ A scale is read from the reticule. """
        dx = self._r_offset(self.A)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        A = math.exp(2 * dx / SCALE)
        return float(int(A * 10) / 10.)

    def _calc_S(self):
        """ S scale is read from the reticule. """
        dx = self._r_offset(self.S)
        dx /= SCALE
        s = math.exp(dx)/10
        if s > 1.0:
            s = 1.0
        r = math.asin(s)
        S = 180.0 * r / math.pi
        return float(int(S * 10) / 10.)

    def _calc_T(self):
        """ T scale is read from the reticule. """
        dx = self._r_offset(self.T)
        dx /= SCALE
        t = math.exp(dx)/10
        if t > 1.0:
            t = 1.0
        r = math.atan(t)
        T = 180.0 * r / math.pi
        return float(int(T * 10) / 10.)

    def _calc_K(self):
        """ K scale is read from the reticule. """
        dx = self._r_offset(self.K)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        K = math.exp(3 * dx / SCALE)
        return float(int(K * 10) / 10.)

    def _calc_L(self):
        """ L scale is read from the reticule. """
        dx = self._r_offset(self.L)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _top_slide_offset(self, x):
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
        elif self.slider_on_top == 'LLn':
            x2, y2 = self.LLn.spr.get_xy()
        elif self.slider_on_top == 'LL0':
            x2, y2 = self.LL0.spr.get_xy()
        return x2 - x

    def _calc_D(self):
        """ D scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.D.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        D = math.exp(dx / SCALE)
        return float(int(D * 100) / 100.)

    def _calc_LLn2(self):
        """ LLn2 scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.LLn2.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        LLn = (dx / SCALE)
        return float(int(LLn * 100) / 100.)

    def _calc_LL02(self):
        """ LL02 scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.LL02.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        LL0 = (dx / SCALE)
        return float(int(LL0 * 100) / 100.)

    def _calc_DI(self):
        """ DI scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.DI.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 0.1
        else:
            self.factor = 1
        DI = math.exp(dx / SCALE)
        return float(int((10.0 / DI) * 100)) / 100.

    def _calc_L2(self):
        """ L scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.L2.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_A2(self):
        """ A2 scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.A2.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        A2 = math.exp(2 * dx / SCALE)
        return float(int(A2 * 100) / 100.)

    def _calc_K2(self):
        """ K2 scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.K2.spr.get_xy()[0])
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            self.factor = 10
        else:
            self.factor = 1
        K2 = math.exp(3 * dx / SCALE)
        return float(int(K2 * 100) / 100.)

    def _calc_S2(self):
        """ S2 scale is read from the position of the top slider """
        dx = self._top_slide_offset(self.S2.spr.get_xy()[0])
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
        dx = self._top_slide_offset(self.T2.spr.get_xy()[0])
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
        dx = self._r_offset(self.D)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        D = math.exp(dx / SCALE)
        return float(int(D * 100) / 100.)

    def _calc_LLn2_results(self):
        dx = self._r_offset(self.D)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        LLn = (dx / SCALE)
        return float(int(LLn * 100) / 100.)

    def _calc_DI_results(self):
        dx = self._r_offset(self.DI)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        DI = math.exp(dx / SCALE)
        return float(int((10.0 / DI) * 100) / 100.)

    def _calc_L2_results(self):
        dx = self._r_offset(self.L2)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
            L = 10 * ((dx / SCALE) / math.log(10) - 1.0)
        else:
            L = 10 * (dx / SCALE) / math.log(10)
        return float(int(L * 100) / 100.)

    def _calc_A2_results(self):
        dx = self._r_offset(self.A2)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        A2 = math.exp(2 * dx / SCALE)
        return float(int(A2 * 100) / 100.)

    def _calc_K2_results(self):
        dx = self._r_offset(self.K2)
        if dx < 0:
            dx = math.log(10.) * SCALE + dx
        K2 = math.exp(3 * dx / SCALE)
        return float(int(K2 * 100) / 100.)

    def _calc_S2_results(self):
        dx = self._r_offset(self.S2)
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
        dx = self._r_offset(self.T2)
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
        # self.sprite_list.refresh(event)
        self.sprites.redraw_sprites()
        return True

    def _destroy_cb(self, win, event):
        gtk.main_quit()
