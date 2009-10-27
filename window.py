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
    tw.A = Sprite(tw,"A",0,y+60,SWIDTH,SHEIGHT)
    tw.C = Sprite(tw,"C",0,y+60,SWIDTH,SHEIGHT)
    tw.C_tab_left = Sprite(tw,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.C_tab_right = Sprite(tw,"tab",SWIDTH-100,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.D = Sprite(tw,"D",0,y+2*SHEIGHT,SWIDTH,SHEIGHT)
    tw.R = Sprite(tw,"reticule",0,y+SHEIGHT,100,2*SHEIGHT,False)
    tw.R_tab_top = Sprite(tw,"tab",0,y,100,60,False)
    tw.R_tab_bot = Sprite(tw,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.slider_on_top = 'C'

    setlabel(tw.R.spr,"")
    setlabel(tw.A.spr,"")
    setlabel(tw.C.spr,"")
    setlabel(tw.D.spr,"")
    _update_slider_labels(tw)
    _update_results_label(tw)

    tw.A.draw_slider(500)
    tw.C.draw_slider()
    tw.C_tab_left.draw_slider()
    tw.C_tab_right.draw_slider()
    tw.D.draw_slider()
    tw.R.draw_slider(2000)
    tw.R_tab_top.draw_slider()
    tw.R_tab_bot.draw_slider()

    # Start calculating
    tw.factor = 1
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
    if tw.press == tw.D.spr or tw.press == tw.A.spr:
        # everything moves
        move(tw.R.spr,(tw.R.spr.x+dx,tw.R.spr.y))
        move(tw.R_tab_top.spr,(tw.R_tab_top.spr.x+dx,tw.R_tab_top.spr.y))
        move(tw.R_tab_bot.spr,(tw.R_tab_bot.spr.x+dx,tw.R_tab_bot.spr.y))
        move(tw.C.spr,(tw.C.spr.x+dx,tw.C.spr.y))
        move(tw.C_tab_left.spr,(tw.C_tab_left.spr.x+dx,tw.C_tab_left.spr.y))
        move(tw.C_tab_right.spr,(tw.C_tab_right.spr.x+dx,tw.C_tab_right.spr.y))
        move(tw.A.spr,(tw.A.spr.x+dx,tw.A.spr.y))
        move(tw.D.spr,(tw.D.spr.x+dx,tw.D.spr.y))
    elif tw.press == tw.R_tab_top.spr or \
         tw.press == tw.R_tab_bot.spr or \
         tw.press == tw.R.spr:
        move(tw.R.spr,(tw.R.spr.x+dx,tw.R.spr.y))
        move(tw.R_tab_top.spr,(tw.R_tab_top.spr.x+dx,tw.R_tab_top.spr.y))
        move(tw.R_tab_bot.spr,(tw.R_tab_bot.spr.x+dx,tw.R_tab_bot.spr.y))
    elif tw.press == tw.C.spr or \
         tw.press == tw.C_tab_left.spr or \
         tw.press == tw.C_tab_right.spr:
        move(tw.C.spr,(tw.C.spr.x+dx,tw.C.spr.y))
        move(tw.C_tab_left.spr,(tw.C_tab_left.spr.x+dx,tw.C_tab_left.spr.y))
        move(tw.C_tab_right.spr,(tw.C_tab_right.spr.x+dx,tw.C_tab_right.spr.y))

    # reset drag position
    tw.dragpos = x
    _update_slider_labels(tw)
    _update_results_label(tw)

def _update_slider_labels(tw):
    setlabel(tw.C_tab_left.spr,str(_calc_D(tw)))
    setlabel(tw.C_tab_right.spr,str(_calc_D(tw)))
    if tw.slider_on_top == "A":
        setlabel(tw.R_tab_top.spr,str(_calc_A(tw)))
        setlabel(tw.R_tab_bot.spr,str(_calc_DA(tw)))
    else:
        setlabel(tw.R_tab_top.spr,str(_calc_C(tw)))
        setlabel(tw.R_tab_bot.spr,str(_calc_DC(tw)))
    return True


#
# Button release
#
def _button_release_cb(win, event, tw):
    if tw.press == None:
        return True
    tw.press = None
    _update_results_label(tw)

def _update_results_label(tw):
    if tw.slider_on_top == "A":
        # calculate the values for D, A, and D*A (under the redicule)
        tw.activity.results_label.set_text(" √ " + str(_calc_A(tw)) + 
                                           " = " + str(_calc_DA(tw)*tw.factor))
    else:
        # calculate the values for D, C, and D*C (under the redicule)
        tw.activity.results_label.set_text(str(_calc_D(tw)) + " × " + 
                                           str(_calc_C(tw)) + " = " +
                                           str(_calc_DC(tw)*tw.factor))
    tw.activity.results_label.show()
    return True

def _calc_C(tw):
    dx = tw.R.spr.x - tw.C.spr.x    
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    C = math.exp(dx/SCALE)
    return float(int(C*100)/100.)

def _calc_A(tw):
    dx = tw.R.spr.x - tw.A.spr.x
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    A = math.exp(2*dx/SCALE) # two-decade rule
    return float(int(A*100)/100.)

def _calc_D(tw):
    if tw.slider_on_top == "A":
        dx = tw.A.spr.x - tw.D.spr.x
    else:
        dx = tw.C.spr.x - tw.D.spr.x
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
        tw.factor = 10
    else:
        tw.factor = 1
    D = math.exp(dx/SCALE)
    return float(int(D*100)/100.)

def _calc_DC(tw):
    dx = tw.R.spr.x - tw.D.spr.x    
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    DC = math.exp(dx/SCALE)
    return float(int(DC*100)/100.)

def _calc_DA(tw):
    dx = tw.R.spr.x - tw.D.spr.x    
    if dx < 0:
        dx = math.log(100.)*SCALE + dx
    DA = math.exp(dx/SCALE)
    return float(int(DA*100)/100.)

def _expose_cb(win, event, tw):
    redrawsprites(tw)
    return True

def _destroy_cb(win, event, tw):
    gtk.main_quit()
