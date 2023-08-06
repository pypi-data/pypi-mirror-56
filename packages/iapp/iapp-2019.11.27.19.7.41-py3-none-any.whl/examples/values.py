#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : values
# @Time         : 2019-11-20 17:19
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


class Config(object):
    v = 1


def get_value():
    return Config.v


def set_value(v):
    Config.v = v

if __name__ == '__main__':
    print(get_value())
    set_value(1111)
    print(get_value())
