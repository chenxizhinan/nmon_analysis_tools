#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/6 23:48
# @Author  : tx.lei
# @File    : chart_utils.py
# @Description : generate py echarts

from pyecharts.charts import Line
from pyecharts import options as opts


def line_chart(title: str, x_title: str, x_series: list, y_title: str, y_series_name: str, y_series: list) -> Line:
    """
        生成包含多条折线的图表
        title：图表的标题
        x_title：x轴的标题
        x_series：x轴的数值列表
        y_title：y轴的标题
        y_series_name: y系列名
        y_series: y系列值

    """
    # 创建一个折线图对象
    line_chart = Line()

    # 添加 x 轴数据
    line_chart.add_xaxis(x_series)

    # 添加 y 轴数据
    line_chart.add_yaxis(y_series_name, y_series)

    # 设置全局配置项
    line_chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        legend_opts=opts.LegendOpts(orient='vertical', pos_right='10%'),
        datazoom_opts=[opts.DataZoomOpts()],
        xaxis_opts=opts.AxisOpts(
            name=x_title,
            axislabel_opts=opts.LabelOpts(rotate=-70),
        ),
        yaxis_opts=opts.AxisOpts(
            name=y_title,
            max_=1000
        )
    )
    # 显示图表
    line_chart.render("Sales.html")
    return line_chart


def multi_line_chart(title: str, x_title: str, x_series: list, y_title: str, y_series_data: dict) -> Line:
    """
        生成包含多条折线的图表
        title：图表的标题
        x_title：x轴的标题
        x_series：x轴的数值列表
        y_title：y轴的标题
        y_series_data: 包含多条折线的数据{key:value}分别表示系列名和数值

    """
    # 创建一个折线图对象
    line_chart = Line()

    # 添加 x 轴数据
    line_chart.add_xaxis(x_series)

    # 添加 y 轴数据
    for y_series_name, y_series in y_series_data.items():
        line_chart.add_yaxis(y_series_name, y_series)

    # 设置全局配置项
    line_chart.set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        legend_opts=opts.LegendOpts(type_='plain', orient='vertical', pos_right='0%'),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],  # inside表示内部缩放，slider表示滑动窗口
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",
        ),
        xaxis_opts=opts.AxisOpts(
            name=x_title,
            axislabel_opts=opts.LabelOpts(rotate=-70),
            interval=1
        ),
        yaxis_opts=opts.AxisOpts(
            name=y_title,
            # max_= 100
        ),
        toolbox_opts=opts.ToolboxOpts(
            is_show=True,
            feature={
                'saveAsImage': {'isShow': True},
                'dataView': {'isShow': True},
                'dataZoom': {'isShow': True},
                'magicType': {'isShow': True},
                'restore': {'isShow': True},
            },
            pos_top="0%",
            pos_left="15%",
        ),

    )

    # 显示图表
    line_chart.render("Sales.html")
    return line_chart


if __name__ == "__main__":
    line_chart()
