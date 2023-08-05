#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star, xiongbai
# @contact: astar@snowland.ltd, xiongbai@snowland.ltd
# @site: www.xiongbai.ltd
# @file: base.py
# @time: 2019/10/25 3:50
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from collections import namedtuple
# from astar_qa.base import Strategy
import numpy as np
import matplotlib as plt
import pandas as pd
import datetime
import json
import time
# 监听模块
from multiprocessing import Process
# 导入枚举类
from enum import Enum


# Operation = namedtuple('Operation', ('time''min_hand'))
# Item = namedtuple('Item', ('time', 'code', 'hand', 'price', 'leverage', 'min_hand'))  # (时间， 手数, 单价, 杠杆率)
# Price = namedtuple('Price', ('time', 'code', 'name', 'open', 'close', 'high', 'low', 'price'))
# State = namedtuple('State', ('time', 'cash', 'stocks'))
# Stock = namedtuple('State', ('code', 'hand', 'min_hand', 'price'))

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, Operation):
            return str(obj.__dict__())
        else:
            return json.JSONEncoder.default(self, obj)


# 操作类
class Operation(object):
    def __init__(self, time, code, type_choice, hand, price, leverage, min_hand):
        self.time = time
        self.code = code
        self.type_choice = type_choice
        self.hand = hand
        self.price = price
        self.leverage = leverage
        self.min_hand = min_hand

    def __dict__(self):
        return {
            'time': self.time,
            'code': self.code,
            'type_choice': self.type_choice.value,
            'hand': self.hand,
            'price': self.price,
            'leverage': self.leverage,
            'min_hand': self.min_hand
        }

    def __str__(self):
        return "<" + str(self.hand) + ">"


# 价格类
class Price(object):
    def __init__(self, time, code, name, open, close, high, low, price):
        self.time = time
        self.code = code
        self.name = name
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.price = price

    def __str__(self):
        return str((self.time, self.code, self.name, self.open, self.close, self.high, self.low, self.price))

    def __eq__(self, other):
        if isinstance(other, Price):
            return (self.time, self.code, self.name, self.open, self.close, self.high, self.low, self.price) == \
                   (other.time, other.code, other.name, other.open, other.close, other.high, other.low, other.price)
        else:
            return False


# 状态类
class State(object):
    def __init__(self, time, cash, stocks):
        self.time = time
        self.cash = cash
        self.stocks = stocks


# 股票类
class Stock(object):
    def __init__(self, code, hand, min_hand, price):
        self.code = code
        self.hand = hand
        self.min_hand = min_hand
        self.price = price


# 继承枚举类
class TypeChoice(Enum):
    WAIT = 0
    BUY_UP = 1
    BUY_DOWN = 2
    SELL_UP = 3
    SELL_DOWN = 4


class TradeDetail:
    def __init__(self, price_buy, buy_time, type_choice: TypeChoice, price_sell, sell_time):
        """
        :param price_buy:
        :param buy_time:
        :param type_choice:
        :param price_sell:
        :param sell_time:
        """
        self.price_buy = price_buy
        self.buy_time = buy_time
        self.type_choice = type_choice
        self.price_sell = price_sell
        self.sell_time = sell_time


class DataSet(metaclass=ABCMeta):
    """
    数据抽象类
    """

    def __init__(self, data=None, code=None, source=None):
        if source is None:
            self.source = None
            self.data = data
            self.code = code
        else:
            # TODO
            pass

    def __iter__(self):
        if self.data:
            return iter(self.data)
        else:
            raise StopIteration()

    def __str__(self):
        return "<" + self.__name__ + ">" + str(self.data)


class Strategy(metaclass=ABCMeta):

    def __init__(self, data: list, d1=4, d2=2, delta=0.4, delta2=0.2, delta3=0.3, max_size=50):
        if data:
            data = []
        if not isinstance(data, list):
            raise ValueError('data must be list')

        self.data = data
        self.d1 = d1  # 进仓窗口
        self.d2 = d2  # 出仓窗口
        self.delta = delta  # 缩量上涨指标
        self.delta2 = delta2  # 缩量下降指标
        self.delta3 = delta3  # 缩量平稳指标
        self.max_size = max_size

    # 列表获得新数据后更新缓冲区
    def update_data(self, data, *args, **kwargs):
        if isinstance(data, list):
            self.data.extend(data)
        elif isinstance(data, Price):
            self.data.append(data)
        self.data = self.data[-self.max_size:]

    @abstractmethod
    def mk_sure_buy_up(self, *args, **kwargs):
        """
        是否买涨
        :return:
        """
        pass

    @abstractmethod
    def mk_sure_buy_down(self, *args, **kwargs):
        """
        是否买涨
        :return:
        """
        pass

    @abstractmethod
    def mk_sure_sell_up(self, *args, **kwargs):
        """
        是否卖涨
        :return:
        """
        pass

    @abstractmethod
    def mk_sure_sell_down(self, *args, **kwargs):
        """
        是否卖跌
        :return:
        """
        pass


