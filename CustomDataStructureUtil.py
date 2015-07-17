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


def sort_dictionary_by_value(dictionary):
    """对一个value值可以比较的dictionary根据value进行排序 / Sort a dictionary by value while value in the dictionary are comparable

    :param dictionary:
        要排序的dictionary / The dictionary to be sort
    :return:
    """

    sorted_dictionary = {}
    while len(dictionary) > 0:
        sorted_dictionary.setdefault()

    # TODO
