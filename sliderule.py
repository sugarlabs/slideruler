#!/usr/bin/env python

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

import pygtk
pygtk.require('2.0')
import gtk

from gettext import gettext as _
import os

from window import SlideRule

_FA = _('square/square root')
_FC = _('multiply/divide')
_FCI = _('divide/multiply')
_FK = _('cube/cube root')
_FS = _('sin, asin')
_FT = _('tan, atan')
_FL = _('add/subtract')


class SlideruleMain:

    def __init__(self):
        self.r = 0
        self.sr = None

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.maximize()
        self.win.set_title(_('Slide Rule'))
        self.win.connect('delete_event', lambda w,e: gtk.main_quit())

        menu = gtk.Menu()
        menu_items = gtk.MenuItem(_("L") + ' ' + _FL)
        menu.append(menu_items)
        menu_items.connect("activate", self._l_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("C") + ' ' + _FC)
        menu.append(menu_items)
        menu_items.connect("activate", self._c_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("CI") + ' ' + _FCI)
        menu.append(menu_items)
        menu_items.connect("activate", self._ci_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("A") + ' ' + _FA)
        menu.append(menu_items)
        menu_items.connect("activate", self._a_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("K") + ' ' + _FK)
        menu.append(menu_items)
        menu_items.connect("activate", self._k_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("S") + ' ' + _FS)
        menu.append(menu_items)
        menu_items.connect("activate", self._s_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("T") + ' ' + _FT)
        menu.append(menu_items)
        menu_items.connect("activate", self._t_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("realign slides"))
        menu.append(menu_items)
        menu_items.connect("activate", self._realign_cb)
        menu_items.show()
        root_menu = gtk.MenuItem("Tools")
        root_menu.show()
        root_menu.set_submenu(menu)

        vbox = gtk.VBox(False, 0)
        self.win.add(vbox)
        vbox.show()

        menu_bar = gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)
        menu_bar.show()

        canvas = gtk.DrawingArea()
        vbox.pack_end(canvas, True, True)
        canvas.show()

        menu_bar.append(root_menu)
        self.win.show_all()

        self.sr = SlideRule(canvas, os.path.join(os.path.abspath('.'),
                                                 'images/'))
        self.sr.win = self.win
        self.sr.activity = self
        self.hide_all()
        self._c_cb(None)

    def set_title(self, title):
        self.win.set_title(title)

    def hide_all(self):
        self.sr.A.spr.hide()
        self.sr.K.spr.hide()
        self.sr.S.spr.hide()
        self.sr.T.spr.hide()
        self.sr.A2.spr.hide()
        self.sr.K2.spr.hide()
        self.sr.S2.spr.hide()
        self.sr.T2.spr.hide()
        self.sr.D.spr.hide()
        self.sr.C.spr.hide()
        self.sr.C_tab_left.spr.hide()
        self.sr.C_tab_right.spr.hide()
        self.sr.CI.spr.hide()
        self.sr.CI_tab_left.spr.hide()
        self.sr.CI_tab_right.spr.hide()
        self.sr.A_tab_left.spr.hide()
        self.sr.A_tab_right.spr.hide()
        self.sr.K_tab_left.spr.hide()
        self.sr.K_tab_right.spr.hide()
        self.sr.S_tab_left.spr.hide()
        self.sr.S_tab_right.spr.hide()
        self.sr.T_tab_left.spr.hide()
        self.sr.T_tab_right.spr.hide()
        self.sr.L2.spr.hide()
        self.sr.L.spr.hide()
        self.sr.L_tab_left.spr.hide()
        self.sr.L_tab_right.spr.hide()
        self.sr.LL02.spr.hide()
        self.sr.LL0.spr.hide()
        self.sr.LL0_tab_left.spr.hide()
        self.sr.LL0_tab_right.spr.hide()
        self.sr.LLn2.spr.hide()
        self.sr.LLn.spr.hide()
        self.sr.LLn_tab_left.spr.hide()
        self.sr.LLn_tab_right.spr.hide()

    def _realign_cb(self, arg=None):
        """ Realign all sliders with the D scale. """
        dx, dy = self.sr.D.spr.get_xy()
        cx, cy = self.sr.C.spr.get_xy()
        ax, y = self.sr.A.spr.get_xy()
        ix, y = self.sr.CI.spr.get_xy()
        kx, y = self.sr.K.spr.get_xy()
        sx, y = self.sr.S.spr.get_xy()
        tx, y = self.sr.T.spr.get_xy()
        lx, y = self.sr.L.spr.get_xy()
        ll0x, y = self.sr.LL0.spr.get_xy()
        llnx, y = self.sr.LLn.spr.get_xy()
        self.sr.C.spr.move((dx, cy))
        self.sr.CI.spr.move((dx, cy))
        self.sr.A.spr.move((dx, cy))
        self.sr.K.spr.move((dx, cy))
        self.sr.S.spr.move((dx, cy))
        self.sr.T.spr.move((dx, cy))
        self.sr.L.spr.move((dx, cy))
        self.sr.LL0.spr.move((dx, cy))
        self.sr.LLn.spr.move((dx, cy))
        self.sr.LL02.spr.move((dx, cy))
        self.sr.LLn2.spr.move((dx, cy))
        self.sr.L2.spr.move((dx, dy))
        self.sr.A2.spr.move((dx, dy))
        self.sr.K2.spr.move((dx, dy))
        self.sr.S2.spr.move((dx, dy))
        self.sr.T2.spr.move((dx, dy))
        self.sr.DI.spr.move((dx, dy))
        self.sr.C_tab_left.spr.move_relative((dx-cx, 0))
        self.sr.C_tab_right.spr.move_relative((dx-cx, 0))
        self.sr.CI_tab_left.spr.move_relative((dx-ix, 0))
        self.sr.CI_tab_right.spr.move_relative((dx-ix, 0))
        self.sr.A_tab_left.spr.move_relative((sx-ax, 0))
        self.sr.A_tab_right.spr.move_relative((dx-ax, 0))
        self.sr.K_tab_left.spr.move_relative((dx-kx, 0))
        self.sr.K_tab_right.spr.move_relative((dx-kx, 0))
        self.sr.S_tab_left.spr.move_relative((dx-sx, 0))
        self.sr.S_tab_right.spr.move_relative((dx-sx, 0))
        self.sr.T_tab_left.spr.move_relative((dx-tx, 0))
        self.sr.T_tab_right.spr.move_relative((dx-tx, 0))
        self.sr.L_tab_left.spr.move_relative((dx-lx, 0))
        self.sr.L_tab_right.spr.move_relative((dx-lx, 0))
        self.sr.LL0_tab_left.spr.move_relative((dx-ll0x, 0))
        self.sr.LL0_tab_right.spr.move_relative((dx-ll0x, 0))
        self.sr.LLn_tab_left.spr.move_relative((dx-llnx, 0))
        self.sr.LLn_tab_right.spr.move_relative((dx-llnx, 0))
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _c_cb(self, widget):
        self.hide_all()
        self.sr.C.draw_slider(1000)
        self.sr.C_tab_left.draw_slider(1000)
        self.sr.C_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "C"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _ci_cb(self, widget):
        self.hide_all()
        self.sr.CI.draw_slider(1000)
        self.sr.CI_tab_left.draw_slider(1000)
        self.sr.CI_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "CI"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _a_cb(self, widget):
        self.hide_all()
        self.sr.A.draw_slider(1000)
        self.sr.A_tab_left.draw_slider(1000)
        self.sr.A_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "A"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _k_cb(self, widget):
        self.hide_all()
        self.sr.K.draw_slider(1000)
        self.sr.K_tab_left.draw_slider(1000)
        self.sr.K_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "K"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _s_cb(self, widget):
        self.hide_all()
        self.sr.S.draw_slider(1000)
        self.sr.S_tab_left.draw_slider(1000)
        self.sr.S_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "S"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _t_cb(self, widget):
        self.hide_all()
        self.sr.T.draw_slider(1000)
        self.sr.T_tab_left.draw_slider(1000)
        self.sr.T_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "T"
        self.sr.slider_on_bottom = "D"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _l_cb(self, widget):
        self.hide_all()
        self.sr.L2.draw_slider(1000)
        self.sr.L.draw_slider(1000)
        self.sr.L_tab_left.draw_slider(1000)
        self.sr.L_tab_right.draw_slider(1000)
        self.sr.slider_on_top = "L"
        self.sr.slider_on_bottom = "L2"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SlideruleMain()
    main()
