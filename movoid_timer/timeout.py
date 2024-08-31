#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : timeout
# Author        : Sun YiFan-Movoid
# Time          : 2024/8/31 13:00
# Description   : 
"""
import time
from typing import Union


class TimeoutElement:
    def __init__(self, parent):
        self.time_start = time.time()
        self.time_end = None
        self.with_time_list = []
        self.time_with_start = None
        self.time_with_end = None
        self.parent: Timeout = parent
        self.should_pass = True

    def __enter__(self):
        self.time_with_start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.should_pass = False
        self.time_with_end = time.time()
        self.with_time_list.append(self.time_with_end - self.time_with_start)
        return True

    def end(self) -> float:
        self.time_end = time.time()
        return self.time

    @property
    def time(self) -> float:
        if self.time_end is None:
            return 0
        else:
            return self.time_end - self.time_start

    @property
    def with_time(self) -> Union[float, None]:
        if self.with_time_list:
            return sum(self.with_time_list)
        else:
            return None

    @property
    def index(self):
        return self.parent.index


class Timeout:
    """
    这是一个使用for方式调用的超时计时器。
    如果循环体顺利完成，那么直接推出循环
    如果循环体报错，则进行重试
    如果循环至超时，则直接报错
    循环体保证必定会执行第1轮的循环操作
    :param timeout:超时时间，到达后即立刻推出for in循环
    :param interval:最少间隔时间，即本次运行距离上次运行开始的最小间隔时间，如果不足则进行time.sleep的等待
    :param only_with:是否只有对循环体进行with操作的时间才是需要统计的超时时间
    :param last_0_when_no_with:如果循环中没有调用with，那么认为就是跑了0秒。如果置为False，那么将使用本次loop的时间作为with持续时间
    """

    def __init__(self, timeout: float = 60, interval=1, only_with=False, last_0_when_no_with=True):
        self.timeout = timeout
        self.interval = interval
        self.only_with = only_with
        self.last_0_when_no_with = last_0_when_no_with
        self.elements = []
        self.elements_time = []
        self.time_start = time.time()
        self.for_time = None  # 最后一次完成的for in究竟结算了多久的时间
        self.total_time = None  # 最后一次完成的for in究竟运行了多久

    def __iter__(self):
        self.elements = []
        self.elements_time = []
        self.time_start = time.time()
        self.time_last = 0
        self.index = -1
        self.now_timeout = TimeoutElement(self)
        self.elements.append(self.now_timeout)
        return self

    def __next__(self):
        if self.index >= 0:
            if self.now_timeout.should_pass:
                self.end()
            if self.only_with:
                this_loop_time = self.now_timeout.with_time
                if this_loop_time is None:
                    this_loop_time = 0 if self.last_0_when_no_with else self.now_timeout.end()
                self.time_last += this_loop_time
            else:
                this_loop_time = self.now_timeout.end()
                self.time_last = time.time() - self.time_start
            self.elements_time.append(this_loop_time)
            if self.time_last >= self.timeout:
                self.end(False)
            else:
                if this_loop_time < self.interval:
                    should_sleep = self.interval - this_loop_time
                    if self.timeout - self.time_last < should_sleep:
                        self.time_last += self.sleep(self.timeout - self.time_last)
                        self.end(False)
                    else:
                        if self.only_with:
                            self.time_last += self.sleep(should_sleep)
                        else:
                            self.sleep(should_sleep)
                            self.time_last = time.time() - self.time_start
            self.now_timeout = TimeoutElement(self)
            self.elements.append(self.now_timeout)
        self.index += 1
        return self.now_timeout

    def __len__(self):
        return len(self.elements)

    def end(self, should_pass=True):
        self.for_time = self.time_last
        self.total_time = time.time() - self.time_start
        if should_pass:
            raise StopIteration
        else:
            raise TimeoutError(f'循环耗时{self.for_time:.3f}秒，共计耗时{self.total_time:.3f}秒，已经超过时限{self.timeout}秒，最小间隔{self.interval}秒')

    @staticmethod
    def sleep(sleep_time: float = 0):
        start_time = time.time()
        time.sleep(sleep_time)
        return time.time() - start_time
