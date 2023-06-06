#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/7 0:27
# @Author  : tx.lei
# @File    : drawing.py
from src.analysis import Nmonpy
from src.utils.chart_utils import multi_line_chart

nnmon = Nmonpy()
x_series_data = nnmon.get_fulltime_series()
y_series_data = nnmon.get_top_series_data_filter_type(["kworker"])
line_chart = multi_line_chart("process","时间",x_series_data,"百分比",y_series_data)
line_chart.render("./cpu.html")

