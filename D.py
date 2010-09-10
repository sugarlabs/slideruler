# -*- coding: utf-8 -*-
#Copyright (c) 2009,10 Walter Bender

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from constants import SWIDTH, SHEIGHT, OFFSET, SCALE, HTOP1, HTOP2, HTOP3
from C import mark, special_mark, header, footer, make_stator
import math

def main():
    """ Log scale for stator (bottom scale) """

    def offset_function(x):
        return math.log(x, 10)

    def label_function(x):
        return x

    make_stator('D', offset_function, label_function)
    return 0


if __name__ == "__main__":
    main()
