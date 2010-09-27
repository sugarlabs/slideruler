#Copyright (c) 2009, 2010 Walter Bender

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
        self.name = name
        self.calculate = calculate
        self.result = result

    def draw(self, layer=1000):
        self.spr.set_layer(layer)
        self.spr.draw()

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

    def match(self, sprite):
        if sprite == self.spr or sprite == self.tabs[0].spr or \
                sprite == self.tabs[1].spr:
            return True
        return False

    def draw(self, layer=1000):
        self.spr.set_layer(layer)
        self.spr.draw()
        self.tabs[0].spr.set_layer(layer)
        self.tabs[0].spr.draw()
        self.tabs[1].spr.set_layer(layer)
        self.tabs[1].spr.draw()

    def move(self, dx, dy):
        self.spr.move((dx, dy))
        self.tabs[0].spr.move((dx + self.tab_dx[0], dy + self.tab_dy[0]))
        self.tabs[1].spr.move((dx + self.tab_dx[1], dy + self.tab_dy[1]))

    def move_relative(self, dx, dy):
        self.spr.move_relative((dx, dy))
        self.tabs[0].spr.move_relative((dx, dy))
        self.tabs[1].spr.move_relative((dx, dy))

    def hide(self):
        self.spr.hide()
        self.tabs[0].spr.hide()
        self.tabs[1].spr.hide()


class Reticule(Slide):
    """ Create a sprite for a reticle """
    def __init__(self, sprites, path, name, x, y, w, h):
        self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        self.tab_dx = [0, 0]
        self.tab_dy = [-SHEIGHT, 2 * SHEIGHT]
        self.tabs = []
        self.tabs.append(Tab(sprites, path, 'tab', x + self.tab_dx[0],
                             y + self.tab_dy[0], TABWIDTH, SHEIGHT))
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
    """ Create tabs for the slide """
    def __init__(self, sprites, path, name, x, y, w, h):
        self.spr = Sprite(sprites, x, y, file_to_pixbuf(path, name, w, h))
        self.spr.label = "1.0"
        self.name = name

def file_to_pixbuf(path, name, w, h):
    """ Load pixbuf from a file. """
    return gtk.gdk.pixbuf_new_from_file_at_size(
        os.path.join(path+name+'.svg'), int(w), int(h))


def svg_str_to_pixbuf(svg_string):
    """ Load pixbuf from SVG string. """
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf


