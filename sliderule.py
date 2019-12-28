#!/usr/bin/env python

#Copyright (c) 2009, 2010 Walter Bender
#Copyright (c) 2012 Ignacio Rodriguez

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA
from gi.repository import Gtk, Gdk, GdkPixbuf

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

        self.win = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.win.maximize()
        self.win.set_title(_('Sliderule'))
        self.win.connect('delete_event', lambda w,e: Gtk.main_quit())

        menu = Gtk.Menu()
        menu_items = Gtk.MenuItem(_("L") + ' ' + _FL)
        menu.append(menu_items)
        menu_items.connect("activate", self._l_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("C") + ' ' + _FC)
        menu.append(menu_items)
        menu_items.connect("activate", self._c_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("CI") + ' ' + _FCI)
        menu.append(menu_items)
        menu_items.connect("activate", self._ci_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("A") + ' ' + _FA)
        menu.append(menu_items)
        menu_items.connect("activate", self._a_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("K") + ' ' + _FK)
        menu.append(menu_items)
        menu_items.connect("activate", self._k_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("S") + ' ' + _FS)
        menu.append(menu_items)
        menu_items.connect("activate", self._s_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("T") + ' ' + _FT)
        menu.append(menu_items)
        menu_items.connect("activate", self._t_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("realign slides"))
        menu.append(menu_items)
        menu_items.connect("activate", self._realign_cb)
        menu_items.show()
        menu_items = Gtk.MenuItem(_("Quit"))
        menu.append(menu_items)
        menu_items.connect("activate", self._quit_cb)
        menu_items.show()
        root_menu = Gtk.MenuItem("Tools")
        root_menu.show()
        root_menu.set_submenu(menu)

        menu.show()
        self.menu_bar = Gtk.MenuBar()
        self.menu_bar.append(root_menu)
        self.menu_bar.show()
        self.menu_height = self.menu_bar.size_request().height

        vbox = Gtk.VBox(False, 0)
        self.win.add(vbox)
        vbox.show()

        self.fixed = Gtk.Fixed()
        self.fixed.connect('size-allocate', self._fixed_resize_cb)
        width = Gdk.Screen.width() - 80
        height = Gdk.Screen.height() - 60
        self.fixed.set_size_request(width, height)
        vbox.pack_start(self.fixed, True, True, 0)

        self.vbox = Gtk.VBox(False, 0)
        self.vbox.show()

        self.vbox.pack_start(self.menu_bar, False, False, 2)

        canvas = Gtk.DrawingArea()
        width = Gdk.Screen.width() - 80
        height = Gdk.Screen.height() - 60
        canvas.set_size_request(width, height)
        canvas.show()
        self.vbox.pack_end(canvas, True, True, 0)
        self.fixed.put(self.vbox, 0, 0)
        self.fixed.show()
        self.win.show_all()

        self.sr = SlideRule(canvas,
                            os.path.join(os.path.abspath('.'), 'images/'),
                            parent=self, sugar=False)
        self.sr.win = self.win
        self.sr.activity = self
        self.hide_all()
        self._c_cb(None)

    def show_all(self):
        self.win.show_all()

    def _fixed_resize_cb(self, widget=None, rect=None):
        ''' If a toolbar opens or closes, we need to resize the vbox
        holding out scrolling window. '''
        self.vbox.set_size_request(rect.width, rect.height)
        if hasattr(self, 'sr'):
            self.sr.update_textview_y_offset(-self.menu_height)
        self.menu_height = self.menu_bar.size_request().height
        if hasattr(self, 'sr'):
            self.sr.update_textview_y_offset(self.menu_height)

    def set_title(self, title):
        self.win.set_title(title)

    def hide_all(self):
        for slide in self.sr.slides:
            slide.hide()
        for stator in self.sr.stators:
            stator.hide()

    def _realign_cb(self, arg=None):
        """ Realign all sliders with the D scale. """
        dx, dy = self.sr.name_to_stator('D').spr.get_xy()
        cy = self.sr.name_to_slide('C').spr.get_xy()[1]
        for slide in self.sr.slides:
            slide.move(dx, cy)
        self.sr.move_stators(dx, dy)

    def _show(self):
        self.sr.active_slide.draw()
        self.sr.active_stator.draw()
        if hasattr(self.sr, "update_slider_labels"):
            self.sr.update_slider_labels()
            self.sr.update_results_label()

    def _c_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('C')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _ci_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('CI')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _a_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('A')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _k_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('K')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _s_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('S')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _t_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('T')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show()
        return True

    def _l_cb(self, widget):
        self.hide_all()
        self.sr.active_slide = self.sr.name_to_slide('L')
        self.sr.active_stator = self.sr.name_to_stator('L2')
        self._show()
        return True

    def _quit_cb(self, widget):
        Gtk.main_quit()
        exit()


def main():
    Gtk.main()
    return 0

if __name__ == "__main__":
    SlideruleMain()
    main()
