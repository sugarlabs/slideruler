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
try:
    from sugar.graphics.toolbarbox import ToolbarBox
    _have_toolbox = True
except ImportError:
    _have_toolbox = False

if _have_toolbox:
    from sugar.bundle.activitybundle import ActivityBundle
    from sugar.activity.widgets import ActivityToolbarButton
    from sugar.activity.widgets import StopButton
    from sugar.graphics.toolbarbox import ToolbarButton

from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.menuitem import MenuItem
from sugar.graphics.icon import Icon
from sugar.datastore import datastore

from gettext import gettext as _
import locale
import os.path

import logging
_logger = logging.getLogger('sliderule-activity')

from window import SlideRule
from constants import SWIDTH


def _button_factory(icon_name, tooltip, callback, toolbar, cb_arg=None,
                    accelerator=None):
    """Factory for making toolbar buttons"""
    my_button = ToolButton(icon_name)
    my_button.set_tooltip(tooltip)
    my_button.props.sensitive = True
    if accelerator is not None:
        my_button.props.accelerator = accelerator
    if cb_arg is not None:
        my_button.connect('clicked', callback, cb_arg)
    else:
        my_button.connect('clicked', callback)
    if hasattr(toolbar, 'insert'):  # the main toolbar
        toolbar.insert(my_button, -1)
    else:  # or a secondary toolbar
        toolbar.props.page.insert(my_button, -1)
    my_button.show()
    return my_button


def _separator_factory(toolbar, visible=True, expand=False):
    """ Factory for adding a separator to a toolbar """
    _separator = gtk.SeparatorToolItem()
    _separator.props.draw = visible
    _separator.set_expand(expand)
    toolbar.insert(_separator, -1)
    _separator.show()


