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
from constants import SWIDTH, SLIDE, STATOR, CUSTOM

_FA = _('square/square root')
_FC = _('multiply/divide')
_FCI = _('divide/multiply')
_FK = _('cube/cube root')
_FS = _('sin, asin')
_FT = _('tan, atan')
_FL = _('add/subtract')
_FE = _('natural log')
_UK = '-'
_FUNCTIONS = [_FL, _FC, _FCI, _FA, _FK, _FS, _FT, _FE, _UK]

_A = _('log²')
_C = _('log')
_CI = _('1/log')
_K = _('log³')
_S = _('sin')
_T = _('tan')
_L = _('linear')
# _LL0 = _('log log')
_Log = _('log log')
_LLn = _('ln')
_UD = _('user defined')
_SLIDES = [_L, _C, _CI, _A, _K, _S, _T, _Log, _LLn, _UD]

_D = _C
_DI = _CI
_B = _A
_STATORS = [_L, _D, _DI, _B, _K, _S, _T, _Log, _LLn, _UD]

_SLIDE_DICTIONARY = {_C: 'C', _CI: 'CI', _A: 'A', _K: 'K', _S: 'S', _T: 'T',
                     _L: 'L', _Log: 'Log', _LLn: 'LLn', _UD: 'custom'}

_STATOR_DICTIONARY = {_D: 'D', _DI: 'DI', _L: 'L2', _B: 'B', _K: 'K2',
                      _S: 'S2', _T: 'T2', _Log: 'Log2', _LLn: 'LLn2',
                      _UD: 'custom2'}

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


def _entry_factory(default_string, toolbar, tooltip='', max=14):
    """ Factory for adding a text box to a toolbar """
    my_entry = gtk.Entry()
    my_entry.set_text(default_string)
    if hasattr(my_entry, 'set_tooltip_text'):
        my_entry.set_tooltip_text(tooltip)
    my_entry.set_width_chars(max)
    my_entry.show()
    _toolitem = gtk.ToolItem()
    _toolitem.add(my_entry)
    toolbar.insert(_toolitem, -1)
    _toolitem.show()
    return my_entry


def _separator_factory(toolbar, visible=True, expand=False):
    """ Factory for adding a separator to a toolbar """
    _separator = gtk.SeparatorToolItem()
    _separator.props.draw = visible
    _separator.set_expand(expand)
    toolbar.insert(_separator, -1)
    _separator.show()


