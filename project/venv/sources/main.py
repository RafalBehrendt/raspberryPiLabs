from init import *
from menu import Menu
import sys

m = Menu()

if len(sys.argv) > 1:
    if sys.argv[1] == "F":
        firstInit()

init()

m.start()


