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

from sugar.graphics.combobox import ComboBox
from sugar.graphics.toolcombobox import ToolComboBox
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

_FA = _('square/square root')
_FC = _('multiply/divide')
_FCI = _('inverse')
_FK = _('cube/cube root')
_FS = _('sin, asin')
_FT = _('tan, atan')
_FL = _('add/subtract')
_UD = _('user defined')
_FUNCTIONS = [_FL, _FC, _FCI, _FA, _FK, _FS, _FT, _UD]

_A = _('log²')
_C = _('log')
_CI = _('1/log')
_K = _('log³')
_S = _('sin')
_T = _('tan')
_L = _('linear')
_TOP_SCALES = [_L, _C, _CI, _A, _K, _S, _T]

_D = _('log')
_CI2 = _('1/log')
_L2 = _('linear')
_BOT_SCALES = [_L2, _D, _CI2]


def _combo_factory(combo_array, default, tooltip, callback, toolbar):
    """Factory for making a toolbar combo box"""
    my_combo = ComboBox()
    if hasattr(my_combo, 'set_tooltip_text'):
        my_combo.set_tooltip_text(tooltip)

    my_combo.connect('changed', callback)

    for i, s in enumerate(combo_array):
        my_combo.append_item(i, s, None)
        if s == default:
            my_combo.set_active(i)

    toolbar.insert(ToolComboBox(my_combo), -1)
    return my_combo


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


def _label_factory(label, toolbar):
    """ Factory for adding a label to a toolbar """
    my_label = gtk.Label(label)
    my_label.set_line_wrap(True)
    my_label.show()
    _toolitem = gtk.ToolItem()
    _toolitem.add(my_label)
    toolbar.insert(_toolitem, -1)
    _toolitem.show()
    return my_label


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
        if 'D' in self.metadata:
            Doffset = int(self.metadata['D'])
            self.sr.D.spr.move_relative((Doffset, 0))
            self.sr.A.spr.move_relative((Doffset, 0))
            self.sr.K.spr.move_relative((Doffset, 0))
            self.sr.S.spr.move_relative((Doffset, 0))
            self.sr.T.spr.move_relative((Doffset, 0))
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
            _logger.debug("restoring %s" % (self.metadata['slider']))
            self.sr.slider_on_top = self.metadata['slider']
            if self.sr.slider_on_top == 'A':
                self._show_a()
            elif self.sr.slider_on_top == 'L':
                self._show_l()
            elif self.sr.slider_on_top == 'K':
                self._show_k()
            elif self.sr.slider_on_top == 'S':
                self._show_s()
            elif self.sr.slider_on_top == 'T':
                self._show_t()
            elif self.sr.slider_on_top == 'CI':
                self._show_ci()
            else:
                self._show_c()
            self.sr.update_results_label()
            self.sr.update_slider_labels()

    def write_file(self, file_path):
        """ Write the slider positions to the Journal """
        self.metadata['slider'] = self.sr.slider_on_top
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

    def _hide_all(self):
        self.sr.A.spr.hide()
        self.sr.K.spr.hide()
        self.sr.S.spr.hide()
        self.sr.T.spr.hide()
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

    def _show_c(self):
        self._hide_all()
        self.t_button.set_icon('Con')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_C))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FC))
        self.sr.C.draw_slider(1000)
        self.sr.C_tab_left.draw_slider(1000)
        self.sr.C_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'C'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_ci(self):
        self._hide_all()
        self.t_button.set_icon('CIon')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_CI))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FCI))
        self.sr.CI.draw_slider(1000)
        self.sr.CI_tab_left.draw_slider(1000)
        self.sr.CI_tab_right.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'CI'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_a(self):
        self._hide_all()
        self.t_button.set_icon('Aon')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_A))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FA))
        self.sr.A.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'A'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_k(self):
        self._hide_all()
        self.t_button.set_icon('Kon')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_K))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FK))
        self.sr.K.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'K'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_s(self):
        self._hide_all()
        self.t_button.set_icon('Son')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_S))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FS))
        self.sr.S.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'S'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_t(self):
        self._hide_all()
        self.t_button.set_icon('Ton')
        self.b_button.set_icon('Don')
        self._top_combo.set_active(_TOP_SCALES.index(_T))
        self._bot_combo.set_active(_BOT_SCALES.index(_D))
        self._function_combo.set_active(_FUNCTIONS.index(_FT))
        self.sr.T.draw_slider(1000)
        self.sr.D.draw_slider(1000)
        self.sr.slider_on_top = 'T'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _show_l(self):
        self._hide_all()
        self.t_button.set_icon('Lon')
        self.b_button.set_icon('Lon')
        self._top_combo.set_active(_TOP_SCALES.index(_L))
        self._bot_combo.set_active(_BOT_SCALES.index(_L2))
        self._function_combo.set_active(_FUNCTIONS.index(_FL))
        self.sr.L.draw_slider(1000)
        self.sr.L2.draw_slider(1000)
        self.sr.L2_tab_left.draw_slider(1000)
        self.sr.L2_tab_right.draw_slider(1000)
        self.sr.slider_on_top = 'L'
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _top_combo_cb(self, arg=None):
        """ Read value from top combo box """
        top_dictionary = {_A: self._show_a, _C: self._show_c, _K: self._show_k,
                          _S: self._show_s, _T: self._show_t, _L: self._show_l, 
                          _CI: self._show_ci} 
        if hasattr(self, '_top_combo'):
            top_dictionary[_TOP_SCALES[self._top_combo.get_active()]]()
        else:
            _logger.debug("no top_combo yet")

    def _fun_combo_cb(self, arg=None):
        """ Read value from function combo box """
        fun_dictionary = {_FA: self._show_a, _FC: self._show_c,
                          _FK: self._show_k, _FS: self._show_s,
                          _FT: self._show_t, _FL: self._show_l, 
                          _FCI: self._show_ci} 
        if hasattr(self, '_function_combo'):
            fun_dictionary[_FUNCTIONS[self._function_combo.get_active()]]()
        else:
            _logger.debug("no function_combo yet")


    def _bot_combo_cb(self, arg=None):
        #TODO: reset function combo
        return

    def _dummy_cb(self, arg=None):
        return

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
        self.t_button = _button_factory('Con', _('top scale'), self._dummy_cb,
                                        toolbar)
        self._top_combo = _combo_factory(_TOP_SCALES, _C, _('top scale'),
                                         self._top_combo_cb, toolbar)
        self.b_button = _button_factory('Don', _('bottom scale'),
                                        self._dummy_cb, toolbar)
        self._bot_combo = _combo_factory(_BOT_SCALES, _D, _('bot scale'),
                                         self._bot_combo_cb, toolbar)
        _separator_factory(toolbar)
        self._function_combo = _combo_factory(_FUNCTIONS, _FC, _('function'),
                                              self._fun_combo_cb, toolbar)

        if _have_toolbox:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

