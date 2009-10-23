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

from constants import *

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

from sprite_factory import *

class srWindow: pass

#
# handle launch from both within and without of Sugar environment 
#
def new_window(canvas, path, parent=None):
    tw = srWindow()
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
    y = 50
    tw.R = Sprite(tw,"reticule",0,y+SHEIGHT,100,2*SHEIGHT,False)
    tw.R_tab_top = Sprite(tw,"tab",0,y,100,60,False)
    tw.R_tab_bot = Sprite(tw,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.C = Sprite(tw,"C",0,y+60,SWIDTH,SHEIGHT)
    tw.C_tab = Sprite(tw,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.D = Sprite(tw,"D",0,y+2*SHEIGHT,SWIDTH,SHEIGHT)

    setlabel(tw.R.spr,"")
    setlabel(tw.C.spr,"")
    setlabel(tw.D.spr,"")
    _update_labels(tw)

    tw.C.draw_slider()
    tw.C_tab.draw_slider()
    tw.D.draw_slider()
    tw.R.draw_slider()
    tw.R_tab_top.draw_slider()
    tw.R_tab_bot.draw_slider()

    # Start calculating
    tw.press = None
    tw.dragpos = 0

    return tw

#
# Button press
#
def _button_press_cb(win, event, tw):
    win.grab_focus()
    x, y = map(int, event.get_coords())
    tw.dragpos = x
    spr = findsprite(tw,(x,y))
    tw.press = spr
    return True

#
# Mouse move
#
def _mouse_move_cb(win, event, tw):
    if tw.press is None:
        tw.dragpos = 0
        return True

    win.grab_focus()
    x, y = map(int, event.get_coords())
    # redicule doesn't use offset
    dx = x-tw.dragpos
    if tw.press == tw.D.spr:
        # everything moves
        move(tw.R.spr,(tw.R.spr.x+dx,tw.R.spr.y))
        move(tw.R_tab_top.spr,(tw.R_tab_top.spr.x+dx,tw.R_tab_top.spr.y))
        move(tw.R_tab_bot.spr,(tw.R_tab_bot.spr.x+dx,tw.R_tab_bot.spr.y))
        move(tw.C.spr,(tw.C.spr.x+dx,tw.C.spr.y))
        move(tw.C_tab.spr,(tw.C_tab.spr.x+dx,tw.C_tab.spr.y))
        move(tw.D.spr,(tw.D.spr.x+dx,tw.D.spr.y))
    elif tw.press == tw.R_tab_top.spr or \
         tw.press == tw.R_tab_bot.spr or \
         tw.press == tw.R.spr:
        move(tw.R.spr,(tw.R.spr.x+dx,tw.R.spr.y))
        move(tw.R_tab_top.spr,(tw.R_tab_top.spr.x+dx,tw.R_tab_top.spr.y))
        move(tw.R_tab_bot.spr,(tw.R_tab_bot.spr.x+dx,tw.R_tab_bot.spr.y))
    elif tw.press == tw.C.spr or tw.press == tw.C_tab.spr:
        move(tw.C.spr,(tw.C.spr.x+dx,tw.C.spr.y))
        move(tw.C_tab.spr,(tw.C_tab.spr.x+dx,tw.C_tab.spr.y))
    else: # what else?
        move(tw.press,(tw.press.x+dx,tw.press.y))
    # reset drag position
    tw.dragpos = x
    _update_labels(tw)

def _update_labels(tw):
    setlabel(tw.C_tab.spr,_calc_D(tw))
    setlabel(tw.R_tab_top.spr,_calc_C(tw))
    setlabel(tw.R_tab_bot.spr,_calc_DC(tw))
    return True


#
# Button release
#
def _button_release_cb(win, event, tw):
    if tw.press == None:
        return True
    tw.press = None
    update_label(tw)

def update_label(tw):
    # calculate the values for D, C, and D*C (under the redicule)
    tw.activity.results_label.set_text(_calc_D(tw) + " × " + 
                                       _calc_C(tw) + " = " +
                                       _calc_DC(tw))
    tw.activity.results_label.show()
    return True

def _calc_C(tw):
    dx = tw.R.spr.x - tw.C.spr.x    
    if dx < 0:
        return " "
    else:
        C = math.exp(dx/SCALE)
        return str(float(int(C*100)/100.))

def _calc_D(tw):
    dx = tw.C.spr.x - tw.D.spr.x
    if dx < 0:
        return " "
    else:
        D = math.exp(dx/SCALE)
        return str(float(int(D*100)/100.))

def _calc_DC(tw):
    dx = tw.R.spr.x - tw.D.spr.x    
    if dx < 0:
        return " "
    else:
        DC = math.exp(dx/SCALE)
        return str(float(int(DC*100)/100.))

def _expose_cb(win, event, tw):
    redrawsprites(tw)
    return True

def _destroy_cb(win, event, tw):
    gtk.main_quit()
