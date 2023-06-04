#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 17:06
# @Author  : tx.lei
# @File    : time_utils.py


"""
时间操作工具
"""

from datetime import datetime


def time_format(time_str):
    """
        时间格式化，示例：
            将16:52:55,04-JUN-2023 格式化成 2023-06-04 16:52:55
        :return:
    """
    # 将时间字符串转换为datetime对象
    dt = datetime.strptime(time_str, '%H:%M:%S,%d-%b-%Y')
    # 将datetime对象格式化为字符串
    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    # print(formatted_time) # 输出: 2023-06-04 16:52:55
    return formatted_time