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

from sprites import *
import window
from constants import *

class SlideruleMain:
    def __init__(self):
        self.r = 0
        self.tw = None
        # create a new window
        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.maximize()
        self.win.set_title("%s: %s" % (_("Slide Rule"),
                           ("1.0 x 1.0 = 1.0")))
        self.win.connect("delete_event", lambda w,e: gtk.main_quit())

        menu = gtk.Menu()
        menu_items = gtk.MenuItem(_("C"))
        menu.append(menu_items)
        menu_items.connect("activate", self._c_cb)
        menu_items.show()
        menu_items = gtk.MenuItem(_("A"))
        menu.append(menu_items)
        menu_items.connect("activate", self._a_cb)
        menu_items = gtk.MenuItem(_("L"))
        menu.append(menu_items)
        menu_items.connect("activate", self._l_cb)
        menu_items.show()
        root_menu = gtk.MenuItem("Tools")
        root_menu.show()
        root_menu.set_submenu(menu)

        # A vbox to put a menu and the canvas in:
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

        # Join the activity
        self.tw = window.new_window(canvas, \
                               os.path.join(os.path.abspath('.'), \
                                            'images/'))
        self.tw.win = self.win
        self.tw.activity = self
        self.tw.A.spr.hide()        
        self.tw.L.spr.hide()
        self.tw.L2.spr.hide()
        self.tw.L2_tab_left.spr.hide()
        self.tw.L2_tab_right.spr.hide()
        self.tw.slider_on_top = "C"

    def set_title(self, title):
        self.win.set_title(title)

    def _c_cb(self, widget):
        self.tw.A.spr.hide()
        self.tw.L.spr.hide()
        self.tw.L2.spr.hide()
        self.tw.L2_tab_left.spr.hide()
        self.tw.L2_tab_right.spr.hide()
        self.tw.C.draw_slider(1000)
        self.tw.C_tab_left.draw_slider(1000)
        self.tw.C_tab_right.draw_slider(1000)
        self.tw.D.draw_slider(1000)
        self.tw.slider_on_top = "C"
        return True

    def _a_cb(self, widget):
        self.tw.C.spr.hide()
        self.tw.C_tab_left.spr.hide()
        self.tw.C_tab_right.spr.hide()
        self.tw.L.spr.hide()
        self.tw.L2.spr.hide()
        self.tw.L2_tab_left.spr.hide()
        self.tw.L2_tab_right.spr.hide()
        self.tw.A.draw_slider(1000)
        self.tw.D.draw_slider(1000)
        self.tw.slider_on_top = "A"
        return True

    def _l_cb(self, widget):
        self.tw.C.spr.hide()
        self.tw.A.spr.hide()
        self.tw.D.spr.hide()
        self.tw.C_tab_left.spr.hide()
        self.tw.C_tab_right.spr.hide()
        self.tw.L.draw_slider(1000)
        self.tw.L2.draw_slider(1000)
        self.tw.L2_tab_left.draw_slider(1000)
        self.tw.L2_tab_right.draw_slider(1000)
        self.tw.slider_on_top = "L"
        return True

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SlideruleMain()
    main()
