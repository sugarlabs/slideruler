#!/usr/bin/env python

#Copyright (c) 2009, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

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
        self.tw.slider_on_top = "C"

    def set_title(self, title):
        self.win.set_title(title)

    def _c_cb(self, widget):
        self.tw.A.spr.hide()
        self.tw.C.draw_slider(1000)
        self.tw.C_tab_left.draw_slider(1000)
        self.tw.C_tab_right.draw_slider(1000)
        self.tw.slider_on_top = "C"
        return True

    def _a_cb(self, widget):
        self.tw.C.spr.hide()
        self.tw.C_tab_left.spr.hide()
        self.tw.C_tab_right.spr.hide()
        self.tw.A.draw_slider(1000)
        self.tw.slider_on_top = "A"
        return True

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    SlideruleMain()
    main()
