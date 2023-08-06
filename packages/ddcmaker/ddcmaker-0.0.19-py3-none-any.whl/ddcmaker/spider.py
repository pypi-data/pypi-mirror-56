# -*- utf-8 -*-
"""蜘蛛侠来了"""
from ddcmaker import __version__
from ddcmaker import get_equipment_type as ge
from ddcmaker import Serial_Servo_Running as SSR
if ge.get_eq_type() == 3:
    class spider(object):
        def __init__(self):
            self.version = __version__

        def forward(self):
            # print()
            SSR.running_action_group('5',1)

        def backward(self):
            # print()
            SSR.running_action_group('6', 1)

        def left(self):
            print()

        def right(self):
            print()
