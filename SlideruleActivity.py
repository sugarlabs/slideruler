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

from window import SlideRule, move_slider_and_tabs, draw_slider_and_tabs, \
                   hide_slider_and_tabs
from constants import SWIDTH

_FA = _('square/square root')
_FC = _('multiply/divide')
_FCI = _('divide/multiply')
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
_LL0 = _('log log')
_LLn = _('ln')
_TOP_SCALES = [_L, _C, _CI, _A, _K, _S, _T, _LL0, _LLn]

_D = _C
_DI = _CI
_L2 = _L
_A2 = _A
_K2 = _K
_S2 = _S
_T2 = _T
_LL02 = _LL0
_LLn2 = _LLn
_BOT_SCALES = [_L2, _D, _DI, _A2, _K2, _S2, _T2, _LL0, _LLn2]


def _combo_factory(combo_array, default, tooltip, callback, toolbar):
    """Factory for making a toolbar combo box"""
    my_combo = ComboBox()
    if hasattr(my_combo, 'set_tooltip_text'):
        my_combo.set_tooltip_text(tooltip)

    my_combo.connect('changed', callback)

    for i, s in enumerate(combo_array):
        my_combo.append_item(i, s, None)
        # if s == default:
        #     my_combo.set_active(i)

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

        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(),
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        self.sr = SlideRule(canvas, os.path.join(activity.get_bundle_path(),
                                                 'images/'), self)

        # Rfead the slider positions from the Journal
        if 'C' in self.metadata:
            move_slider_and_tabs(self.sr.C, self.sr.C_tab_left,
                                 self.sr.C_tab_right,
                                 int(self.metadata['C']), 0)
        if 'CI' in self.metadata:
            move_slider_and_tabs(self.sr.CI, self.sr.CI_tab_left,
                                 self.sr.CI_tab_right,
                                 int(self.metadata['CI']), 0)
        if 'L' in self.metadata:
            move_slider_and_tabs(self.sr.L, self.sr.L_tab_left,
                                 self.sr.L_tab_right,
                                 int(self.metadata['L']), 0)
        if 'A' in self.metadata:
            move_slider_and_tabs(self.sr.A, self.sr.A_tab_left,
                                 self.sr.A_tab_right,
                                 int(self.metadata['A']), 0)
        if 'K' in self.metadata:
            move_slider_and_tabs(self.sr.K, self.sr.K_tab_left,
                                 self.sr.K_tab_right,
                                 int(self.metadata['K']), 0)
        if 'S' in self.metadata:
            move_slider_and_tabs(self.sr.S, self.sr.S_tab_left,
                                 self.sr.S_tab_right,
                                 int(self.metadata['S']), 0)
        if 'T' in self.metadata:
            move_slider_and_tabs(self.sr.T, self.sr.T_tab_left,
                                 self.sr.T_tab_right,
                                 int(self.metadata['T']), 0)
        if 'R' in self.metadata:
            move_slider_and_tabs(self.sr.R, self.sr.R_tab_top,
                                 self.sr.R_tab_bottom,
                                 int(self.metadata['R']), 0)
        if 'D' in self.metadata:
            Doffset = int(self.metadata['D'])
            self.sr.D.spr.move_relative((Doffset, 0))
            self.sr.DI.spr.move_relative((Doffset, 0))
            self.sr.L2.spr.move_relative((Doffset, 0))
            self.sr.A2.spr.move_relative((Doffset, 0))
            self.sr.K2.spr.move_relative((Doffset, 0))
            self.sr.S2.spr.move_relative((Doffset, 0))
            self.sr.T2.spr.move_relative((Doffset, 0))
        if 'slider' in self.metadata:
            _logger.debug("restoring %s" % (self.metadata['slider']))
            self.sr.slider_on_top = self.metadata['slider']
            if self.sr.slider_on_top == 'A':
                self.show_a()
            elif self.sr.slider_on_top == 'L':
                self.show_l()
            elif self.sr.slider_on_top == 'K':
                self.show_k()
            elif self.sr.slider_on_top == 'S':
                self.show_s()
            elif self.sr.slider_on_top == 'T':
                self.show_t()
            else:
                self.show_c()
        else:
            self.show_c()

    def write_file(self, file_path):
        """ Write the slider positions to the Journal """
        self.metadata['slider'] = self.sr.slider_on_top
        self.metadata['C'] = str(self.sr.C.spr.get_xy()[0])
        self.metadata['D'] = str(self.sr.D.spr.get_xy()[0])
        self.metadata['R'] = str(self.sr.R.spr.get_xy()[0])
        self.metadata['L'] = str(self.sr.L.spr.get_xy()[0])
        self.metadata['A'] = str(self.sr.A.spr.get_xy()[0])
        self.metadata['K'] = str(self.sr.K.spr.get_xy()[0])
        self.metadata['S'] = str(self.sr.S.spr.get_xy()[0])
        self.metadata['T'] = str(self.sr.T.spr.get_xy()[0])
        self.metadata['LLn'] = str(self.sr.LLn.spr.get_xy()[0])
        self.metadata['LL0'] = str(self.sr.LL0.spr.get_xy()[0])

    def _hide_all(self):
        self._hide_top()
        self._hide_bottom()

    def _hide_top(self):
        hide_slider_and_tabs(self.sr.C, self.sr.C_tab_left,
                             self.sr.C_tab_right)
        hide_slider_and_tabs(self.sr.CI, self.sr.CI_tab_left,
                             self.sr.CI_tab_right)
        hide_slider_and_tabs(self.sr.A, self.sr.A_tab_left,
                             self.sr.A_tab_right)
        hide_slider_and_tabs(self.sr.K, self.sr.K_tab_left,
                             self.sr.K_tab_right)
        hide_slider_and_tabs(self.sr.S, self.sr.S_tab_left,
                             self.sr.S_tab_right)
        hide_slider_and_tabs(self.sr.T, self.sr.T_tab_left,
                             self.sr.T_tab_right)
        hide_slider_and_tabs(self.sr.L, self.sr.L_tab_left,
                             self.sr.L_tab_right)
        hide_slider_and_tabs(self.sr.LLn, self.sr.LLn_tab_left,
                             self.sr.LLn_tab_right)
        hide_slider_and_tabs(self.sr.LL0, self.sr.LL0_tab_left,
                             self.sr.LL0_tab_right)

    def _hide_bottom(self):
        self.sr.D.spr.hide()
        self.sr.DI.spr.hide()
        self.sr.L2.spr.hide()
        self.sr.A2.spr.hide()
        self.sr.K2.spr.hide()
        self.sr.S2.spr.hide()
        self.sr.T2.spr.hide()
        self.sr.LLn2.spr.hide()
        self.sr.LL02.spr.hide()

    def _show_slides(self, top, bottom, function):
        self._hide_all()
        self._top_combo.set_active(_TOP_SCALES.index(top))
        self._set_top_slider()
        self._bottom_combo.set_active(_BOT_SCALES.index(bottom))
        self._set_bottom_slider()
        self._function_combo.set_active(_FUNCTIONS.index(function))
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _set_top_slider(self):
        """ Move the top slider onto top layer """
        self._hide_top()
        if self.sr.slider_on_top == 'C':
            draw_slider_and_tabs(self.sr.C, self.sr.C_tab_left,
                                 self.sr.C_tab_right)
        elif self.sr.slider_on_top == 'CI':
            draw_slider_and_tabs(self.sr.CI, self.sr.CI_tab_left,
                                 self.sr.CI_tab_right)
        elif self.sr.slider_on_top == 'A':
            draw_slider_and_tabs(self.sr.A, self.sr.A_tab_left,
                                 self.sr.A_tab_right)
        elif self.sr.slider_on_top == 'K':
            draw_slider_and_tabs(self.sr.K, self.sr.K_tab_left,
                                 self.sr.K_tab_right)
        elif self.sr.slider_on_top == 'S':
            draw_slider_and_tabs(self.sr.S, self.sr.S_tab_left,
                                 self.sr.S_tab_right)
        elif self.sr.slider_on_top == 'T':
            draw_slider_and_tabs(self.sr.T, self.sr.T_tab_left,
                                 self.sr.T_tab_right)
        elif self.sr.slider_on_top == 'L':
            draw_slider_and_tabs(self.sr.L, self.sr.L_tab_left,
                                 self.sr.L_tab_right)
        elif self.sr.slider_on_top == 'LLn':
            draw_slider_and_tabs(self.sr.LLn, self.sr.LLn_tab_left,
                                 self.sr.LLn_tab_right)
        elif self.sr.slider_on_top == 'LL0':
            draw_slider_and_tabs(self.sr.LL0, self.sr.LL0_tab_left,
                                 self.sr.LL0_tab_right)
        self.top_button.set_icon(self.sr.slider_on_top)

    def _set_bottom_slider(self):
        """ Move the bottom slider onto top layer """
        self._hide_bottom()
        if self.sr.slider_on_bottom == 'D':
            self.sr.D.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'DI':
            self.sr.DI.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'L2':
            self.sr.L2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'A2':
            self.sr.A2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'K2':
            self.sr.K2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'S2':
            self.sr.S2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'T2':
            self.sr.T2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'LLn2':
            self.sr.LLn2.draw_slider(1000)
        elif self.sr.slider_on_bottom == 'LL02':
            self.sr.LL02.draw_slider(1000)

        self.bottom_button.set_icon(self.sr.slider_on_bottom + 'on')

    def _predefined_function(self):
        """ Return the predefined function that matches the sliders """
        if not hasattr(self, 'sr'):
            return None
        if self.sr.slider_on_top == 'C' and self.sr.slider_on_bottom == 'D':
            return self.show_c
        elif self.sr.slider_on_top == 'CI' and self.sr.slider_on_bottom == 'D':
            return self.show_ci
        elif self.sr.slider_on_top == 'A' and self.sr.slider_on_bottom == 'D':
            return self.show_a
        elif self.sr.slider_on_top == 'K' and self.sr.slider_on_bottom == 'D':
            return self.show_k
        elif self.sr.slider_on_top == 'S' and self.sr.slider_on_bottom == 'D':
            return self.show_s
        elif self.sr.slider_on_top == 'T' and self.sr.slider_on_bottom == 'D':
            return self.show_t
        elif self.sr.slider_on_top == 'L' and self.sr.slider_on_bottom == 'L2':
            return self.show_l
        return None

    # Predefined functions
    def show_c(self):
        """ basic log scale """
        self.sr.slider_on_top = 'C'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_C, _D, _FC)
        self.sr.D.draw_slider(1000)

    def show_ci(self):
        """ Inverse scale """
        self.sr.slider_on_top = 'CI'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_CI, _D, _FCI)
        self.sr.D.draw_slider(1000)

    def show_a(self):
        """ two-decade scale """
        self.sr.slider_on_top = 'A'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_A, _D, _FA)
        self.sr.D.draw_slider(1000)

    def show_k(self):
        """ three-decade scale """
        self.sr.slider_on_top = 'K'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_K, _D, _FK)
        self.sr.D.draw_slider(1000)

    def show_s(self):
        """ Sine """
        self.sr.slider_on_top = 'S'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_S, _D, _FS)
        self.sr.D.draw_slider(1000)

    def show_t(self):
        """ Tangent """
        self.sr.slider_on_top = 'T'
        self.sr.slider_on_bottom = 'D'
        self._show_slides(_T, _D, _FT)
        self.sr.D.draw_slider(1000)

    def show_l(self):
        """ Linear scale """
        self.sr.slider_on_top = 'L'
        self.sr.slider_on_bottom = 'L2'
        self._show_slides(_L, _L2, _FL)
        self.sr.L.draw_slider(1000)

    def realign_cb(self, arg=None):
        """ Realign all sliders with the D scale. """
        dx, dy = self.sr.D.spr.get_xy()
        cx, cy = self.sr.C.spr.get_xy()
        ax, y = self.sr.A.spr.get_xy()
        cix, y = self.sr.CI.spr.get_xy()
        kx, y = self.sr.K.spr.get_xy()
        sx, y = self.sr.S.spr.get_xy()
        tx, y = self.sr.T.spr.get_xy()
        lx, y = self.sr.L.spr.get_xy()
        llnx, y = self.sr.LLn.spr.get_xy()
        ll0x, y = self.sr.LL0.spr.get_xy()
        self.sr.C.spr.move((dx, cy))
        self.sr.CI.spr.move((dx, cy))
        self.sr.A.spr.move((dx, cy))
        self.sr.K.spr.move((dx, cy))
        self.sr.S.spr.move((dx, cy))
        self.sr.T.spr.move((dx, cy))
        self.sr.L.spr.move((dx, cy))
        self.sr.LLn.spr.move((dx, cy))
        self.sr.A2.spr.move((dx, dy))
        self.sr.K2.spr.move((dx, dy))
        self.sr.S2.spr.move((dx, dy))
        self.sr.T2.spr.move((dx, dy))
        self.sr.DI.spr.move((dx, dy))
        self.sr.L2.spr.move((dx, dy))
        self.sr.LLn2.spr.move((dx, dy))
        self.sr.LL02.spr.move((dx, dy))
        self.sr.C_tab_left.spr.move_relative((dx-cx, 0))
        self.sr.C_tab_right.spr.move_relative((dx-cx, 0))
        self.sr.CI_tab_left.spr.move_relative((dx-cix, 0))
        self.sr.CI_tab_right.spr.move_relative((dx-cix, 0))
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
        self.sr.LLn_tab_left.spr.move_relative((dx-llnx, 0))
        self.sr.LLn_tab_right.spr.move_relative((dx-llnx, 0))
        self.sr.LL0_tab_left.spr.move_relative((dx-ll0x, 0))
        self.sr.LL0_tab_right.spr.move_relative((dx-ll0x, 0))
        self.sr.update_slider_labels()
        self.sr.update_results_label()

    def _function_combo_cb(self, arg=None):
        """ Read value from predefined-functions combo box """
        _functions_dictionary = {_FA: self.show_a, _FC: self.show_c,
                                 _FK: self.show_k, _FS: self.show_s,
                                 _FT: self.show_t, _FL: self.show_l,
                                 _FCI: self.show_ci}
        try:
            _functions_dictionary[
                _FUNCTIONS[self._function_combo.get_active()]]()
        except KeyError:
            # 'user defined'
            pass

    def _top_combo_cb(self, arg=None):
        """ Read value from top combo box """
        _top_dictionary = {_C: 'C', _CI: 'CI', _A: 'A', _K: 'K', _S: 'S',
                           _T: 'T', _L: 'L', _LL0: 'LL0', _LLn: 'LLn'}
        self.sr.slider_on_top = _top_dictionary[
            _TOP_SCALES[self._top_combo.get_active()]]
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UD))
            self._set_top_slider()
            self.sr.update_slider_labels()
            self.sr.update_results_label()

    def _bottom_combo_cb(self, arg=None):
        """ Read value from bottom combo box """
        _bottom_dictionary = {_D: 'D', _DI: 'DI', _L2: 'L2', _A2: 'A2',
                              _K2: 'K2', _S2: 'S2', _T2: 'T2', _LL02: 'LL02',
                              _LLn2: 'LLn2'}
        self.sr.slider_on_bottom = _bottom_dictionary[
            _BOT_SCALES[self._bottom_combo.get_active()]]
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UD))
            self._set_bottom_slider()
            self.sr.update_slider_labels()
            self.sr.update_results_label()

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
        self._function_combo = _combo_factory(_FUNCTIONS, _FC, _('function'),
                                              self._function_combo_cb, toolbar)
        self.top_button = _button_factory('Con', _('top scale'),
                                          self._dummy_cb, toolbar)
        self._top_combo = _combo_factory(_TOP_SCALES, _C, _('top scale'),
                                         self._top_combo_cb, toolbar)
        self.bottom_button = _button_factory('Don', _('bottom scale'),
                                             self._dummy_cb, toolbar)
        self._bottom_combo = _combo_factory(_BOT_SCALES, _D, _('bot scale'),
                                         self._bottom_combo_cb, toolbar)
        _separator_factory(toolbox.toolbar)
        self.realign_button = _button_factory('realign', _('realign slides'),
                                             self.realign_cb, toolbar)

        if _have_toolbox:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()

