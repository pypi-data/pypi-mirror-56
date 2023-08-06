# -*- utf-8 -*-
"""蜘蛛侠来了"""
from ddcmaker import __version__
from ddcmaker import get_equipment_type as ge
if ge.get_eq_type() == 3:
    class spider(object):
        def __init__(self):
            self.version = __version__

        def forward(self):
            print()

        def backward(self):
            print()

        def left(self):
            print()

        def right(self):
            print()
