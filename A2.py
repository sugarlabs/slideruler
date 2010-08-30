# -*- coding: utf-8 -*-
#Copyright (c) 2009, 10 Walter Bender

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

htop1 = SHEIGHT - HTOP1
htop2 = SHEIGHT - HTOP2
htop3 = SHEIGHT - HTOP3 + 12
offset1 = - 5
offset2 = - 7
offset3 = 12


def main():

    header('A')

    for i in range(100, 200):
        if int((i / 10) * 10) == i:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1,
                 str(float(int(i) * 10 / SCALE)))
        elif int((i / 5) * 5) == i:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1 + offset1)
        else:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1 + offset2)

    for i in range(200, 400, 2):
        if int((i / 20) * 20) == i:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1,
                 str(float(int(i) * 10 / SCALE)))
        else:
            mark(math.log(i/100.) / 2, htop3, htop2, htop1 + offset1)

    for i in range(400, 1000, 5):
        if int((i / 10) * 10) == i:
            if int((i / 100) * 100) == i:
                mark(math.log(i / 100.) / 2, htop3, htop2,
                     htop1, str(float(int(i) * 10 / SCALE)))
            else:
                mark(math.log(i / 100.) / 2, htop3, htop2, htop1)
        else:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1 + offset1)

    for i in range(1000, 2000, 10):
        if int((i / 200) * 200) == i:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1,
                 str(float(int(i) * 10 / SCALE)))
        else:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1 + offset1)

    for i in range(2000, 10050, 50):
        if int((i / 1000) * 1000) == i:
            if int((i / 100) * 100) == i:
                mark(math.log(i / 100.) / 2, htop3, htop2,
                     htop1, str(float(int(i) * 10 / SCALE)))
            else:
                mark(math.log(i / 100.) / 2, htop3, htop2, htop1)
        else:
            mark(math.log(i / 100.) / 2, htop3, htop2, htop1 + offset1)

    special_mark(math.log(math.pi) / 2, htop3 + offset3, htop2, htop1, 'π')
    special_mark(math.log(math.e) / 2, htop3 + offset3, htop2, htop1, 'e')

    footer()
    return 0

if __name__ == "__main__":
    main()