class SlideruleActivity(activity.Activity):
    """ A sliderul activity for Sugar """

    def __init__(self, handle):
        super(SlideruleActivity,self).__init__(handle)

        self._setup_toolbars(_have_toolbox)

        # Create a canvas
        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(),
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        # Initialize the canvas
        self.sr = SlideRule(canvas, os.path.join(activity.get_bundle_path(),
                                                 'images/'), self)

        # Read the slider positions from the Journal
        if 'L' in self.metadata:
            self.sr.L.spr.move_relative((int(self.metadata['L']), 0))
        if 'L2' in self.metadata:
            self.sr.L2.spr.move_relative((int(self.metadata['L2']), 0))
            self.sr.L2_tab_left.spr.move_relative((int(self.metadata['L2']), 0))
            self.sr.L2_tab_right.spr.move_relative((int(self.metadata['L2']) +\
                                                   SWIDTH - 100, 0))
        if 'A' in self.metadata:
            self.sr.A.spr.move_relative((int(self.metadata['A']), 0))
        if 'K' in self.metadata:
            self.sr.K.spr.move_relative((int(self.metadata['K']), 0))
        if 'S' in self.metadata:
            self.sr.S.spr.move_relative((int(self.metadata['S']), 0))
        if 'D' in self.metadata:
            self.sr.D.spr.move_relative((int(self.metadata['D']), 0))
        if 'C' in self.metadata:
            self.sr.C.spr.move_relative((int(self.metadata['C']), 0))
            self.sr.C_tab_left.spr.move_relative((int(self.metadata['C']), 0))
            self.sr.C_tab_right.spr.move_relative((int(self.metadata['C']) + \
                                                   SWIDTH - 100, 0))
        if 'CI' in self.metadata:
            self.sr.CI.spr.move_relative((int(self.metadata['CI']), 0))
            self.sr.CI_tab_left.spr.move_relative((int(self.metadata['CI']), 0))
            self.sr.CI_tab_right.spr.move_relative((int(self.metadata['CI']) + \
                                                   SWIDTH - 100, 0))
        if 'R' in self.metadata:
            self.sr.R.spr.move_relative((int(self.metadata['R']), 0))
            self.sr.R_tab_top.spr.move_relative((int(self.metadata['R']), 0))
            self.sr.R_tab_bot.spr.move_relative((int(self.metadata['R']), 0))
        if 'slider' in self.metadata:
            self.sr.slider_on_top = self.metadata['slider']
            if self.sr.slider_on_top == 'A':
                self._show_a()
            elif self.sr.slider_on_top == 'L':
                self._show_l()
            elif self.sr.slider_on_top == 'CI':
                self._show_ci()
            else:
                self._show_c()
            self.sr.update_results_label()
            self.sr.update_slider_labels()

    def _hide_all(self):
        self.a_slider.set_icon('Aoff')
        self.k_slider.set_icon('Koff')
        self.s_slider.set_icon('Soff')
        self.c_slider.set_icon('Coff')
        self.ci_slider.set_icon('CIoff')
        self.l_slider.set_icon('Loff')
        self.sr.A.spr.hide()
        self.sr.K.spr.hide()
        self.sr.S.spr.hide()
        self.sr.C.spr.hide()
        self.sr.CI.spr.hide()
        self.sr.C_tab_left.spr.hide()
        self.sr.C_tab_right.spr.hide()
        self.sr.CI_tab_left.spr.hide()
        self.sr.CI_tab_right.spr.hide()
        self.sr.D.spr.hide()
        self.sr.L.spr.hide()
        self.sr.L2.spr.hide()
        self.sr.L2_tab_left.spr.hide()
        self.sr.L2_tab_right.spr.hide()

    def _c_slider_cb(self, button):
        self._show_c()
        return True

    def _show_c(self):
        self._hide_all()
        self.c_slider.set_icon('Con')
        self.sr.C.draw_slider(1000)
        self.sr.C_tab_left.draw_slider(1000)
        self.sr.C_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'C'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _ci_slider_cb(self, button):
        self._show_ci()
        return True

    def _show_ci(self):
        self._hide_all()
        self.ci_slider.set_icon('CIon')
        self.sr.CI.draw_slider(1000)
        self.sr.CI_tab_left.draw_slider(1000)
        self.sr.CI_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'CI'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _a_slider_cb(self, button):
        self._show_a()
        return True

    def _show_a(self):
        self._hide_all()
        self.a_slider.set_icon('Aon')
        self.sr.A.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'A'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _k_slider_cb(self, button):
        self._show_k()
        return True

    def _show_k(self):
        self._hide_all()
        self.k_slider.set_icon('Kon')
        self.sr.K.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'K'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _s_slider_cb(self, button):
        self._show_s()
        return True

    def _show_s(self):
        self._hide_all()
        self.s_slider.set_icon('Son')
        self.sr.S.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'S'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _l_slider_cb(self, button):
        self._show_l()
        return True

    def _show_l(self):
        self._hide_all()
        self.l_slider.set_icon('Lon')
        self.sr.L.draw_slider(1000)
        self.sr.L2.draw_slider(1000)
        self.sr.L2_tab_left.draw_slider(1000)
        self.sr.L2_tab_right.draw_slider(1000)
        self.sr.slider_on_top = 'L'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    """
    Write the slider positions to the Journal
    """
    def write_file(self, file_path):
        self.metadata['slider'] = self.sr.slider_on_top
        x, y = self.sr.A.spr.get_xy()
        self.metadata['A'] = str(x)
        x, y = self.sr.K.spr.get_xy()
        self.metadata['K'] = str(x)
        x, y = self.sr.S.spr.get_xy()
        self.metadata['S'] = str(x)
        x, y = self.sr.C.spr.get_xy()
        self.metadata['C'] = str(x)
        x, y = self.sr.CI.spr.get_xy()
        self.metadata['CI'] = str(x)
        x, y = self.sr.D.spr.get_xy()
        self.metadata['D'] = str(x)
        x, y = self.sr.R.spr.get_xy()
        self.metadata['R'] = str(x)
        x, y = self.sr.L.spr.get_xy()
        self.metadata['L'] = str(x)
        x, y = self.sr.L2.spr.get_xy()
        self.metadata['L2'] = str(x)

    def _setup_toolbars(self, have_toolbox):
        """ Setup the toolbars.. """

        if have_toolbox:
            toolbox = ToolbarBox()

            # Activity toolbar
            activity_button = ActivityToolbarButton(self)

            toolbox.toolbar.insert(activity_button, 0)
            activity_button.show()

            self.set_toolbar_box(toolbox)
            toolbox.show()
            toolbar = toolbox.toolbar

        else:
            # Use pre-0.86 toolbar design
            project_toolbar = gtk.Toolbar()
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.add_toolbar(_('Project'), project_toolbar)
            toolbox.show()
            toolbox.set_current_toolbar(1)
            toolbar = project_toolbar

        # Add the buttons to the toolbars
        self.l_slider = _button_factory('Loff', _('add/subtract'),
                                        self._l_slider_cb, toolbar)
        self.c_slider = _button_factory('Con', _('multiply/divide'),
                                        self._c_slider_cb, toolbar)
        self.ci_slider = _button_factory('CIoff', _('inverse'),
                                        self._ci_slider_cb, toolbar)
        self.a_slider = _button_factory('Aoff', _('square/square root'),
                                        self._a_slider_cb, toolbar)
        self.k_slider = _button_factory('Koff', _('cube/cube root'),
                                        self._k_slider_cb, toolbar)
        self.s_slider = _button_factory('Soff', _('sin, asin'),
                                        self._s_slider_cb, toolbar)

        if _have_toolbox:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

