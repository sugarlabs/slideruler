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
_SLIDES = [_L, _C, _CI, _A, _K, _S, _T, _LL0, _LLn]

_D = _C
_DI = _CI
_L2 = _L
_B = _A
_K2 = _K
_S2 = _S
_T2 = _T
_LL02 = _LL0
_LLn2 = _LLn
_STATORS = [_L2, _D, _DI, _B, _K2, _S2, _T2, _LL0, _LLn2]


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

        # Read the slider positions from the Journal
        for name in ['C', 'CI', 'L', 'A', 'K', 'S', 'T', 'LLn', 'LL0']:
            if name in self.metadata:
                self.sr.name_to_slide(name).move(int(self.metadata[name]),
                    self.sr.slides[0].spr.get_xy()[1])
        if 'D' in self.metadata:
            self.move_stators(int(self.metadata['D']),
                              self.sr.name_to_stator('D').spr.get_xy()[1])
        if 'stator' in self.metadata:
            _logger.debug("restoring %s" % (self.metadata['stator']))
            self.sr.active_stator = self.sr.name_to_stator(
                self.metadata['stator'])
        if 'slide' in self.metadata:
            _logger.debug("restoring %s" % (self.metadata['slide']))
            self.sr.active_slide = self.sr.name_to_slide(
                self.metadata['slide'])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self.show_c()
        if 'R' in self.metadata:
            self.sr.reticule.move(int(self.metadata['R']),
                                  self.sr.reticule.spr.get_xy()[1])

    def write_file(self, file_path):
        """ Write the slide positions to the Journal """
        self.metadata['slide'] = self.sr.active_slide.name
        self.metadata['stator'] = self.sr.active_stator.name
        for name in ['C', 'CI', 'L', 'A', 'K', 'S', 'T', 'LLn', 'LL0']:
            self.metadata[name] = str(
                self.sr.name_to_slide(name).spr.get_xy()[0])
        self.metadata['D'] = str(self.sr.name_to_stator('D').spr.get_xy()[0])
        self.metadata['R'] = str(self.sr.reticule.spr.get_xy()[0])

    def _hide_all(self):
        self._hide_top()
        self._hide_bottom()

    def _hide_top(self):
        for slide in self.sr.slides:
            slide.hide()

    def _hide_bottom(self):
        for stator in self.sr.stators:
            stator.hide()

    def _show_slides(self, top, bottom, function):
        self._hide_all()
        self._top_combo.set_active(_SLIDES.index(top))
        self._set_top_slider()
        self._bottom_combo.set_active(_STATORS.index(bottom))
        self._set_bottom_slider()
        self._function_combo.set_active(_FUNCTIONS.index(function))
        self.sr.update_slide_labels()
        self.sr.update_results_label()

    def _set_top_slider(self):
        """ Move the top slider onto top layer """
        self._hide_top()
        self.sr.active_slide.draw()
        self.top_button.set_icon(self.sr.active_slide.name)

    def _set_bottom_slider(self):
        """ Move the bottom slider onto top layer """
        self._hide_bottom()
        self.sr.active_stator.draw()
        self.bottom_button.set_icon(self.sr.active_stator.name)

    def move_stators(self, x, y):
        """ Move all the stators to the same x, y position """
        for stator in self.sr.stators:
            stator.move(x, y)

    def _predefined_function(self):
        """ Return the predefined function that matches the sliders """
        if not hasattr(self, 'sr'):
            return None
        if self.sr.active_slide.name == 'C' and \
           self.sr.active_stator.name == 'D':
            return self.show_c
        elif self.sr.active_slide.name == 'CI' and \
             self.sr.active_stator.name == 'D':
            return self.show_ci
        elif self.sr.active_slide.name == 'A' and \
             self.sr.active_stator.name == 'D':
            return self.show_a
        elif self.sr.active_slide.name == 'K' and \
             self.sr.active_stator.name == 'D':
            return self.show_k
        elif self.sr.active_slide.name == 'S' and \
             self.sr.active_stator.name == 'D':
            return self.show_s
        elif self.sr.active_slide.name == 'T' and \
             self.sr.active_stator.name == 'D':
            return self.show_t
        elif self.sr.active_slide.name == 'L' and \
             self.sr.active_stator.name == 'L2':
            return self.show_l
        return None

    # Predefined functions
    def show_c(self):
        """ basic log scale """
        self.sr.active_slide = self.sr.name_to_slide('C')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_C, _D, _FC)

    def show_ci(self):
        """ inverse scale """
        self.sr.active_slide = self.sr.name_to_slide('CI')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_CI, _D, _FCI)

    def show_a(self):
        """ two-decade scale """
        self.sr.active_slide = self.sr.name_to_slide('A')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_A, _D, _FA)

    def show_k(self):
        """ three-decade scale """
        self.sr.active_slide = self.sr.name_to_slide('K')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_K, _D, _FK)

    def show_s(self):
        """ sine """
        self.sr.active_slide = self.sr.name_to_slide('S')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_S, _D, _FS)

    def show_t(self):
        """ tangent """
        self.sr.active_slide = self.sr.name_to_slide('T')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(_T, _D, _FT)

    def show_l(self):
        """ linear scale """
        self.sr.active_slide = self.sr.name_to_slide('L')
        self.sr.active_stator = self.sr.name_to_stator('L2')
        self._show_slides(_L, _L2, _FL)

    # toolbar button callbacks
    def realign_cb(self, arg=None):
        """ Realign all sliders with the D scale. """
        dx, dy = self.sr.name_to_stator('D').spr.get_xy()
        cy = self.sr.name_to_slide('C').spr.get_xy()[1]
        for slide in self.sr.slides:
            slide.move(dx, cy)
        self.move_stators(dx, dy)
        self.sr.update_slide_labels()
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
        """ Read value from slide combo box """
        _top_dictionary = {_C: 'C', _CI: 'CI', _A: 'A', _K: 'K', _S: 'S',
                           _T: 'T', _L: 'L', _LL0: 'LL0', _LLn: 'LLn'}
        self.sr.active_slide = self.sr.name_to_slide(_top_dictionary[
            _SLIDES[self._top_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UD))
            self._set_top_slider()
            self.sr.update_slide_labels()
            self.sr.update_results_label()

    def _bottom_combo_cb(self, arg=None):
        """ Read value from stator combo box """
        _bottom_dictionary = {_D: 'D', _DI: 'DI', _L2: 'L2', _B: 'B',
                              _K2: 'K2', _S2: 'S2', _T2: 'T2', _LL02: 'LL02',
                              _LLn2: 'LLn2'}
        self.sr.active_stator = self.sr.name_to_stator(_bottom_dictionary[
            _STATORS[self._bottom_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UD))
            self._set_bottom_slider()
            self.sr.update_slide_labels()
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
        self._function_combo = _combo_factory(_FUNCTIONS, _FC, _('functions'),
                                              self._function_combo_cb, toolbar)
        self.top_button = _button_factory('C', _('slide'),
                                          self._dummy_cb, toolbar)
        self._top_combo = _combo_factory(_SLIDES, _C, _('slides'),
                                         self._top_combo_cb, toolbar)
        self.bottom_button = _button_factory('D', _('stator'),
                                             self._dummy_cb, toolbar)
        self._bottom_combo = _combo_factory(_STATORS, _D, _('stators'),
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

