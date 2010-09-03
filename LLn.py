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

from constants import SWIDTH, SHEIGHT, OFFSET, SCALE, HTOP1, HTOP2, HTOP3
from C import mark, special_mark, header, footer

import math


htop1 = HTOP1
htop2 = HTOP2
htop3 = HTOP3
offset1 = 5
offset2 = 7
offset3 = -12


def main():

    header('LLn', 10)

    x = 0.0
    i = 0
    while x < math.log(10):
        if i/5*5 == i:
            mark(x, htop3, htop2, htop1,
                 str(float(int(x*100))/100.))
        else:
            mark(x, htop3, htop2, htop1 + offset1)
        x += math.log(math.e)/100
        i += 1

    s = math.log(10)
    mark(s, htop3 + offset3, htop2, htop1)
    footer()
    return 0

if __name__ == "__main__":
    main()
