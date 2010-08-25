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


class SlideruleMain:

    def __init__(self):
        self.r = 0
        self.sr = None

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.maximize()
        self.win.set_title(_('Slide Rule'))
        self.win.connect('delete_event', lambda w,e: gtk.main_quit())

        menu = gtk.Menu()
        menu_items = gtk.MenuItem(_("L"))
        menu.append(menu_items)
        menu_items.connect("activate", self._l_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("C"))
        menu.append(menu_items)
        menu_items.connect("activate", self._c_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("CI"))
        menu.append(menu_items)
        menu_items.connect("activate", self._ci_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("A"))
        menu.append(menu_items)
        menu_items.connect("activate", self._a_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("K"))
        menu.append(menu_items)
        menu_items.connect("activate", self._k_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("S"))
        menu.append(menu_items)
        menu_items.connect("activate", self._s_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("T"))
        menu.append(menu_items)
        menu_items.connect("activate", self._t_cb)
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

    def hide_all(self):
        self.sr.A.spr.hide()
        self.sr.K.spr.hide()
        self.sr.S.spr.hide()
        self.sr.T.spr.hide()
        self.sr.C.spr.hide()
        self.sr.C_tab_left.spr.hide()
        self.sr.C_tab_right.spr.hide()
        self.sr.CI.spr.hide()
        self.sr.CI_tab_left.spr.hide()
        self.sr.CI_tab_right.spr.hide()
        self.sr.L.spr.hide()
        self.sr.L2.spr.hide()
        self.sr.L2_tab_left.spr.hide()
        self.sr.L2_tab_right.spr.hide()

    def set_title(self, title):
        self.win.set_title(title)

    def _c_cb(self, widget):
        self.hide_all()
        self.sr.C.draw_slider(1000)
        self.sr.C_tab_left.draw_slider(1000)
        self.sr.C_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "C"
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
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _a_cb(self, widget):
        self.hide_all()
        self.sr.A.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "A"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _k_cb(self, widget):
        self.hide_all()
        self.sr.K.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "K"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _s_cb(self, widget):
        self.hide_all()
        self.sr.S.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "S"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _t_cb(self, widget):
        self.hide_all()
        self.sr.T.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = "T"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True

    def _l_cb(self, widget):
        self.hide_all()
        self.sr.L.draw_slider(1000)
        self.sr.L2.draw_slider(1000)
        self.sr.L2_tab_left.draw_slider(1000)
        self.sr.L2_tab_right.draw_slider(1000)
        self.sr.slider_on_top = "L"
        self.sr.update_slider_labels()
        self.sr.update_results_label()
        return True


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SlideruleMain()
    main()
