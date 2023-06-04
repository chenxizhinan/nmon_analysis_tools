#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 17:12
# @Author  : tx.lei
# @File    : analysis.py


"""

"""
import fileinput
import glob
import os
import csv
import datetime
import time
from src.utils.time_utils import time_format
import pandas as pd
import matplotlib.pyplot as plt

NMON_TYPE = ['AAA','BBBP','CPU_ALL','DISKBSIZE','DISKBUSY','DISKREAD','DISKWRITE','DISKXFER','JFSFILE','MEM','NET','NETPACKET','ZZZZ', 'PROC','TOP','VM']



class Nmonpy(object):

    def __init__(self):
        self.result_dir = os.path.dirname(os.path.abspath(__file__)) + '\\Result\\'       #与pytinstaller兼容
        self.zzzz = []
        self.time_map = {}
        self.output_files = {}



    def open_output_files(self):
        """创建分解输出的csv文件"""
        for data_type in NMON_TYPE:
            output_file_name = os.path.join(self.result_dir,f'{data_type}.csv')
            if os.path.exists(output_file_name):
                os.remove(output_file_name)
            print('{}'.format(output_file_name))
            self.output_files[data_type] = csv.writer(open(output_file_name, 'w',newline=''))

            # 设置时间表头
            if data_type == 'ZZZZ' :
                zzzz_header = "ZZZZ,taskId,date,day,full_time"
                self.output_files[data_type].writerow(zzzz_header.split(','))



    def clode_output_files(self):
        # 关闭所有输出文件
        for output_file in self.output_files.values():
            output_file.close()

    def integrate_to_excel(self):
        # TODO: 整合所有csv文件，输出到excel
        pass

    def get_fulltime_by_task(self,time_list):

        print("Analysis TIME ...")
        # 读取CSV文件
        data = pd.read_csv('./Result/ZZZZ.csv')

        # 设置Pandas的显示选项
        pd.set_option('display.max_columns', None)

        # 过滤数据
        filtered_data = data[data['taskId'].isin(time_list)]
        print(filtered_data)

        return filtered_data['full_time'].tolist()



    def top_analysis(self):
        # TODO: 对top进程分析绘图


        print("Analysis TOP ...")
        # 读取CSV文件
        data = pd.read_csv('./Result/TOP.csv')

        # 设置Pandas的显示选项
        pd.set_option('display.max_columns', None)

        # 过滤数据
        filtered_data = data[data['Command'] == 'barad_agent']
        print(filtered_data)

        # 显示数据统计信息
        print(filtered_data.describe())

        time_list = filtered_data['Time'].tolist()
        print(time_list)

        # 获取到时间列表
        filltime_list = self.get_fulltime_by_task(time_list)
        print(filltime_list)

        if filtered_data['+PID'].nunique() == 1:
            print("+PID列的值都相同")
        else:
            print("+PID列的值不都相同")
            print(filtered_data.groupby('+PID')['+PID'])




        # TODO: 绘制图表

        # TODO: 绘制CPU

        # TODO: 绘制内存变化图
        ResSet_list = filtered_data['ResSet'].to_list()
        from pyecharts.charts import Line, Timeline
        from pyecharts import options as opts

        # 创建时间轴和折线图对象
        timeline = Timeline()
        line_chart = Line()

        # 创建x和y轴数据
        # x = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01']
        # y1 = [3, 5, 2, 7, 1]


        # 添加数据到折线图中
        line_chart.add_xaxis(filltime_list)
        line_chart.add_yaxis('Y1', ResSet_list)
        # line_chart.add_yaxis('Y2', y2)

        # 将折线图添加到时间轴中
        timeline.add(line_chart, '2021')

        # 设置时间轴的时间点和格式
        timeline.add_schema(play_interval=1000, is_auto_play=True,
                            pos_left='center', pos_bottom='10%',
                            label_opts=opts.LabelOpts(formatter='{value}'))

        # 设置图表标题和坐标轴标签
        line_chart.set_global_opts(title_opts=opts.TitleOpts(title="Line Chart with Timeline"),
                                   xaxis_opts=opts.AxisOpts(name="Time"))

        # 显示图表
        timeline.render("line_chart.html")



    def analysis(self, file_path):

        top_first = True

        # 打开文件并迭代每一行
        for line in fileinput.input(file_path):
            line = line.rstrip()
            data_type = line.split(',')[0]

            if data_type in NMON_TYPE:

                # 跳过首次匹配到的TOP，第二次匹配到的才是TOP表的表头
                if top_first is True and data_type == 'TOP':
                    top_first = False
                    continue

                # 获取时间
                elif 'ZZZZ' == data_type:
                    print(line)
                    self.zzzz.append(line)
                    full_time = time_format(line.split(',')[2].strip() + "," + line.split(',')[3].strip())
                    self.time_map[line.split(',')[1].strip()] = full_time
                    line = line+","+full_time
                    self.output_files['ZZZZ'].writerow(line.split(','))

                else:
                    self.output_files[data_type].writerow(line.split(','))





        # print(self.zzzz)
        print(self.time_map)

        self.top_analysis()


    def main(self,file_path):
        self.open_output_files()
        self.analysis(file_path)
        # self.clode_output_files()
        self.top_analysis()



if __name__ == '__main__':
    Nmonpy().main("./VM-12-13-centos_230604_1047.nmon")