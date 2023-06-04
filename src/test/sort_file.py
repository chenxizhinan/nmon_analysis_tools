#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 16:35
# @Author  : tx.lei
# @File    : sort_file.py


# 读取文件内容并排序
filename = '../../source/VM-12-13-centos_230604_1652.nmon'
with open(filename, 'r') as f:
    lines = f.readlines()
sorted_lines = sorted(lines)

# 将排序后的内容写入新文件
new_filename = 'sorted.csv'
with open(new_filename, 'w') as f:
    f.writelines(sorted_lines)