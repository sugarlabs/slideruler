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
from C import header, footer, mark, special_mark

import math


htop1 = HTOP1
htop2 = HTOP2
htop3 = HTOP3
offset1 = 5
offset2 = 7
offset3 = -12


def main():

    header('T')

    for i in range(12, 91):
        r = float(i) / 2 * math.pi / 180.
        t = math.tan(r)
        if (i / 2) * 2 == i:
            mark(math.log(t * 10.), htop3, htop2, htop1, str(int(i / 2)))
        else:
            mark(math.log(t * 10.), htop3, htop2, htop1 + offset1)

    footer()
    return 0

if __name__ == "__main__":
    main()
