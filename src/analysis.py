#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/4 17:12
# @Author  : tx.lei
# @File    : analysis.py


"""

"""
import fileinput
import glob
import linecache
import os
import csv
import datetime
import time

import numpy as np

from src.utils.time_utils import time_format
import pandas as pd
import matplotlib.pyplot as plt

NMON_TYPE = ['AAA', 'BBBP', 'CPU_ALL', 'DISKBSIZE', 'DISKBUSY', 'DISKREAD', 'DISKWRITE', 'DISKXFER', 'JFSFILE', 'MEM',
             'NET', 'NETPACKET', 'ZZZZ', 'PROC', 'TOP', 'VM']


class Nmonpy(object):

    def __init__(self):
        self.result_dir = os.path.dirname(os.path.abspath(__file__)) + '\\result\\'  # 与pytinstaller兼容
        self.zzzz = []
        self.fulltime_map = {}  # 保存时间的映射
        self.time_count = 0
        self.output_files = {}

    def open_output_files(self):
        """创建分解输出的csv文件"""
        for data_type in NMON_TYPE:
            output_file_name = os.path.join(self.result_dir, f'{data_type}.csv')
            if os.path.exists(output_file_name):
                os.remove(output_file_name)
            print('{}'.format(output_file_name))
            self.output_files[data_type] = csv.writer(open(output_file_name, 'w', newline=''))

            # 设置时间表头
            if data_type == 'ZZZZ':
                zzzz_header = "ZZZZ,taskId,date,day,full_time"
                self.output_files[data_type].writerow(zzzz_header.split(','))

    def clode_output_files(self):
        # 关闭所有输出文件
        for output_file in self.output_files.values():
            output_file.close()

    def integrate_to_excel(self):
        # TODO: 整合所有csv文件，输出到excel
        pass

    def get_time_count(self) -> int:

        if self.time_count != 0:
            return  self.time_count

        path = os.path.join(self.result_dir,"ZZZZ.csv")
        if os.path.exists(path):
            return  len(linecache.getlines(path)) - 1

        return 0

    def get_fulltime_by_task(self, time_list):

        print("Analysis TIME ...")
        # 读取CSV文件
        data = pd.read_csv('./result/ZZZZ.csv')

        # 设置Pandas的显示选项
        pd.set_option('display.max_columns', None)

        # 过滤数据
        filtered_data = data[data['taskId'].isin(time_list)]
        print(filtered_data)

        return filtered_data['full_time'].tolist()

    def get_fulltime_series(self) -> list:
        print("get_fulltime_series ...")
        # 读取CSV文件
        data = pd.read_csv('./result/ZZZZ.csv')

        # 设置Pandas的显示选项
        pd.set_option('display.max_columns', None)

        return data['full_time'].tolist()


    def get_top_series_data(self) -> dict:
        """
        获取top表每个进程的序列化数据
        :return
        {
            "pid-command1": {
                "cpu": [...],
                "size": [...],
            },
            "pid-commandn": {
                "cpu": [...],
                "size": [...],
            },
        }
        """

        print("Analysis TOP ...")
        # 读取CSV文件
        data = pd.read_csv('./result/TOP.csv')

        # 设置Pandas的显示选项
        pd.set_option('display.max_columns', None)

        # 根据不同的进程ID进行分组
        groups = data.groupby("+PID")

        process_series_datas = dict()
        # 遍历分组,name是分组名,group是分组数据
        for name, group in groups:
            # for key in group.keys():
            #     print(group[key])
            # TOP,+PID,Time,%CPU,%Usr,%Sys,Size,ResSet,ResText,ResData,ShdLib,MinorFault,MajorFault,Command

            command = group['Command'].tolist()[0]


            cpu_arr = np.zeros(self.get_time_count())
            usr_cpu_arr = np.zeros(self.get_time_count())
            sys_cpu_arr = np.zeros(self.get_time_count())
            size_arr = np.zeros(self.get_time_count())
            res_set_arr = np.zeros(self.get_time_count())
            res_text_arr = np.zeros(self.get_time_count())
            res_data_arr = np.zeros(self.get_time_count())
            shdlib_arr = np.zeros(self.get_time_count())

            # 根据采样的时间点对齐数据，采样时进程不存在则对应点位的值设置为0，采样时进程存在则设置对应点位的值
            for index, row in group.iterrows():
                # print(row['+PID'])
                # print(row['Time'])
                number = int(row['Time'][1:])-1
                cpu_arr[number] = row['%CPU']
                usr_cpu_arr[number] = row['%Usr']
                sys_cpu_arr[number] = row['%Sys']
                size_arr[number] = row['Size']
                res_set_arr[number] = row['ResSet']
                res_text_arr[number] = row['ResText']
                res_data_arr[number] = row['ResData']
                shdlib_arr[number] = row['ShdLib']

            process_series_data = dict()
            process_series_data['cpu'] = cpu_arr.tolist()
            process_series_data['usr_cpu'] = usr_cpu_arr.tolist()
            process_series_data['sys_cpu'] = sys_cpu_arr.tolist()
            process_series_data['size'] = size_arr.tolist()
            process_series_data['res_set'] = res_set_arr.tolist()
            process_series_data['res_text'] = res_text_arr.tolist()
            process_series_data['res_data'] = res_data_arr.tolist()
            process_series_data['shdlib'] = shdlib_arr.tolist()

            # 用进程号-命令名来作为key
            print(f"{str(name)}-{command}")
            process_series_datas[f"{str(name)}-{command}"] = process_series_data

        print(process_series_datas)
        return process_series_datas

    def get_top_series_data_filter_type(self,names = [],type="cpu"):
        """
        根据进程的ID-名称来进行模糊的过滤，同时返回过滤后的指定类型的序列
        :param names: 默认返回所有的序列，保留模糊匹配成功的序列
        :param type: 默认返回cpu序列，可选值：cpu,usr_cpu,sys_cpu,size,res_set,res_text,res_data,shdlib
        :return:
        {
            "pid-command1": {
                "cpu": [...],
                "size": [...],
            },
            "pid-commandn": {
                "cpu": [...],
                "size": [...],
            },
        }
        """
        series_map = self.get_top_series_data()

        if len(names) != 0:
            for key in list(series_map.keys()):
                match = False
                for name in names:
                    if str(key).__contains__(name):
                        match = True
                        break
                if not match:
                    del series_map[key]

        for key in series_map.keys():
            series_map[key] = series_map[key][type]



        return series_map



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
                    self.fulltime_map[line.split(',')[1].strip()] = full_time
                    line = line + "," + full_time
                    self.output_files['ZZZZ'].writerow(line.split(','))


                else:
                    self.output_files[data_type].writerow(line.split(','))

        # 记录共统计了多少次
        self.time_count = len(self.fulltime_map.keys())

        # print(self.zzzz)
        print(self.fulltime_map)

        self.get_top_series_data()

    def main(self, file_path):
        self.open_output_files()
        self.analysis(file_path)
        # self.clode_output_files()
        # self.get_top_series_data()


if __name__ == '__main__':
    Nmonpy().main("./VM-12-13-centos_230604_1047.nmon")
    print(Nmonpy().get_time_count())
    print(Nmonpy().get_top_series_data_filter_type())
