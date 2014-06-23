from pygame import *

import cardinals

from build import Build
from quit import Quit
from look import Look
from destroy import Destroy
from cast import Cast
from ready import Ready

lookup = {}
lookup[K_b] = Build
lookup[K_q] = Quit
lookup[K_l] = Look
lookup[K_g] = Destroy
lookup[K_c] = Cast
lookup[K_r] = Ready


