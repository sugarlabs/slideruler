#Copyright (c) 2009, 2010 Walter Bender
#Copyright (c) 2012, Ignacio Rodriguez

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this library; if not, write to the Free Software
# Foundation, 51 Franklin Street, Suite 500 Boston, MA 02110-1335 USA
from gi.repository import Gdk, GdkPixbuf
from sugar3 import logger
import logging
_logger = logging.getLogger('slideruler')

logger.start('slideruler')
import os.path

from constants import SHEIGHT, SWIDTH, LEFT, RIGHT, TOP, BOTTOM, TABWIDTH
from sprites import Sprite


class Stator():
    """ Create a sprite for a stator """
    def __init__(self, sprites, path, name, x, y, w, h, svg_engine=None,
                 calculate=None, result=None):
        if svg_engine is None:
            self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        else:
            self.spr = Sprite(sprites, x, y,
                              svg_str_to_pixbuf(svg_engine().svg))
        self.spr.type = name
        self.name = name
        self.calculate = calculate
        self.result = result

    def draw(self, layer=1000):
        self.spr.set_layer(layer)

    def match(self, sprite):
        if self.spr == sprite:
            return True
        return False

    def move(self, dx, dy):
        self.spr.move((dx, dy))

    def move_relative(self, dx, dy):
        self.spr.move_relative((dx, dy))

    def hide(self):
        self.spr.hide()


class Slide(Stator):
    """ Create a sprite for a slide """
    def __init__(self, sprites, path, name, x, y, w, h, svg_engine=None,
                 function=None):
        if svg_engine is None:
            self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        else:
            self.spr = Sprite(sprites, x, y,
                              svg_str_to_pixbuf(svg_engine().svg))
        self.tab_dx = [0, SWIDTH - TABWIDTH]
        self.tab_dy = [2 * SHEIGHT, 2 * SHEIGHT]
        self.tabs = []
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[0],
                             y + self.tab_dy[0], TABWIDTH, SHEIGHT))
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[1],
                             y + self.tab_dy[1], TABWIDTH, SHEIGHT))
        self.calculate = function
        self.name = name

    def add_textview(self, textview, i=0):
        self.tabs[i].textview = textview
        self.tabs[i].textbuffer = textview.get_buffer()

    def set_fixed(self, fixed):
        for tab in self.tabs:
            tab.fixed = fixed

    def match(self, sprite):
        if sprite == self.spr or sprite == self.tabs[0].spr or \
                sprite == self.tabs[1].spr:
            return True
        return False

    def draw(self, layer=1000):
        self.spr.set_layer(layer)
        self.spr.draw()
        for tab in self.tabs:
            tab.draw()

    def move(self, dx, dy):
        self.spr.move((dx, dy))
        for i, tab in enumerate(self.tabs):
            tab.move(dx + self.tab_dx[i], dy + self.tab_dy[i])

    def move_relative(self, dx, dy):
        self.spr.move_relative((dx, dy))
        for i, tab in enumerate(self.tabs):
            tab.move_relative(dx, dy)

    def hide(self):
        self.spr.hide()
        for tab in self.tabs:
            tab.hide()

    def label(self, label, i=0):
        self.tabs[i].label(label)


class Reticule(Slide):
    """ Create a sprite for a reticle """
    def __init__(self, sprites, path, name, x, y, w, h):
        self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        self.spr.type = name
        self.tab_dx = [0, 0]
        self.tab_dy = [-SHEIGHT, 2 * SHEIGHT]
        self.tabs = []
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[0],
                             y + self.tab_dy[0], TABWIDTH, SHEIGHT))
        self.tabs[-1].textview_y_offset = int(h / 4)
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[1],
                             y + self.tab_dy[1], TABWIDTH, SHEIGHT))
        self.name = name


class CustomSlide(Slide):
    """ Create a sprite for a custom slide """
    def __init__(self, sprites, path, name, x, y, svg_engine, function,
                 offset, label, min, max, step):
        svg = svg_engine(name, offset, label, min, max, step)
        self.error_msg = svg.error_msg
        self.spr = Sprite(sprites, x, y, svg_str_to_pixbuf(svg.svg))
        self.tab_dx = [0, SWIDTH - TABWIDTH]
        self.tab_dy = [2 * SHEIGHT, 2 * SHEIGHT]
        self.tabs = []
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[0],
                             y + self.tab_dy[0], TABWIDTH, SHEIGHT))
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[1],
                             y + self.tab_dy[1], TABWIDTH, SHEIGHT))
        self.calculate = function
        self.name = name


class CustomStator(Stator):
    """ Create a sprite for a custom slide """
    def __init__(self, sprites, name, x, y, svg_engine, calculate, result,
                 offset, label, min, max, step):
        svg = svg_engine(name, offset, label, min, max, step)
        self.error_msg = svg.error_msg
        self.spr = Sprite(sprites, x, y, svg_str_to_pixbuf(svg.svg))
        self.calculate = calculate
        self.result = result
        self.name = name


class Tab():
    """ Create tabs for the slide; include a TextView for OSK input """
    def __init__(self, sprites, path, name, x, y, w, h):
        self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        self.spr.label = "1.0"
        self.spr.type = name
        self.name = name
        self.width = w
        self.textview = None
        self.textbuffer = None
        self.fixed = None
        self.textview_y_offset = 0

    def label(self, label):
        if self.textbuffer is not None:
            self.textbuffer.set_text(label)

    def _move_textview(self, x, y):
        y += self.textview_y_offset
        if self.textview is not None:
            if x > 0 and x < Gdk.Screen.width() - self.width and y > 0:
                self.fixed.move(self.textview, x, y)
                self.textview.show()
            else:
                self.textview.hide()

    def move(self, x, y):
        self.spr.move((x, y))
        self._move_textview(x, y)

    def move_relative(self, dx, dy):
        self.spr.move_relative((dx, dy))
        x, y = self.spr.get_xy()
        self._move_textview(x, y)

    def draw(self, layer=100):
        self.spr.set_layer(layer)
        self.spr.draw()
        x, y = self.spr.get_xy()
        self._move_textview(x, y)

    def hide(self):
        self.spr.hide()


def file_to_pixbuf(path, name, w, h):
    """ Load pixbuf from a file. """
    return GdkPixbuf.Pixbuf.new_from_file_at_size(
        os.path.join(path, name + '.svg'), int(w), int(h))


def svg_str_to_pixbuf(svg_string):
    """ Load pixbuf from SVG string. """
    pl = GdkPixbuf.PixbufLoader.new_with_type('svg')
    pl.write(svg_string.encode())
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf
