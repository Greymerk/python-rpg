from pygame import *

from src.util import cardinals

from build import Build
from quit import Quit
from look import Look
from destroy import Destroy
from cast import Cast
from ready import Ready

lookup = {}
lookup[K_b] = Build
lookup[K_l] = Look
lookup[K_c] = Cast



