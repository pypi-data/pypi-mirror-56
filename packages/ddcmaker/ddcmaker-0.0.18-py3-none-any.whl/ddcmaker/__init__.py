'''不要随意修改类名和参数名，谁改谁背锅！！！！'''
__version__ = '0.0.18'
__metaclass__ = type
__all__ = [
    'car', 'robot'
]

import os
import subprocess
from inspect import signature
from functools import wraps
from ddcmaker import get_equipment_type as ge


def parameter_checking(*type_args, **type_kwargs):
    def decorate(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument [{}] must be {}'.format(name, bound_types[name]))
                    if value < 0:
                        raise ArithmeticError("Argument [{}] must be positive integer!".format(name))
            return func(*args, **kwargs)

        return wrapper

    return decorate

if ge.get_eq_type()== 0 :
    #####-------------------------------薛定谔的猫---------------------------------------
    def update(version):
        save_path = "/home/pi/human/resave/"
        link = "ddcmaker"+version           #拼接链接和版本号
        try:
            cmd = ("sudo wget -P  {} {}".format(save_path, link))
            ref = subprocess.call(cmd, shell=True)
            if ref != 0:
                print("can't get download")
            else:
                print("finishing downloading ! ")
                upcmd="sudo pip3 install "+save_path+"ddcmaker"+version            # #拼接链接和版本号组成安装命令
                try:
                    subprocess.call(upcmd, shell=True)
                except Exception as e:
                    print("安装失败", e)
        except Exception as e:
            print("失败是成功之母，我们下个版本见！bye~", e)


    #####-------------------------------量子塌陷之前状态同时存在---------------------------------------
    from ddcmaker import robot
    from ddcmaker import showlib

    Rb = robot.robot()
    Sh = showlib.showlib()


    class Robot(object):

        @staticmethod
        @parameter_checking(int)
        def left(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.left(step)

        @staticmethod
        @parameter_checking(int)
        def right(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.right(step)

        @staticmethod
        @parameter_checking(int)
        def left_slide(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.left_slide(step)

        @staticmethod
        @parameter_checking(int)
        def right_slide(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.right_slide(step)

        @staticmethod
        @parameter_checking(int)
        def forward(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.forward(step)

        @staticmethod
        @parameter_checking(int)
        def backward(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.backward(step)

        @staticmethod
        @parameter_checking(int)
        def up(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.up(step)

        @staticmethod
        @parameter_checking(int)
        def down(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.down(step)

        @staticmethod
        @parameter_checking(int)
        def check(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.check(step)

        # @staticmethod
        # def circle(step, radius):
        #     step = 10 if step > 10 else step
        #     Rb.circle(step, radius)

        @staticmethod
        @parameter_checking(int)
        def nod(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.nod(step)

        @staticmethod
        @parameter_checking(int)
        def shaking_head(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.shaking_head(step)

        '''虚不实真，苦切一除能，咒等等无是，咒上无是，咒明大是'''

        @staticmethod
        def hiphop():
            Sh.hiphop()

        @staticmethod
        def smallapple():
            Sh.smallapple()

        @staticmethod
        def jiangnanstyle():
            Sh.jiangnanstyle()

        @staticmethod
        def lasong():
            Sh.lasong()

        @staticmethod
        def feelgood():
            Sh.feelgood()

        '''无法兼容白色机器人，在调用时进行机器人判断'''
        @staticmethod
        def push_up():
            Rb.push_up()

        @staticmethod
        def abdominal_curl():
            Rb.abdominal_curl()

        @staticmethod
        def wave():
            Rb.wave()

        @staticmethod
        def bow():
            Rb.bow()

        @staticmethod
        def spread_wings():
            Rb.spread_wings()

        @staticmethod
        def haha():
            Rb.haha()

if ge.get_eq_type() == 1:
    #####-------------------------------正弦波是微观世界的基本单位---------------------------------------
    def update(version):
        save_path = "/home/pi/Car/resave/"
        link = "ddcmaker"+version           #拼接链接和版本号
        try:
            cmd = ("sudo wget -P  {} {}".format(save_path, link))
            ref = subprocess.call(cmd, shell=True)
            if ref != 0:
                print("can't get download")
            else:
                print("finishing downloading ! ")
                upcmd="sudo pip3 install "+save_path+"ddcmaker"+version            # #拼接链接和版本号组成安装命令
                try:
                    subprocess.call(upcmd, shell=True)
                except Exception as e:
                    print("安装失败", e)
        except Exception as e:
            print("失败是成功之母，我们下个版本见！bye~", e)


    #####-------------------------------波粒二象性是双缝干涉发现的---------------------------------------
    from ddcmaker import car

    Ca = car.car()


    class Car(object):

        @staticmethod
        @parameter_checking(int, int)
        def left(step=1, speed=50):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Ca.left(step, speed)

        @staticmethod
        @parameter_checking(int, int)
        def right(step=1, speed=50):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Ca.right(step, speed)

        @staticmethod
        @parameter_checking(int, int)
        def forward(step=1, speed=50):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Ca.forward(step, speed)

        @staticmethod
        @parameter_checking(int, int)
        def backward(step=1, speed=50):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Ca.backward(step, speed)

        @staticmethod
        def stop():
            Ca.stop(0)
if ge.get_eq_type() == 2:
    def update(version):
        save_path = "/home/pi/human_code/resave/"
        link = "ddcmaker"+version           #拼接链接和版本号
        try:
            cmd = ("sudo wget -P  {} {}".format(save_path, link))
            ref = subprocess.call(cmd, shell=True)
            if ref != 0:
                print("can't get download")
            else:
                print("finishing downloading ! ")
                upcmd="sudo pip3 install "+save_path+"ddcmaker"+version            # #拼接链接和版本号组成安装命令
                try:
                    subprocess.call(upcmd, shell=True)
                except Exception as e:
                    print("安装失败", e)
        except Exception as e:
            print("失败是成功之母，我们下个版本见！bye~", e)



    from ddcmaker import whiterobot
    from ddcmaker import showlib

    Rb = whiterobot.robot()
    Sh = showlib.showlib()

    class Robot(object):

        @staticmethod
        @parameter_checking(int)
        def left(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.left(step)

        @staticmethod
        @parameter_checking(int)
        def right(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.right(step)

        @staticmethod
        @parameter_checking(int)
        def left_slide(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.left_slide(step)

        @staticmethod
        @parameter_checking(int)
        def right_slide(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.right_slide(step)

        @staticmethod
        @parameter_checking(int)
        def forward(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.forward(step)

        @staticmethod
        @parameter_checking(int)
        def backward(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.backward(step)

        @staticmethod
        @parameter_checking(int)
        def up(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.up(step)

        @staticmethod
        @parameter_checking(int)
        def down(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.down(step)

        @staticmethod
        @parameter_checking(int)
        def check(step=1):
            if step > 1:
                step = 1
                print("参数值超过设置上限，默认运行最大上限次数 1")
            Rb.check(step)

        # @staticmethod
        # def circle(step, radius):
        #     step = 10 if step > 10 else step
        #     Rb.circle(step, radius)

        @staticmethod
        @parameter_checking(int)
        def nod(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.nod(step)

        @staticmethod
        @parameter_checking(int)
        def shaking_head(step=1):
            if step > 30:
                step = 30
                print("参数值超过设置上限，默认运行最大上限次数 ", step)
            Rb.shaking_head(step)

        '''虚不实真，苦切一除能，咒等等无是，咒上无是，咒明大是'''

        @staticmethod
        def jiangnanstyle():
            Sh.jiangnanstyle()


        @staticmethod
        def smallapple():
            Sh.smallapple()

        @staticmethod
        def lasong():
            Sh.lasong()

        @staticmethod
        def feelgood():
            Sh.feelgood()

        @staticmethod
        def fantastic_baby():
            Sh.fantastic_baby()

        @staticmethod
        def super_champion():
            Sh.super_champion()

        @staticmethod
        def youth_cultivation():
            Sh.youth_cultivation()

        @staticmethod
        def love_starts():
            Sh.Love_starts()

        @staticmethod
        def push_up():
            Rb.push_up()

        @staticmethod
        def abdominal_curl():
            Rb.abdominal_curl()

        @staticmethod
        def wave():
            Rb.wave()

        @staticmethod
        def bow():
            Rb.bow()

        @staticmethod
        def spread_wings():
            Rb.spread_wings()

        @staticmethod
        def straight_boxing():
            Rb.straight_boxing()

        @staticmethod
        def lower_hook_combo():
            Rb.lower_hook_combo()

        @staticmethod
        def left_hook():
            Rb.left_hook()

        @staticmethod
        def right_hook():
            Rb.right_hook()

        @staticmethod
        def punching():
            Rb.punching()

        @staticmethod
        def crouching():
            Rb.crouching()

        @staticmethod
        def yongchun():
            Rb.yongchun()

        @staticmethod
        def beat_chest():
            Rb.beat_chest()

        @staticmethod
        def left_side_kick():
            Rb.left_side_kick()

        @staticmethod
        def right_side_kick():
            Rb.right_side_kick()

        @staticmethod
        def left_foot_shot():
            Rb.left_foot_shot()

        @staticmethod
        def right_foot_shot():
            Rb.right_foot_shot()

        @staticmethod
        def show_poss():
            Rb.show_poss()

        @staticmethod
        def inverted_standing():
            Rb.inverted_standing()

        @staticmethod
        def rear_stand_up():
            Rb.rear_stand_up()



