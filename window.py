# -*- coding: utf-8 -*-
#Copyright (c) 2009, Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
from gettext import gettext as _
import math

try:
    from sugar.graphics import style
    GRID_CELL_SIZE = style.GRID_CELL_SIZE
except:
    GRID_CELL_SIZE = 0

from rule import *
from mark import *

class taWindow: pass

#
# handle launch from both within and without of Sugar environment 
#
def new_window(canvas, path, parent=None):
    tw = taWindow()
    tw.path = path
    tw.activity = parent

    # starting from command line
    # we have to do all the work that was done in CardSortActivity.py
    if parent is None:
        tw.sugar = False
        tw.canvas = canvas

    # starting from Sugar
    else:
        tw.sugar = True
        tw.canvas = canvas
        parent.show_all()

    tw.canvas.set_flags(gtk.CAN_FOCUS)
    tw.canvas.add_events(gtk.gdk.BUTTON_PRESS_MASK)
    tw.canvas.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
    tw.canvas.add_events(gtk.gdk.POINTER_MOTION_MASK)
    tw.canvas.connect("expose-event", _expose_cb, tw)
    tw.canvas.connect("button-press-event", _button_press_cb, tw)
    tw.canvas.connect("button-release-event", _button_release_cb, tw)
    tw.canvas.connect("motion-notify-event", _mouse_move_cb, tw)
    tw.width = gtk.gdk.screen_width()
    tw.height = gtk.gdk.screen_height()-GRID_CELL_SIZE
    tw.area = tw.canvas.window
    tw.gc = tw.area.new_gc()
    tw.cm = tw.gc.get_colormap()
    tw.msgcolor = tw.cm.alloc_color('black')
    tw.sprites = []
    tw.scale = 1

    # Open the sliders
    tw.sliders = [Mark(tw,"reticule",0,90), \
                  Rule(tw,"C",0,100), \
                  Rule(tw,"D",0,160)]
    tw.sliders[1].draw_ruler()
    tw.sliders[2].draw_ruler()

    # and the reticule
    tw.sliders[0].draw_mark()

    # Start calculating
    tw.press = None
    tw.start_drag = [0,0]

    return tw

#
# Button press
#
def _button_press_cb(win, event, tw):
    win.grab_focus()
    x, y = map(int, event.get_coords())
    tw.start_drag = [x,y]
    spr = findsprite(tw,(x,y))
    tw.press = spr
    return True

#
# Mouse move
#
def _mouse_move_cb(win, event, tw):
    if tw.press is None:
        return True
    win.grab_focus()
    x, y = map(int, event.get_coords())
    # redicule doesn't use offset
    if tw.press == tw.sliders[0].spr:
        dx = x-tw.press.x
    else:
        dx = x-tw.press.x-tw.start_drag[0]
    if tw.press.label == "D":
        # everything moves
        for r in tw.sliders:
            move(r.spr,(r.spr.x+dx,r.spr.y))
    else:
        move(tw.press,(tw.press.x+dx,tw.press.y))
    return True


#
# Button release
#
def _button_release_cb(win, event, tw):
    if tw.press == None:
        return True
    tw.press = None

    # calculate the values for D, C, and D*C (under the redicule)
    dx = tw.sliders[1].spr.x - tw.sliders[2].spr.x    
    if dx < 0:
        D = " "
    else:
        D = math.exp(dx/1000.)
        D = float(int(D*100)/100.)
    
    dx = tw.sliders[0].spr.x - tw.sliders[1].spr.x    
    if dx < 0:
        C = " "
    else:
        C = math.exp(dx/1000.)
        C = float(int(C*100)/100.)

    dx = tw.sliders[0].spr.x - tw.sliders[2].spr.x    
    if dx < 0:
        DC = " "
    else:
        DC = math.exp(dx/1000.)
        DC = float(int(DC*100)/100.)
    tw.activity.results_label.set_text(" D = " + str(D) + 
                                       " C = " + str(C) + 
                                       " D×C = " + str(DC))
    tw.activity.results_label.show()
    return True

def _expose_cb(win, event, tw):
    redrawsprites(tw)
    return True

def _destroy_cb(win, event, tw):
    gtk.main_quit()
