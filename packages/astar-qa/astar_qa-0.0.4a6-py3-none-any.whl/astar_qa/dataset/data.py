#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 xiongbai
# @contact: xiongbai@snowland.ltd
# @site: www.xiongbai.ltd
# @file: data.py
# @time: 2019/10/25 3:31
# @Software: PyCharm


# from abc import ABCMeta
import tushare as ts
import talib
import numpy as np
import pandas as pd
from astar_qa.base import DataSet, Operation, Price



class RealtimeData(DataSet):
    """
    实时数据
    """

    def __init__(self, data=None, code=None, source=None):
        super(RealtimeData, self).__init__(data=data, code=code, source=source)
        self.source = ts
        self.pre = None
        # data = ts.get_realtime_quotes(self.code)
        # self.name = data.loc[0][0]
        # self.price = float(data.loc[0][3])
        # self.open = float(data.loc[0][1])
        # self.high = float(data.loc[0][4])
        # self.low = float(data.loc[0][5])

    def __get_data(self):
        # 获得实时数据
        data = self.source.get_realtime_quotes(self.code)
        time = data['time'][0]
        name = data.loc[0]['name']
        open = float(data.loc[0]['open'])
        close = None
        price = float(data.loc[0]['price'])
        high = float(data.loc[0]['high'])
        low = float(data.loc[0]['low'])
        msg = Price(time=time, code=self.code, name=name, price=price, open=open, close=close, high=high,
                    low=low)

        return msg

    # def call_back_Func(data):
    #     for key in ResultData.data:
    #         print(key, ResultData.data[key])

    def __next__(self):
        d = self.__get_data()
        if self.pre == d:
            raise StopIteration()
        self.pre = d
        return d


# a = RealtimeData(code='600106')
# a.realdata()


class HistoryData(DataSet):
    """
    历史数据
    """

    def __init__(self, data=None, code=None, source=None, start='', end=''):
        super(HistoryData, self).__init__(data=data, code=code, source=source)
        self.start = start
        self.end = end
        self.source = ts
        data_his = self.source.get_k_data(self.code, ktype='30', start=self.start, end=self.end)
        self.data = [
            # 时间，代码，None,None,收盘价，开盘价，最高价，最低价
            Price(each[0], self.code, None, None, float(each[2]), float(each[1]), float(each[3]), float(each[4])) for
            ind, each in enumerate(data_his.values)]
        self.ind = 0

    def __iter__(self, ktype='30'):
        return iter(self.data)

    def __next__(self):
        self.ind += 1
        if self.ind >= len(self.data):
            raise StopIteration("超出迭代次数")
        return self.data[self.ind]


if __name__ == '__main__':
    data = HistoryData(code='000002')
    while data:
        try:
            d = next(data)
            print(d)
        except:
            break
