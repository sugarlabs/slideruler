# -*- coding: utf-8 -*-
#Copyright (c) 2010, Walter Bender

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
log10 = math.log(10)

def main():

    header('L')

    for i in range(0, 101):
        if int((i / 10) * 10) == i:
            mark((i / 100.) * log10, htop3, htop2, htop1,
                 str(float(int(i) * 100 / SCALE)))
        elif int((i / 5) * 5) == i:
            mark((i / 100.) * log10, htop3, htop2, htop1 + offset1)
        else:
            mark((i / 100.) * log10, htop3, htop2, htop1 + offset2)

    special_mark(math.pi / 10 * log10, htop3 + offset3, htop2, htop1, 'π')
    special_mark(math.e / 10 * log10, htop3 + offset3, htop2, htop1, 'e')

    footer()
    return 0

if __name__ == "__main__":
    main()
