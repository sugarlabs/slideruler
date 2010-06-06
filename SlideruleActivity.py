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
import gobject

import sugar
from sugar.activity import activity
try: # 0.86+ toolbar widgets
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarBox
    from sugar.graphics.toolbarbox import ToolbarButton
except ImportError:
    pass
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

from gettext import gettext as _
import locale
import os.path

import logging
_logger = logging.getLogger("sliderule-activity")

from sprites import *
import window
from constants import *

#
# Sugar activity
#
class SlideruleActivity(activity.Activity):

    def __init__(self, handle):
        super(SlideruleActivity,self).__init__(handle)

        try:
            # Use 0.86 toolbar design
            toolbar_box = ToolbarBox()

            # Buttons added to the Activity toolbar
            activity_button = ActivityToolbarButton(self)
            toolbar_box.toolbar.insert(activity_button, 0)
            activity_button.show()

            # C slider
            self.c_slider = ToolButton( "Con" )
            self.c_slider.set_tooltip(_('C'))
            self.c_slider.props.sensitive = True
            self.c_slider.connect('clicked', self._c_slider_cb)
            toolbar_box.toolbar.insert(self.c_slider, -1)
            self.c_slider.show()

            # A slider
            self.a_slider = ToolButton( "Aoff" )
            self.a_slider.set_tooltip(_('A'))
            self.a_slider.props.sensitive = True
            self.a_slider.connect('clicked', self._a_slider_cb)
            toolbar_box.toolbar.insert(self.a_slider, -1)
            self.a_slider.show()

            # L slider
            self.l_slider = ToolButton( "Loff" )
            self.l_slider.set_tooltip(_('L'))
            self.l_slider.props.sensitive = True
            self.l_slider.connect('clicked', self._l_slider_cb)
            toolbar_box.toolbar.insert(self.l_slider, -1)
            self.l_slider.show()

            # Label for showing status
            self.results_label = gtk.Label("1.0 × 1.0 = 1.0")
            self.results_label.show()
            results_toolitem = gtk.ToolItem()
            results_toolitem.add(self.results_label)
            toolbar_box.toolbar.insert(results_toolitem,-1)

            separator = gtk.SeparatorToolItem()
            separator.props.draw = False
            separator.set_expand(True)
            separator.show()
            toolbar_box.toolbar.insert(separator, -1)

            # The ever-present Stop Button
            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>Q'
            toolbar_box.toolbar.insert(stop_button, -1)
            stop_button.show()

            self.set_toolbar_box(toolbar_box)
            toolbar_box.show()

        except NameError:
            # Use pre-0.86 toolbar design
            self.toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(self.toolbox)

            self.projectToolbar = ProjectToolbar(self)
            self.toolbox.add_toolbar( _('Project'), self.projectToolbar )

            self.toolbox.show()

        # Create a canvas
        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(), \
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        # Initialize the canvas
        self.tw = window.new_window(canvas, \
                                    os.path.join(activity.get_bundle_path(), \
                                                 'images/'), \
                                    self)

        # Read the slider positions from the Journal
        try:
            self.tw.L.spr.move_relative((int(self.metadata['L']),0))
            self.tw.L2.spr.move_relative((int(self.metadata['L2']),0))
            self.tw.L2_tab_left.spr.move_relative((int(self.metadata['L2']),0))
            self.tw.L2_tab_right.spr.move_relative((int(self.metadata['L2'])+\
                                                   SWIDTH-100,0))
        except:
            pass
        try:
            self.tw.A.spr.move_relative((int(self.metadata['A']),0))
            self.tw.C.spr.move_relative((int(self.metadata['C']),0))
            self.tw.C_tab_left.spr.move_relative((int(self.metadata['C']),0))
            self.tw.C_tab_right.spr.move_relative((int(self.metadata['C'])+\
                                                   SWIDTH-100,0))
            self.tw.D.spr.move_relative((int(self.metadata['D']),0))
            self.tw.R.spr.move_relative((int(self.metadata['R']),0))
            self.tw.R_tab_top.spr.move_relative((int(self.metadata['R']),0))
            self.tw.R_tab_bot.spr.move_relative((int(self.metadata['R']),0))
            self.tw.slider_on_top = self.metadata['slider']
            if self.tw.slider_on_top == 'A':
                self._show_a()
            elif self.tw.slider_on_top == 'L':
                self._show_l()
            else:
                self._show_c()
            window._update_results_label(self.tw)
            window._update_slider_labels(self.tw)
        except:
            self._show_c()

    def _hide_all(self):
        self.a_slider.set_icon("Aoff")
        self.c_slider.set_icon("Coff")
        self.l_slider.set_icon("Loff")
        self.tw.A.spr.hide()
        self.tw.C.spr.hide()
        self.tw.C_tab_left.spr.hide()
        self.tw.C_tab_right.spr.hide()
        self.tw.D.spr.hide()
        self.tw.L.spr.hide()
        self.tw.L2.spr.hide()
        self.tw.L2_tab_left.spr.hide()
        self.tw.L2_tab_right.spr.hide()

    def _c_slider_cb(self, button):
        self._show_c()
        return True

    def _show_c(self):
        self._hide_all()
        self.c_slider.set_icon("Con")
        self.tw.C.draw_slider(1000)
        self.tw.C_tab_left.draw_slider(1000)
        self.tw.C_tab_right.draw_slider(1000)
        self.tw.D.draw_slider(1000)
        self.tw.slider_on_top = "C"

    def _a_slider_cb(self, button):
        self._show_a()
        return True

    def _show_a(self):
        self._hide_all()
        self.a_slider.set_icon("Aon")
        self.tw.A.draw_slider(1000)
        self.tw.D.draw_slider(1000)
        self.tw.slider_on_top = "A"
        return True

    def _l_slider_cb(self, button):
        self._show_l()
        return True

    def _show_l(self):
        self._hide_all()
        self.l_slider.set_icon("Lon")
        self.tw.L.draw_slider(1000)
        self.tw.L2.draw_slider(1000)
        self.tw.L2_tab_left.draw_slider(1000)
        self.tw.L2_tab_right.draw_slider(1000)
        self.tw.slider_on_top = "L"

    """
    Write the slider positions to the Journal
    """
    def write_file(self, file_path):
        _logger.debug("Write slider on top: " + self.tw.slider_on_top)
        self.metadata['slider'] = self.tw.slider_on_top
        x,y = self.tw.A.spr.get_xy()
        _logger.debug("Write A offset: " + str(x))
        self.metadata['A'] = str(x)
        x,y = self.tw.C.spr.get_xy()
        _logger.debug("Write C offset: " + str(x))
        self.metadata['C'] = str(x)
        x,y = self.tw.D.spr.get_xy()
        _logger.debug("Write D offset: " + str(x))
        self.metadata['D'] = str(x)
        x,y = self.tw.R.spr.get_xy()
        _logger.debug("Write r offset: " + str(x))
        self.metadata['R'] = str(x)
        x,y = self.tw.L.spr.get_xy()
        _logger.debug("Write L offset: " + str(x))
        self.metadata['L'] = str(x)
        x,y = self.tw.L2.spr.get_xy()
        _logger.debug("Write L2 offset: " + str(x))
        self.metadata['L2'] = str(x)


