#!/usr/bin/python3
# encoding=utf-8

__author__ = 'pc'


def get_min(dictionary):
    """获取面积最大的几种颜色中，面积最小的那种颜色
       Get the color with the least area.

    :param
        pixels_statistic_largest: 面积最大的几种颜色 / The colors with largest area
    :return:
        无 / None
    """
    minimal = 1500
    for k, v in dictionary.items():
        if v < minimal:
            minimal = v
            key = k
            value = v

    return key, value


def get_max(dictionary):
    """获取面积最大的几种颜色中，面积最大的那种颜色
       Get the color with the least area.

    :param
        pixels_statistic_largest: 面积最大的几种颜色 / The colors with largest area
    :return:
        无 / None
    """
    maximum = 0
    for k, v in dictionary.items():
        if v > maximum:
            minimal = v
            key = k
            value = v

    return key, value
