#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : timer
# Author        : Sun YiFan-Movoid
# Time          : 2024/1/11 21:51
# Description   : 
"""
import time


class TimerElement:
    def __init__(self, key):
        self.__key = key
        self.__flag = {}
        self.__time = None
        self.start()

    def start(self):
        self.__time = time.time()

    def stop(self) -> float:
        if self.__time is None:
            return 0
        else:
            total_time = time.time() - self.__time
            self.__time = None
            return total_time

    def set_flag(self, flag_name='__default__'):
        self.__flag[flag_name] = time.time()

    def get_flag(self, flag_name='__default__'):
        if self.__time is None:
            raise ValueError(f'{self.__key} timer has not started.')
        if flag_name in self.__flag:
            return self.__flag[flag_name] - self.__time
        else:
            raise KeyError(f'there is no {flag_name} in {self.__key} timer')

    @property
    def now(self):
        if self.__time is None:
            raise ValueError(f'{self.__key} timer has not started.')
        else:
            return time.time() - self.__time

    def check_time(self, check_time):
        check_time = float(check_time)
        return self.now >= check_time

    def check_interval(self, check_time):
        check_time = float(check_time)
        if self.check_time(check_time):
            self.__time.start()
            return True
        else:
            return False

    def now_digit(self, digit=2):
        return round(self.now, digit)

    def now_str(self, digit=2, sep=''):
        now_second = self.now_digit(digit)
        now_list = [now_second % 60]
        unit_list = ['s', 'm', 'h', 'd']
        now_minute = int((now_second - now_list[0]) // 60)
        now_list.append(now_minute % 60)
        now_hour = (now_minute - now_list[1]) // 60
        now_list.append(now_hour % 24)
        now_list.append((now_hour - now_list[2]) // 24)
        while len(now_list) > 1 and now_list[-1] == 0:
            now_list.pop()
        str_list = [f"{now_list[_]}{unit_list[_]}" for _ in range(len(now_list) - 1, 0, -1)]
        sec, msec = str(now_list[0]).split('.')
        msec = msec[:digit]
        str_list.append(f"{sec}{unit_list[0]}{msec}")
        return sep.join(str_list)

    def now_format(self, digit=0, str_format='{}d+{}:{}:{}'):
        digit = int(digit)
        now_second = self.now_digit(digit)
        now_list = [round(now_second % 60, digit)]
        unit_list = str_format.split('{}')
        start = unit_list.pop(0)
        now_minute = int((now_second - now_list[0]) // 60)
        now_list.append(now_minute % 60)
        now_hour = (now_minute - now_list[1]) // 60
        now_list.append(now_hour % 24)
        now_list.append((now_hour - now_list[2]) // 24)
        while len(now_list) > 1 and now_list[-1] == 0:
            now_list.pop()
        if digit == 0:
            format_text = "{:0>2.0f}{}"
        else:
            format_text = "{:0>" + str(digit + 3) + "." + str(digit) + "f}{}"
        str_list = ["{:2>0d}{}".format(now_list[_], unit_list[-_ - 1]) for _ in range(len(now_list) - 1, 0, -1)] + [format_text.format(now_list[0], unit_list[-1])]
        return start + ''.join(str_list)

    def delete(self):
        Timer.delete(self.__key)


class Timer:
    __timer = {}

    def __new__(cls, key='__default__') -> TimerElement:
        cls.__timer[key] = TimerElement(key)
        return cls.__timer[key]

    @classmethod
    def get(cls, item, *args):
        return cls.__timer.get(item, *args)

    @classmethod
    def delete(cls, item):
        Timer.__timer.pop(item)
