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
from sprites import *

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
    tw.sprites = Sprites(tw.canvas)
    tw.scale = 1

    # Open the sliders
    y = 50
    tw.A = Slider(tw.sprites,tw.path,"A",0,y+60,SWIDTH,SHEIGHT)
    tw.C = Slider(tw.sprites,tw.path,"C",0,y+60,SWIDTH,SHEIGHT)
    tw.C_tab_left = Slider(tw.sprites,tw.path,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.C_tab_right = Slider(tw.sprites,tw.path,"tab",SWIDTH-100,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.D = Slider(tw.sprites,tw.path,"D",0,y+2*SHEIGHT,SWIDTH,SHEIGHT)
    tw.R = Slider(tw.sprites,tw.path,"reticule",0,y+SHEIGHT,100,2*SHEIGHT,False)
    tw.R_tab_top = Slider(tw.sprites,tw.path,"tab",0,y,100,60,False)
    tw.R_tab_bot = Slider(tw.sprites,tw.path,"tab",0,y+3*SHEIGHT,100,SHEIGHT,False)
    tw.slider_on_top = 'C'

    tw.R.spr.set_label("")
    tw.A.spr.set_label("")
    tw.C.spr.set_label("")
    tw.D.spr.set_label("")
    _update_slider_labels(tw)
    _update_results_label(tw)

    tw.A.draw_slider(500)
    tw.C.draw_slider()
    tw.C_tab_left.draw_slider()
    tw.C_tab_right.draw_slider()
    tw.D.draw_slider()
    tw.R_tab_bot.draw_slider()
    tw.R_tab_top.draw_slider()
    tw.R.draw_slider(2000)

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
    spr = tw.sprites.find_sprite((x,y))
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
        tw.C.spr.move_relative((dx,0))
        tw.C_tab_left.spr.move_relative((dx,0))
        tw.C_tab_right.spr.move_relative((dx,0))
        tw.A.spr.move_relative((dx,0))
        tw.D.spr.move_relative((dx,0))
        tw.R_tab_top.spr.move_relative((dx,0))
        tw.R_tab_bot.spr.move_relative((dx,0))
        tw.R.spr.move_relative((dx,0))
    elif tw.press == tw.R_tab_top.spr or \
         tw.press == tw.R_tab_bot.spr or \
         tw.press == tw.R.spr:
        tw.R_tab_top.spr.move_relative((dx,0))
        tw.R_tab_bot.spr.move_relative((dx,0))
        tw.R.spr.move_relative((dx,0))
    elif tw.press == tw.C.spr or \
         tw.press == tw.C_tab_left.spr or \
         tw.press == tw.C_tab_right.spr:
        tw.C.spr.move_relative((dx,0))
        tw.C_tab_left.spr.move_relative((dx,0))
        tw.C_tab_right.spr.move_relative((dx,0))

    # reset drag position
    tw.dragpos = x
    _update_slider_labels(tw)
    _update_results_label(tw)

def _update_slider_labels(tw):
    tw.C_tab_left.spr.set_label(str(_calc_D(tw)))
    tw.C_tab_right.spr.set_label(str(_calc_D(tw)))
    if tw.slider_on_top == "A":
        tw.R_tab_top.spr.set_label(str(_calc_A(tw)))
        tw.R_tab_bot.spr.set_label(str(_calc_DA(tw)))
    else:
        tw.R_tab_top.spr.set_label(str(_calc_C(tw)))
        tw.R_tab_bot.spr.set_label(str(_calc_DC(tw)))
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
        s = " √ " + str(_calc_A(tw)) + " = " + str(_calc_DA(tw)*tw.factor)
    else:
        # calculate the values for D, C, and D*C (under the redicule)
        s = str(_calc_D(tw)) + " × " + str(_calc_C(tw)) + " = " + \
                                       str(_calc_DC(tw)*tw.factor)
    if tw.sugar is True:
        tw.activity.results_label.set_text(s)
        tw.activity.results_label.show()
    else:
        if hasattr(tw,"win"):
            tw.win.set_title("%s: %s" % (_("Sliderule"),s))
    return True

def _calc_C(tw):
    rx,ry = tw.R.spr.get_xy()
    cx,cy = tw.C.spr.get_xy()
    dx = rx-cx
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    C = math.exp(dx/SCALE)
    return float(int(C*100)/100.)

def _calc_A(tw):
    rx,ry = tw.R.spr.get_xy()
    ax,ay = tw.A.spr.get_xy()
    dx = rx-ax
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    A = math.exp(2*dx/SCALE) # two-decade rule
    return float(int(A*100)/100.)

def _calc_D(tw):
    x,y = tw.D.spr.get_xy()
    if tw.slider_on_top == "A":
        ax,ay = tw.A.spr.get_xy()
        dx = ax-x
    else:
        cx,cy = tw.C.spr.get_xy()
        dx = cx-x
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
        tw.factor = 10
    else:
        tw.factor = 1
    D = math.exp(dx/SCALE)
    return float(int(D*100)/100.)

def _calc_DC(tw):
    rx,ry = tw.R.spr.get_xy()
    x,y = tw.D.spr.get_xy()
    dx = rx-x
    if dx < 0:
        dx = math.log(10.)*SCALE + dx
    DC = math.exp(dx/SCALE)
    return float(int(DC*100)/100.)

def _calc_DA(tw):
    rx,ry = tw.R.spr.get_xy()
    x,y = tw.D.spr.get_xy()
    dx = rx-x
    if dx < 0:
        dx = math.log(100.)*SCALE + dx
    DA = math.exp(dx/SCALE)
    return float(int(DA*100)/100.)

def _expose_cb(win, event, tw):
    tw.sprites.redraw_sprites()
    return True

def _destroy_cb(win, event, tw):
    gtk.main_quit()
