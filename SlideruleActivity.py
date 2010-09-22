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

"""
Modifying slide rule:

The customization feature is intended to handle most cases where you require
a specialized slide or stator. But if you would like to add a new slide to
the toolbar, you need to make changes in three places:

1. In constants.py, you need to add new entries to SLIDE_TABLE,
STATOR_TABLE, SLIDE_DICTIONARY and STATOR_DICTIONARY so that the
slides appear in the toolbars.

2. In genslides.py, you need to add new class objects to generate the
graphics associated with your slide and stator.

3. In window.py, you need to add methods to calculate values for your
slide and stator.

"""

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
from constants import A_slide, C_slide, CI_slide, K_slide, S_slide, T_slide, \
    L_slide, Log_slide, LLn_slide, UD_slide, D_slide, DI_slide, B_slide, \
    SLIDE_TABLE, STATOR_TABLE, SLIDE_DICTIONARY, STATOR_DICTIONARY, \
    SWIDTH, SLIDE, STATOR, CUSTOM

FA_square = _('square/square root')
FC_multiply = _('multiply/divide')
FCI_divide = _('divide/multiply')
FK_cube = _('cube/cube root')
FS_sin = _('sin, asin')
FT_tan = _('tan, atan')
FL_add = _('add/subtract')
FE_natural_log = _('natural log')
UK_unknown = '-'
FUNCTIONS = [FL_add, FC_multiply, FCI_divide, FA_square, FK_cube, FS_sin,
             FT_tan, FE_natural_log, UK_unknown]


