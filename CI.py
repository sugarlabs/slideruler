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
from C import mark, special_mark, header, footer
import math

htop1 = HTOP1
htop2 = HTOP2
htop3 = HTOP3
offset1 = 5
offset2 = 7
offset3 = -12


def main():

    header('CI')

    for i in range(100,200):
        if int((i / 10) * 10) == i:
            mark(math.log(i / 100.), htop3, htop2, htop1,
                 str(float(int(i) * 10 / SCALE)), flip=True)
        elif int((i / 5) * 5) == i:
            mark(math.log(i / 100.), htop3, htop2, htop1 + offset1, flip=True)
        else:
            mark(math.log(i / 100.), htop3, htop2, htop1 + offset2, flip=True)

        for i in range(200,400,2):
            if int((i / 10)*10) == i:
                mark(math.log(i / 100.), htop3, htop2, htop1,
                     str(float(int(i) * 10 / SCALE)), flip=True)
            else:
                mark(math.log(i/100.), htop3, htop2, htop1 + offset1, flip=True)

        for i in range(400,1005,5):
            if int((i / 10)* 10) == i:
                if int((i / 50) * 50) == i:
                    mark(math.log(i / 100.), htop3, htop2,
                         htop1, str(float(int(i) * 10 / SCALE)), flip=True)
                else:
                    mark(math.log(i / 100.), htop3, htop2, htop1, flip=True)
            else:
                mark(math.log(i / 100.), htop3, htop2, htop1 + offset1,
                     flip=True)

    special_mark(math.log(math.pi), htop3 + offset3, htop2, htop1, 'π',
                 flip=True)
    special_mark(math.log(math.e), htop3 + offset3, htop2, htop1, 'e',
                 flip=True)

    footer()
    return 0

if __name__ == "__main__":
    main()