class SlideruleActivity(activity.Activity):
    """ A sliderule activity for Sugar """

    def __init__(self, handle):
        super(SlideruleActivity,self).__init__(handle)

        self._setup_toolbars(_have_toolbox)

        canvas = gtk.DrawingArea()
        canvas.set_size_request(gtk.gdk.screen_width(),
                                gtk.gdk.screen_height())
        self.set_canvas(canvas)
        canvas.show()
        self.show_all()

        self.custom_slides = [False, False]

        self.sr = SlideRule(canvas, os.path.join(activity.get_bundle_path(),
                                                 'images/'), self)

        # Read the slider positions from the Journal
        for slide in self.sr.slides:
            if slide.name in self.metadata:
                slide.move(int(self.metadata[slide.name]),
                           slide.spr.get_xy()[1])
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

        # custom slide settings
        for i in range(2):
            if 'min' + str(i) in self.metadata:
                self._domain_min[i].set_text(self.metadata['min' + str(i)])
                self.custom_slides[i] = True
            if 'max' + str(i) in self.metadata:
                self._domain_max[i].set_text(self.metadata['max' + str(i)])
                self.custom_slides[i] = True
            if 'step' + str(i) in self.metadata:
                self._step_size[i].set_text(self.metadata['step' + str(i)])
                self.custom_slides[i] = True
            if 'label' + str(i) in self.metadata:
                self._label_function[i].set_text(
                    self.metadata['label' + str(i)])
                self.custom_slides[i] = True
            if 'offset' + str(i) in self.metadata:
                self._offset_function[i].set_text(
                    self.metadata['offset' + str(i)])
                self.custom_slides[i] = True
            if 'calculate' + str(i) in self.metadata:
                self._calculate_function[i].set_text(
                    self.metadata['calculate' + str(i)])
                self.custom_slides[i] = True

        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self.show_c()
        if 'R' in self.metadata:
            self.sr.reticule.move(int(self.metadata['R']),
                                  self.sr.reticule.spr.get_xy()[1])
        self.sr.update_slide_labels()
        self.sr.update_results_label()

    def write_file(self, file_path):
        """ Write the slide positions to the Journal """
        self.metadata['slide'] = self.sr.active_slide.name
        self.metadata['stator'] = self.sr.active_stator.name
        for slide in self.sr.slides:
            self.metadata[slide.name] = str(slide.spr.get_xy()[0])
        self.metadata['D'] = str(self.sr.name_to_stator('D').spr.get_xy()[0])
        self.metadata['R'] = str(self.sr.reticule.spr.get_xy()[0])
        for i in range(2):
            if self.custom_slides[i]:
                self.metadata['min' + str(i)] = self._domain_min[i].get_text()
                self.metadata['max' + str(i)] = self._domain_max[i].get_text()
                self.metadata['step' + str(i)] = self._step_size[i].get_text()
                self.metadata['label' + str(i)] = \
                    self._label_function[i].get_text()
                self.metadata['offset' + str(i)] = \
                    self._offset_function[i].get_text()
                self.metadata['calculate' + str(i)] = \
                    self._calculate_function[i].get_text()

    def _hide_all(self):
        self._hide_top()
        self._hide_bottom()

    def _hide_top(self):
        for slide in self.sr.slides:
            slide.hide()

    def _hide_bottom(self):
        for stator in self.sr.stators:
            stator.hide()

    def _show_slides(self, slide, stator, function):
        self._hide_all()
        self._slide_combo.set_active(_SLIDES.index(slide))
        self.set_slide()
        self._stator_combo.set_active(_STATORS.index(stator))
        self.set_stator()
        self._function_combo.set_active(_FUNCTIONS.index(function))
        self.sr.update_slide_labels()
        self.sr.update_results_label()

    def set_function_unknown(self):
        self._function_combo.set_active(_FUNCTIONS.index(_UK))

    def set_slide(self):
        """ Move the top slider onto top layer """
        self._hide_top()
        self.sr.active_slide.draw()
        self.top_button.set_icon(self.sr.active_slide.name)
        self._set_custom_entries(SLIDE, self.sr.active_slide.name)

    def set_stator(self):
        """ Move the bottom slider onto top layer """
        self._hide_bottom()
        self.sr.active_stator.draw()
        self.bottom_button.set_icon(self.sr.active_stator.name)
        self._set_custom_entries(STATOR, self.sr.active_stator.name)

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
        elif self.sr.active_slide.name == 'C' and \
             self.sr.active_stator.name == 'LLn2':
            return self.show_e
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
        self.sr.align_slides()
        self._show_slides(_A, _D, _FA)

    def show_k(self):
        """ three-decade scale """
        self.sr.active_slide = self.sr.name_to_slide('K')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(_K, _D, _FK)

    def show_s(self):
        """ sine """
        self.sr.active_slide = self.sr.name_to_slide('S')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(_S, _D, _FS)

    def show_t(self):
        """ tangent """
        self.sr.active_slide = self.sr.name_to_slide('T')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(_T, _D, _FT)

    def show_l(self):
        """ linear scale """
        self.sr.active_slide = self.sr.name_to_slide('L')
        self.sr.active_stator = self.sr.name_to_stator('L2')
        self._show_slides(_L, _L, _FL)

    def show_e(self):
        """ natural log scale """
        self.sr.active_slide = self.sr.name_to_slide('C')
        self.sr.active_stator = self.sr.name_to_stator('LLn2')
        self.sr.align_slides()
        self._show_slides(_C, _LLn, _FE)

    def show_u(self, slide):
        """ user-defined scale """
        if slide == SLIDE:
            self.sr.active_slide = self.sr.name_to_slide('custom')
            for k in _STATOR_DICTIONARY:
                if _STATOR_DICTIONARY[k] == self.sr.active_stator.name:
                    self._show_slides(_UD, k, _UK)
        else:
            self.sr.active_stator = self.sr.name_to_stator('custom2')
            for k in _SLIDE_DICTIONARY:
                if _SLIDE_DICTIONARY[k] == self.sr.active_slide.name:
                    self._show_slides(k, _UD, _UK)

    def _set_custom_entries(self, slide, name):
        if not self.custom_slides[slide] and name in CUSTOM:
            self._offset_function[slide].set_text(CUSTOM[name][0])
            self._calculate_function[slide].set_text(CUSTOM[name][1])
            self._label_function[slide].set_text(CUSTOM[name][2])
            self._domain_min[slide].set_text(CUSTOM[name][3])
            self._domain_max[slide].set_text(CUSTOM[name][4])
            self._step_size[slide].set_text(CUSTOM[name][5])

    # toolbar button callbacks
    def realign_cb(self, arg=None):
        """ Realign all sliders with the D scale. """
        dx, dy = self.sr.name_to_stator('D').spr.get_xy()
        cy = self.sr.name_to_slide('C').spr.get_xy()[1]
        for slide in self.sr.slides:
            slide.move(dx, cy)
        self.move_stators(dx, dy)
        # After realignment, some predefined functions may be reactivated
        function = self._predefined_function()
        if function is not None:
            function()
        self.sr.update_slide_labels()
        self.sr.update_results_label()

    def _function_combo_cb(self, arg=None):
        """ Read value from predefined-functions combo box """
        _functions_dictionary = {_FA: self.show_a, _FC: self.show_c,
                                 _FK: self.show_k, _FS: self.show_s,
                                 _FT: self.show_t, _FL: self.show_l,
                                 _FCI: self.show_ci, _FE: self.show_e}
        try:
            _functions_dictionary[
                _FUNCTIONS[self._function_combo.get_active()]]()
        except KeyError:
            # 'unknown'
            pass

    def _slide_combo_cb(self, arg=None):
        """ Read value from slide combo box """
        self.sr.active_slide = self.sr.name_to_slide(_SLIDE_DICTIONARY[
            _SLIDES[self._slide_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UK))
            self.set_slide()
            self.sr.update_slide_labels()
            self.sr.update_results_label()

    def _stator_combo_cb(self, arg=None):
        """ Read value from stator combo box """
        self.sr.active_stator = self.sr.name_to_stator(_STATOR_DICTIONARY[
            _STATORS[self._stator_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(_FUNCTIONS.index(_UK))
            self.set_stator()
            self.sr.update_slide_labels()
            self.sr.update_results_label()

    def _custom_slide_cb(self, arg=None):
        """ Create custom slide from parameters in entry widgets """
        self.custom_slides[SLIDE] = True
        self._customize(SLIDE)

    def _custom_stator_cb(self, arg=None):
        """ Create custom stator from parameters in entry widgets """
        self.custom_slides[STATOR] = True
        self._customize(STATOR)

    def _customize(self, slide):
        self.custom_slides[slide] = True
        self.sr.make_custom_slide(self._offset_function[slide].get_text(),
                                  self._calculate_function[slide].get_text(),
                                  self._label_function[slide].get_text(),
                                  self._domain_min[slide].get_text(),
                                  self._domain_max[slide].get_text(),
                                  self._step_size[slide].get_text(), slide)

    def _dummy_cb(self, arg=None):
        return

    def _setup_toolbars(self, have_toolbox):
        """ Setup the toolbars.. """
        project_toolbar = gtk.Toolbar()
        custom_slide_toolbar = gtk.Toolbar()
        custom_stator_toolbar = gtk.Toolbar()

        # no sharing
        self.max_participants = 1

        if have_toolbox:
            toolbox = ToolbarBox()

            # Activity toolbar
            activity_button = ActivityToolbarButton(self)

            toolbox.toolbar.insert(activity_button, 0)
            activity_button.show()

            project_toolbar_button = ToolbarButton(page=project_toolbar,
                                                   icon_name='sliderule')
            project_toolbar.show()
            toolbox.toolbar.insert(project_toolbar_button, -1)
            project_toolbar_button.show()

            custom_slide_toolbar_button = ToolbarButton(
                page=custom_slide_toolbar,
                icon_name='custom-slide')
            custom_slide_toolbar.show()
            toolbox.toolbar.insert(custom_slide_toolbar_button, -1)
            custom_slide_toolbar_button.show()

            custom_stator_toolbar_button = ToolbarButton(
                page=custom_stator_toolbar,
                icon_name='custom-stator')
            custom_stator_toolbar.show()
            toolbox.toolbar.insert(custom_stator_toolbar_button, -1)
            custom_stator_toolbar_button.show()

            self.set_toolbar_box(toolbox)
            toolbox.show()
            toolbar = toolbox.toolbar

        else:
            # Use pre-0.86 toolbar design
            toolbox = activity.ActivityToolbox(self)
            self.set_toolbox(toolbox)
            toolbox.add_toolbar(_('Project'), project_toolbar)
            toolbox.add_toolbar(_('Custom slide'), custom_slide_toolbar)
            toolbox.add_toolbar(_('Custom stator'), custom_stator_toolbar)
            toolbox.show()
            toolbox.set_current_toolbar(1)
            toolbar = project_toolbar

            # no sharing
            if hasattr(toolbox, 'share'):
               toolbox.share.hide()
            elif hasattr(toolbox, 'props'):
               toolbox.props.visible = False

        # Add the buttons to the toolbars
        self._function_combo = _combo_factory(_FUNCTIONS, _FC,
            _('select function'), self._function_combo_cb, project_toolbar)
        self.top_button = _button_factory('C', _('active slide'),
                                          self._dummy_cb, project_toolbar)
        self._slide_combo = _combo_factory(_SLIDES, _C, _('select slide'),
                                           self._slide_combo_cb,
                                           project_toolbar)
        self.bottom_button = _button_factory('D', _('active stator'),
                                             self._dummy_cb, project_toolbar)
        self._stator_combo = _combo_factory(_STATORS, _D, _('select stator'),
            self._stator_combo_cb, project_toolbar)
        _separator_factory(project_toolbar)
        self.realign_button = _button_factory('realign', _('realign slides'),
                                              self.realign_cb, project_toolbar)

        self._offset_function = []
        self._calculate_function = []
        self._label_function = []
        self._domain_min = []
        self._domain_max = []
        self._step_size = []
        self.custom = []

        self._offset_function.append(_entry_factory(CUSTOM['C'][0],
            custom_slide_toolbar, _('position function')))
        self._calculate_function.append(_entry_factory(CUSTOM['C'][1],
            custom_slide_toolbar, _('results function')))
        self._label_function.append(_entry_factory(CUSTOM['C'][2],
            custom_slide_toolbar, _('label function')))
        self._domain_min.append(_entry_factory(CUSTOM['C'][3],
            custom_slide_toolbar, _('domain minimum'), max=4))
        self._domain_max.append(_entry_factory(CUSTOM['C'][4],
            custom_slide_toolbar, _('domain maximum'), max=4))
        self._step_size.append(_entry_factory(CUSTOM['C'][5],
            custom_slide_toolbar, _('step size'), max=4))
        self.custom.append(_button_factory("custom-slide",
            _('create custom slide'), self._custom_slide_cb,
                                           custom_slide_toolbar))

        self._offset_function.append(_entry_factory(CUSTOM['D'][0],
            custom_stator_toolbar, _('position function')))
        self._calculate_function.append(_entry_factory(CUSTOM['D'][1],
            custom_stator_toolbar, _('results function')))
        self._label_function.append(_entry_factory(CUSTOM['D'][2],
            custom_stator_toolbar, _('label function')))
        self._domain_min.append(_entry_factory(CUSTOM['D'][3],
            custom_stator_toolbar, _('domain minimum'), max=4))
        self._domain_max.append(_entry_factory(CUSTOM['D'][4],
            custom_stator_toolbar, _('domain maximum'), max=4))
        self._step_size.append(_entry_factory(CUSTOM['D'][5],
            custom_stator_toolbar, _('step size'), max=4))
        self.custom.append(_button_factory("custom-stator",
            _('create custom stator'), self._custom_stator_cb,
                                           custom_stator_toolbar))

        if have_toolbox:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()
            project_toolbar_button.set_expanded(True)