def _combo_factory(combo_array, default, tooltip, callback, toolbar):
    """Factory for making a toolbar combo box"""
    my_combo = ComboBox()
    if hasattr(my_combo, 'set_tooltip_text'):
        my_combo.set_tooltip_text(tooltip)

    my_combo.connect('changed', callback)

    for i, s in enumerate(combo_array):
        my_combo.append_item(i, s, None)

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
        self._slide_combo.set_active(SLIDE_TABLE.index(slide))
        self.set_slide()
        self._stator_combo.set_active(STATOR_TABLE.index(stator))
        self.set_stator()
        self._function_combo.set_active(FUNCTIONS.index(function))
        self.sr.update_slide_labels()
        self.sr.update_results_label()

    def set_function_unknown(self):
        self._function_combo.set_active(FUNCTIONS.index(_UK))

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
        self._show_slides(C_slide, D_slide, FC_multiply)

    def show_ci(self):
        """ inverse scale """
        self.sr.active_slide = self.sr.name_to_slide('CI')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self._show_slides(CI_slide, D_slide, FCI_divide)

    def show_a(self):
        """ two-decade scale """
        self.sr.active_slide = self.sr.name_to_slide('A')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(A_slide, D_slide, FA_square)

    def show_k(self):
        """ three-decade scale """
        self.sr.active_slide = self.sr.name_to_slide('K')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(K_slide, D_slide, FK_cube)

    def show_s(self):
        """ sine """
        self.sr.active_slide = self.sr.name_to_slide('S')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(S_slide, D_slide, FS_sin)

    def show_t(self):
        """ tangent """
        self.sr.active_slide = self.sr.name_to_slide('T')
        self.sr.active_stator = self.sr.name_to_stator('D')
        self.sr.align_slides()
        self._show_slides(T_slide, D_slide, FT_tan)

    def show_l(self):
        """ linear scale """
        self.sr.active_slide = self.sr.name_to_slide('L')
        self.sr.active_stator = self.sr.name_to_stator('L2')
        self._show_slides(L_slide, L_slide, FL_add)

    def show_e(self):
        """ natural log scale """
        self.sr.active_slide = self.sr.name_to_slide('C')
        self.sr.active_stator = self.sr.name_to_stator('LLn2')
        self.sr.align_slides()
        self._show_slides(C_slide, LLn_slide, FE_natural_log)

    def show_u(self, slide):
        """ user-defined scale """
        if slide == SLIDE:
            self.sr.active_slide = self.sr.name_to_slide('custom')
            for k in _STATOR_DICTIONARY:
                if _STATOR_DICTIONARY[k] == self.sr.active_stator.name:
                    self._show_slides(UD_slide, k, UK_unknown)
        else:
            self.sr.active_stator = self.sr.name_to_stator('custom2')
            for k in _SLIDE_DICTIONARY:
                if _SLIDE_DICTIONARY[k] == self.sr.active_slide.name:
                    self._show_slides(k, UD_slide, UK_unknown)
        self.sr.align_slides()

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
        FUNCTIONS_DICTIONARY = {FA_square: self.show_a,
                                FC_multiply: self.show_c,
                                FK_cube: self.show_k, FS_sin: self.show_s,
                                FT_tan: self.show_t, FL_add: self.show_l,
                                FCI_divide: self.show_ci,
                                FE_natural_log: self.show_e}
        try:
            FUNCTIONS_DICTIONARY[FUNCTIONS[self._function_combo.get_active()]]()
        except KeyError:
            # 'unknown'
            pass

    def _slide_combo_cb(self, arg=None):
        """ Read value from slide combo box """
        self.sr.active_slide = self.sr.name_to_slide(SLIDE_DICTIONARY[
            SLIDE_TABLE[self._slide_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(FUNCTIONS.index(UK_unknown))
            self.set_slide()
            self.sr.update_slide_labels()
            self.sr.update_results_label()

    def _stator_combo_cb(self, arg=None):
        """ Read value from stator combo box """
        self.sr.active_stator = self.sr.name_to_stator(STATOR_DICTIONARY[
            STATOR_TABLE[self._stator_combo.get_active()]])
        function = self._predefined_function()
        if function is not None:
            function()
        else:
            self._function_combo.set_active(FUNCTIONS.index(UK_unknown))
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
        self._function_combo = _combo_factory(FUNCTIONS, FC_multiply,
            _('select function'), self._function_combo_cb, project_toolbar)
        self.top_button = _button_factory('C', _('active slide'),
                                          self._dummy_cb, project_toolbar)
        self._slide_combo = _combo_factory(SLIDE_TABLE, C_slide,
            _('select slide'), self._slide_combo_cb, project_toolbar)
        self.bottom_button = _button_factory('D', _('active stator'),
                                             self._dummy_cb, project_toolbar)
        self._stator_combo = _combo_factory(STATOR_TABLE, D_slide,
            _('select stator'), self._stator_combo_cb, project_toolbar)
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


        ENTRY = ['C', 'D']
        ENTRY_TOOLBAR = [custom_slide_toolbar, custom_stator_toolbar]
        ENTRY_BUTTON = ['custom-slide', 'custom-stator']
        ENTRY_TOOLTIP = [_('create custom slide'), _('create custom stator')]
        ENTRY_CALLBACK = [self._custom_slide_cb, self._custom_stator_cb]
        for i in range(2):
            self._offset_function.append(_entry_factory(CUSTOM[ENTRY[i]][0],
                ENTRY_TOOLBAR[i], _('position function')))
            self._calculate_function.append(_entry_factory(CUSTOM[ENTRY[i]][1],
                ENTRY_TOOLBAR[i], _('results function')))
            self._label_function.append(_entry_factory(CUSTOM[ENTRY[i]][2],
                ENTRY_TOOLBAR[i], _('label function')))
            self._domain_min.append(_entry_factory(CUSTOM[ENTRY[i]][3],
                ENTRY_TOOLBAR[i], _('domain minimum'), max=4))
            self._domain_max.append(_entry_factory(CUSTOM[ENTRY[i]][4],
                ENTRY_TOOLBAR[i], _('domain maximum'), max=4))
            self._step_size.append(_entry_factory(CUSTOM[ENTRY[i]][5],
                ENTRY_TOOLBAR[i], _('step size'), max=4))
            self.custom.append(_button_factory(ENTRY_BUTTON[i],
                ENTRY_TOOLTIP[i], ENTRY_CALLBACK[i], ENTRY_TOOLBAR[i]))

        if have_toolbox:
            _separator_factory(toolbox.toolbar, False, True)

            stop_button = StopButton(self)
            stop_button.props.accelerator = '<Ctrl>q'
            toolbox.toolbar.insert(stop_button, -1)
            stop_button.show()
            project_toolbar_button.set_expanded(True)