#
# Project toolbar for pre-0.86 toolbars
#
class ProjectToolbar(gtk.Toolbar):

    def __init__(self, pc):
        gtk.Toolbar.__init__(self)
        self.activity = pc

        # C slider
        self.activity.c_slider = ToolButton( "Con" )
        self.activity.c_slider.set_tooltip(_('C'))
        self.activity.c_slider.props.sensitive = True
        self.activity.c_slider.connect('clicked', self.activity._c_slider_cb)
        self.insert(self.activity.c_slider, -1)
        self.activity.c_slider.show()

        # A slider
        self.activity.a_slider = ToolButton( "Aoff" )
        self.activity.a_slider.set_tooltip(_('A'))
        self.activity.a_slider.props.sensitive = True
        self.activity.a_slider.connect('clicked', self.activity._a_slider_cb)
        self.insert(self.activity.a_slider, -1)
        self.activity.a_slider.show()

        # L slider
        self.activity.l_slider = ToolButton( "Loff" )
        self.activity.l_slider.set_tooltip(_('L'))
        self.activity.l_slider.props.sensitive = True
        self.activity.l_slider.connect('clicked', self.activity._l_slider_cb)
        self.insert(self.activity.l_slider, -1)
        self.activity.l_slider.show()

        # Label for showing status
        self.activity.results_label = gtk.Label("1.0 × 1.0 = 1.0")
        self.activity.results_label.show()
        self.activity.results_toolitem = gtk.ToolItem()
        self.activity.results_toolitem.add(self.activity.results_label)
        self.insert(self.activity.results_toolitem, -1)
        self.activity.results_toolitem.show()