class Deal(metaclass=ABCMeta):

    def __init__(self, cash, stocks: (list, Stock) = None, fee=0.00006, leverage=2, dataset: DataSet = None,
                 min_hand=100,
                 strategies: (Strategy, list) = None):
        """
        :param stocks: 金融票据列表
        :param fee: 手续费
        :param cash: 现金
        :param leverage: 杠杆率
        """
        self.stocks = stocks if stocks is not None else []
        self.fee = fee
        self.cash = cash
        self.state = State(datetime.datetime.now(), stocks, cash)
        self.operations = []
        self.leverage = leverage
        self.data = []
        if isinstance(dataset, DataSet):
            self.dataset = dataset
        else:
            raise ValueError('error in dataset.')
        self.min_hand = min_hand
        if strategies:
            if isinstance(strategies, Strategy):
                self.strategies = [strategies]
            else:
                self.strategies = strategies
        else:
            self.strategies = []

    def get_stocks_valuation(self):
        """
        获得股票估值
        :return:
        """
        return sum([get_valuation(stock, self.leverage, self.min_hand) for stock in self.stocks])

    def get_valuation(self):
        """
        计算估值
        :return:
        """
        return self.get_stocks_valuation() + self.cash

    def process(self, *args, **kwargs):
        """
        运行方法
        :return:
        """

        while True:
            try:
                each_data = next(self.dataset)
                self.data.append(each_data)
                # print(len(self.data))
                print(each_data)
                for strategy in self.strategies:
                    strategy.update_data(each_data)
                    if isinstance(strategy, Strategy):
                        if strategy.mk_sure_buy_down(self.data, *args, **kwargs):
                            self.buy_down(code=self.data[-1].code, price=self.data[-1].price, hand=0.2, *args, **kwargs)
                        elif strategy.mk_sure_buy_up(self.data, *args, **kwargs):
                            self.buy_up(code=self.data[-1].code, price=self.data[-1].price, hand=0.2, *args, **kwargs)
                        elif strategy.mk_sure_sell_down(self.data, *args, **kwargs):
                            self.sell_down(code=self.data[-1].code, price=self.data[-1].price, hand=0.2, *args, **kwargs)
                        elif strategy.mk_sure_sell_up(self.data, *args, **kwargs):
                            self.sell_up(code=self.data[-1].code, price=self.data[-1].price, hand=0.2, *args, **kwargs)
                        else:
                            print("正在收集数据，尚未决策")
                            pass
                    else:
                        raise ValueError('返回状态值错误')
            except StopIteration:
                # print('迭代完成')
                break
        return self.operations

    def winning_table(self):
        sell = []
        buy = []
        ma_re = []
        re = []
        row = 0
        for i in self.operations:
            if i.type_choice == TypeChoice.SELL_DOWN or i.type_choice == TypeChoice.SELL_UP:
                sell.append(i.price)
            elif i.type_choice == TypeChoice.BUY_UP or i.type_choice == TypeChoice.BUY_DOWN:
                buy.append(i.price)
        for l in range(min(len(sell), len(buy))):
            re.append(sell[l] - buy[l])  # 列表每次交易的收益 # 列表每次交易的收益

        re = np.array(re)
        max_re = max(re)
        min_re = min(re)
        ret = sum(re)  # 用卖出数列减去买入数列得到收益点数，然后对所有收益求和
        s = sum(re > 0)
        win = sum(re[re > 0])
        loss = sum(re[re <= 0])
        # print(s)
        if s == len(sell):
            winloss_rate = win
        elif (s == 0.0):
            winloss_rate = 0
        else:
            winloss_rate = (win / s) / (abs(loss) / (len(sell) - s))
        win_rate = s / len(sell)
        # 把收益点数和相应的均线参数存到表格中
        ma_re.append(round(ret, 2))
        ma_re.append(round(max_re, 2))
        ma_re.append(round(min_re, 2))
        ma_re.append(round(win_rate, 2))
        ma_re.append(round(winloss_rate, 2))
        return ma_re

    @abstractmethod
    def buy_up(self, code, hand, price, *args, **kwargs):
        pass

    @abstractmethod
    def sell_up(self, code, hand, price, *args, **kwargs):
        pass

    @abstractmethod
    def buy_down(self, code, hand, price, *args, **kwargs):
        pass

    @abstractmethod
    def sell_down(self, code, hand, price, *args, **kwargs):
        pass

    def run(self):
        """
        运行
        :return:
        """
        p = Process(target=self.process, kwargs={"code": "600106"})
        p.start()


