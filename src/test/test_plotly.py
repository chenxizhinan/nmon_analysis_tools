#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 15:23
# @Author  : tx.lei
# @File    : test_plotly.py

import os
import csv

# 打开nmon输出文件
with open('../../source/VM-12-13-centos_230604_1652.nmon', 'r') as f:
    # 读取所有行
    lines = f.readlines()

# 初始化输出文件字典
output_files = {}

# 迭代每一行
for line in lines:
    # 检查行是否以'AAA'开头，如果是，则表示一个新的数据类型
    if line.startswith('AAA'):
        # 提取数据类型名称
        data_type = line.split(',')[1].strip()

        # 初始化新的CSV输出文件
        output_file_name = f'{data_type}.csv'
        output_files[data_type] = csv.writer(open(output_file_name, 'w'))

    # 如果当前行表示数据，则将其写入当前数据类型的CSV文件中
    if line.startswith('T') and data_type:
        output_files[data_type].writerow(line.split(','))

# 关闭所有输出文件
for output_file in output_files.values():
    output_file.close()