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

    header('S')

    for i in range(12, 32):
        r = float(i) / 2 * math.pi / 180.
        s = math.sin(r)
        if (i / 2) * 2 == i:
            mark(math.log(s * 10.), htop3, htop2, htop1, str(int(i / 2)))
            if int((i / 4) * 4) == i:
                special_mark(math.log(s * 10.), htop3 + offset3, htop2, htop1,
                             str(int(180 - i / 2)))
        else:
            mark(math.log(s * 10.), htop3, htop2, htop1 + offset1)

    for i in range(32, 64):
        r = float(i) / 2 * math.pi / 180.
        s = math.sin(r)
        if (i / 4) * 4 == i:
            mark(math.log(s * 10.), htop3, htop2, htop1, str(int(i / 2)))
            if int((i / 4) * 4) == i:
                special_mark(math.log(s * 10.), htop3 + offset3, htop2, htop1,
                             str(int(180 - i / 2)))
        else:
            mark(math.log(s * 10.), htop3, htop2, htop1 + offset1)

    for i in range(64, 120, 2):
        r = float(i) / 2 * math.pi / 180.
        s = math.sin(r)
        if (i / 4) * 4 == i:
            mark(math.log(s * 10.), htop3, htop2, htop1, str(int(i / 2)))
            if (i / 8) * 8 == i:
                special_mark(math.log(s * 10.), htop3 + offset3, htop2, htop1,
                            str(180 - i / 2))
        else:
            mark(math.log(s * 10.), htop3, htop2, htop1 + offset1)

    for i in range(120, 160, 4):
        r = float(i) / 2 * math.pi / 180.
        s = math.sin(r)
        if (i / 8) * 8 == i:
            mark(math.log(s * 10.), htop3, htop2, htop1, str(int(i / 2)))
            if (i / 16) * 16 == i:
                special_mark(math.log(s * 10.), htop3 + offset3, htop2, htop1,
                            str(180 - i / 2))
        else:
            mark(math.log(s * 10.), htop3, htop2, htop1 + offset1)

    for i in range(160, 180, 2):
        r = float(i) / 2 * math.pi / 180.
        s = math.sin(r)
        if (i / 20) * 20 == i:
            mark(math.log(s * 10.), htop3, htop2, htop1, str(int(i / 2)))
            special_mark(math.log(s * 10.), htop3 + offset3, htop2, htop1,
                         str(180 - i / 2))

    r = 90. * math.pi / 180.
    s = math.sin(r)
    mark(math.log(s * 10.), htop3, htop2, htop1, '90')

    footer()
    return 0

if __name__ == "__main__":
    main()