def get_valuation(stock: Stock, leverage, min_hand=100):
    """
    :param stock: 期货(Operation)
    :param leverage: 杠杆率
    :param min_hand: 最小手数
    :return:
    """
    return stock.hand * stock.price * min_hand / leverage


def buy_up(now, now_state: State, code, hand, price, leverage, fee, min_hand=100):
    """
    :param now: 时间
    :param now_state: 当前状态
    :param hand: 手数
    :param price: 价格
    :param min_hand: 最小手数
    :return:
    """
    now_time, now_cash, now_stocks = now_state.time, now_state.cash, now_state.stocks
    flag = True
    for i, each_stock in enumerate(now_stocks):
        if each_stock.code == code:
            flag = False
        if flag is False:
            stock = now_stocks.pop(i)
            now_stocks.append(Stock(stock.code, stock.hand + hand, stock.min_hand,
                                    (stock.price * stock.hand + hand * price) / (stock.hand + hand)))
        else:
            now_stocks.append(Stock(code, hand, min_hand, price))
    now_cash -= (hand * price * min_hand / leverage) * (1 + fee)
    return State(now, now_cash, now_stocks)


def sell_up(now, now_state: State, code, hand, price, leverage, fee, min_hand=100):
    now_time, now_cash, now_stocks = now_state.time, now_state.cash, now_state.stocks
    flag = True
    for i, each_stock in enumerate(now_stocks):
        if each_stock.code == code:
            flag = False
        if flag is False:
            stock = now_stocks.pop(i)
            if stock.hand > hand:
                now_stocks.append(Stock(stock.code, stock.hand - hand, stock.min_hand,
                                        (stock.price * stock.hand - hand * price) / (stock.hadn + hand)))
            else:
                raise ValueError("当前所持手数不足以卖出这么多手")
        else:
            raise ValueError('当前所持没有这个股票')
    now_cash += (hand * price * min_hand / leverage) * (1 - fee)
    return State(now, now_cash, now_stocks)


def buy_down(now, now_state: State, code, hand, price, leverage, fee, min_hand=100):
    now_time, now_cash, now_stocks = now_state.time, now_state.cash, now_state.stocks
    flag = True
    for i, each_stock in enumerate(now_stocks):
        if each_stock.code == code:
            flag = False
        if flag is False:
            stock = now_stocks.pop(i)
            now_stocks.append(Stock(stock.code, stock.hand + hand, stock.min_hand,
                                    (stock.price * stock.hand + hand * price) / (stock.hand + hand)))
        else:
            now_stocks.append(Stock(code, hand, min_hand, price))
    now_cash -= (hand * price * min_hand / leverage) * (1 + fee)
    return State(now, now_cash, now_stocks)


def sell_down(now, now_state: State, code, hand, price, leverage, fee, min_hand=100):
    now_time, now_cash, now_stocks = now_state.time, now_state.cash, now_state.stocks
    flag = True
    for i, each_stock in enumerate(now_stocks):
        if each_stock.code == code:
            flag = False
        if flag is False:
            stock = now_stocks.pop(i)
            if stock.hand > hand:
                now_stocks.append(Stock(stock.code, stock.hand - hand, stock.min_hand,
                                        (stock.price * stock.hand - hand * price) / (stock.hadn + hand)))
            else:
                raise ValueError("当前所持手数不足以卖出这么多手")
        else:
            raise ValueError('当前所持没有这个股票')
    now_cash += (hand * price * min_hand / leverage) * (1 - fee)
    return State(now, now_cash, now_stocks)
