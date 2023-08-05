#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: macd_deal.py
# @time: 2019/10/31 22:08
# @Software: PyCharm


from astar_qa.deal import RealtimeDeal, HistoryDeal
from astar_qa.dataset.data import RealtimeData, HistoryData
from astar_qa.base import buy_up, buy_down, sell_down, sell_up, Strategy, Stock
# from datetime import datetime
from astar_qa.base import Price, Operation, TypeChoice, Stock
from astar_qa.base import get_valuation
import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
from astar_qa.strategy.macd_strategy import MACDStrategy
import threading
import time
import json


class MACDRealtimeDeal(RealtimeDeal):
    """
    MACD实时代码
    """

    def __init__(self, cash, stocks: list = None, fee=0.00006, leverage=2, dataset: RealtimeData = None, min_hand=100,
                 strategies: MACDStrategy = None):
        """
        :param stocks: 金融票据列表
        :param fee: 手续费
        :param cash: 现金
        :param leverage: 杠杆率
        """
        super(MACDRealtimeDeal, self).__init__(cash, stocks, fee=fee, leverage=leverage, dataset=dataset,
                                               min_hand=min_hand, strategies=strategies)
        if strategies:
            if isinstance(strategies, MACDStrategy):
                self.strategies = [strategies]
            else:
                self.strategies = strategies
        else:
            self.strategies = []

    def buy_up(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = buy_up(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.BUY_UP, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def sell_up(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = sell_up(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                 self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.SELL_UP, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    # def buy_10_per(self, code, hand, price, *args, **kwargs):
    #     if isinstance(self.data[-1], Price):
    #         self.state = buy_down(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
    #                                 self.min_hand)
    #         self.operations.append(
    #             Operation(self.data[-1].time, code, TypeChoice:BUY_UP, hand, price, self.leverage, self.min_hand))

    def buy_down(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = buy_down(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                  self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.BUY_DOWN, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def sell_down(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = sell_down(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                   self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.SELL_DOWN, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def get_stocks_valuation(self):
        """
        获得股票估值
        :return:
        """
        return sum([get_valuation(stock, self.leverage, self.min_hand) for stock in self.stocks])

    def get_valuation(self):
        self.value = self.cash + self.get_stocks_valuation()
        return self.value


class MACDDealHistory(HistoryDeal):
    """
    MACD回测代码
    """

    def __init__(self, cash, stocks: (Stock, list) = None, fee=0.00006, leverage=2, dataset: HistoryData = None,
                 min_hand=100,
                 strategies: MACDStrategy = None):
        """
        :param stocks: 金融票据列表
        :param fee: 手续费
        :param cash: 现金
        :param leverage: 杠杆率
        """
        super(MACDDealHistory, self).__init__(cash, stocks, fee=fee, leverage=leverage, dataset=dataset,
                                              min_hand=min_hand, strategies=strategies)
        self.data = []
        if strategies:
            if isinstance(strategies, MACDStrategy):
                self.strategies = [strategies]
            else:
                self.strategies = strategies
        else:
            self.strategies = []

    def buy_up(self, code, price, hand, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = buy_up(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.BUY_UP, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def sell_up(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = sell_up(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                 self.min_hand)
            # sell_down(now, now_state: State, code, hand, price, leverage, fee, min_hand = 100):

            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.SELL_UP, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def buy_down(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = buy_down(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                  self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.BUY_DOWN, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def sell_down(self, code, hand, price, *args, **kwargs):
        if isinstance(self.data[-1], Price):
            self.state = sell_down(self.data[-1].time, self.state, code, hand, price, self.leverage, self.fee,
                                   self.min_hand)
            self.operations.append(
                Operation(self.data[-1].time, code, TypeChoice.SELL_DOWN, hand, price, self.leverage, self.min_hand))
        else:
            raise ValueError('error')

    def plot(self):
        col = []
        col2 = []
        for i in self.dataset:
            try:
                a = next(self.dataset)
                b = a.close
                c = a.time
                col.append(b)
                col2.append(c)
            except:
                ma = np.array(col)
                dif, dea, hist = talib.MACD(ma, fastperiod=12, slowperiod=9)
                df = pd.DataFrame({'dif': dif[33:], 'dea': dea[33:], 'hist': hist[33:]},
                                  index=col2[33:], columns=['dif', 'dea', 'hist'])
                df.plot(title='MACD')
                plt.show()


#
# # 历史回测
# if __name__ == '__main__':
#     b = HistoryData(code="600210")
#     a = MACDDealHistory(dataset=b, cash=100000, stocks=[], strategies=MACDStrategy(b))
#     pro = a.process()
#     # a.plot()
#     from astar_qa.base import MyEncoder
#     op = json.dumps(a.operations, cls=MyEncoder)
#     # print(op)
#     win = a.winning_table()
#     print(win)

# # 实时数据
if __name__ == '__main__':
    b = RealtimeData(code='600020')
    a = MACDRealtimeDeal(dataset=b, cash=None, stocks=[], strategies=MACDStrategy(b))
    while True:
        t1 = threading.Thread(target=a.process, name='first_thread')
        t1.start()
        time.sleep(1)
        t2 = threading.Thread(target=a.process, name='second_thread')
        t2.start()
        time.sleep(1)
