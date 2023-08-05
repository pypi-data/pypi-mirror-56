#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 xiongbai, A.Star
# @contact: xiongbai@snowland.ltd, astar@snowland.ltd
# @site: www.astar.ltd
# @file: macd_strategy.py
# @time: 2019/10/25 3:49
# @Software: PyCharm

from astar_qa.base import Strategy, TypeChoice, Stock
from astar_qa.base import Operation
from astar_qa.dataset.data import HistoryData, RealtimeData
# from astar_qa.base import Item
import numpy as np
import talib
import pandas as pd

npa = np.array


class MACDStrategy(Strategy):

    def __init__(self, data: list = None, d1=4, d2=2, delta=0.4, delta2=0.2, delta3=0.3, max_size=50):
        super(MACDStrategy, self).__init__(data=data, d1=d1, d2=d2, delta=delta, delta2=delta2, delta3=delta3)
        self.pre = None
        self.max_size = max_size
        self.bar = 0

    def __macd_decision(self):
        # 回测的话利用close做macd线
        # if ma.all() is None:
        #     # 实时的话用price做macd线
        #     # a = self.__get_next_data()
        #     ma = npa([each.price for each in self.data])
        ma = npa([each.price if each.close is None else each.close for each in self.data])
        if len(self.data) < self.max_size:
            return None

        # macd,signal,hist三个线
        # macd（对应diff），
        #
        # macdsignal（对应dea），
        #
        # macdhist（对应macd）。
        macd, signal, hist = talib.MACD(ma, fastperiod=12, slowperiod=26, signalperiod=9)
        # # 金叉出现
        # 入场原则
        # 多头盈利入场条件：
        if macd[-2] < signal[-2] and macd[-1] > signal[-1]:
            if hist[-2] < 0 and hist[-1] > 0:
                return TypeChoice.BUY_UP
            # 多头盈利终结
            if hist[-2] > 0 and hist[-1] < 0:
                return TypeChoice.SELL_UP
        # 空头盈利入场条件：
        if macd[-2] > signal[-2] and macd[-1] < signal[-1]:
            if hist[-2] > 0 and hist[-1] < 0:
                return TypeChoice.SELL_DOWN
            # 空头盈利终结
            if hist[-2] < 0 and hist[-1] > 0:
                return TypeChoice.BUY_DOWN
        return TypeChoice.WAIT

    # def __next__(self):
    #     while True:
    #         try:
    #             d = self.__macd_decision()
    #             print("一次操作")
    #             return d
    #         except:
    #             break

    def mk_sure_sell_down(self, *args, **kwargs):
        macd_decision = self.__macd_decision()
        return macd_decision == TypeChoice.SELL_DOWN

    def mk_sure_buy_up(self, *args, **kwargs):
        macd_decision = self.__macd_decision()
        return macd_decision == TypeChoice.BUY_UP

    def mk_sure_buy_down(self, *args, **kwargs):
        macd_decision = self.__macd_decision()
        return macd_decision == TypeChoice.BUY_DOWN

    def mk_sure_sell_up(self, *args, **kwargs):
        macd_decision = self.__macd_decision()
        return macd_decision == TypeChoice.SELL_UP
