#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : test_timeout
# Author        : Sun YiFan-Movoid
# Time          : 2024/8/31 14:41
# Description   : 
"""
import time

from movoid_timer import Timeout


class Test_Timeout:
    def test_init(self):
        timeout = Timeout()
        timeout = Timeout(30)
        timeout = Timeout(interval=0.1)
        timeout = Timeout(22, 0.2)
        timeout = Timeout(only_with=False)
        timeout = Timeout(11, only_with=False)
        timeout = Timeout(only_with=False, interval=1.9)
        timeout = Timeout(99, 0.88, False)

    def test_timeout(self):
        timeout = Timeout(1, 0.1)
        for i, v in enumerate(timeout):
            assert i == v.index
            with v:
                if i <= 8:
                    raise Exception
        assert timeout.index == 9
        assert len(timeout) == 10
        assert 0.9 < timeout.for_time < 1
        assert 0.9 < timeout.total_time < 1
        try:
            for i, v in enumerate(timeout):
                assert i == v.index
                with v:
                    raise Exception
        except TimeoutError:
            pass
        else:
            raise Exception('超时后没有发出error')
        assert timeout.index == 9
        assert len(timeout) == 10
        assert 1 < timeout.for_time < 1.1
        assert 1 < timeout.total_time < 1.1

    def test_timeout_interval_less_than_loop(self):
        timeout = Timeout(1, 0.1)
        try:
            for i, v in enumerate(timeout):
                with v:
                    time.sleep(0.2)
                    assert i == v.index
                    raise Exception
        except TimeoutError:
            pass
        else:
            raise Exception('超时后没有发出error')
        assert timeout.index == 4
        assert len(timeout) == 5
        assert 1 < timeout.for_time < 1.2
        assert 1 < timeout.total_time < 1.2

    def test_timeout_only_with(self):
        timeout = Timeout(1, 0.1, True)
        try:
            for i, v in enumerate(timeout):
                time.sleep(0.1)
                with v:
                    time.sleep(0.1)
                    raise Exception
        except TimeoutError:
            pass
        else:
            raise Exception('超时后没有发出error')
        assert timeout.index == 9
        assert len(timeout) == 10
        assert 1 < timeout.for_time < 1.1
        assert 2 < timeout.total_time < 2.2

    def test_timeout_only_with_last_0_when_no_with(self):
        timeout = Timeout(1, 0, True, True)
        try:
            for v in timeout:
                if v.index % 2 == 0:
                    with v:
                        time.sleep(0.1)
                        raise Exception
                else:
                    time.sleep(0.1)
                    v.should_pass = False
        except TimeoutError:
            pass
        else:
            raise Exception('超时后没有发出error')
        assert 1 < timeout.for_time < 1.1
        assert 2 < timeout.total_time < 2.2
        timeout = Timeout(1, 0, True, False)
        try:
            for v in timeout:
                if v.index % 2 == 0:
                    with v:
                        time.sleep(0.1)
                        raise Exception
                else:
                    time.sleep(0.1)
                    v.should_pass = False
        except TimeoutError:
            pass
        else:
            raise Exception('超时后没有发出error')
        assert 1 < timeout.for_time < 1.1
        assert 1 < timeout.total_time < 1.1

    def test_timeout_break(self):
        timeout = Timeout(1, 0.1)
        for v in timeout:
            v.should_pass=False
            if v.index >= 5:
                break
        assert timeout.index == 5
        assert len(timeout) == 6

    def test_timeout_with_no_error(self):
        timeout = Timeout(1, 0.1)
        for v in timeout:
            with v:
                pass
        assert timeout.index == 0
        assert len(timeout) == 1
