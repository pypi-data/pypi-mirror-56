#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 xiongbai
# @contact: xiongbai@snowland.ltd
# @site: www.xiongbai.ltd
# @file: deal.py
# @time: 2019/10/25 3:34
# @Software: PyCharm


from abc import ABCMeta, ABC

from astar_qa.base import Deal
from astar_qa.base import Strategy, DataSet, Stock
from astar_qa.dataset.data import RealtimeData, HistoryData


class RealtimeDeal(Deal):

    def __init__(self, cash, stocks: list = None, fee=0.00006, leverage=2, dataset: RealtimeData = None, min_hand=100,
                 strategies: (Strategy, list) = None):
        """
        :param stocks: 金融票据列表
        :param fee: 手续费
        :param cash: 现金
        :param leverage: 杠杆率
        """
        if isinstance(dataset, RealtimeData):
            super(RealtimeDeal, self).__init__(stocks, cash, fee=fee, leverage=leverage, dataset=dataset,
                                               min_hand=min_hand, strategies=strategies)
        else:
            raise ValueError('RealtimeData')


class HistoryDeal(Deal):

    def __init__(self, cash, stocks: (list, Stock) = None, fee=0.00006, leverage=2, dataset: HistoryData = None,
                 min_hand=100,
                 strategies: (Strategy, list) = None):
        """
        :param stocks: 金融票据列表
        :param fee: 手续费
        :param cash: 现金
        :param leverage: 杠杆率
        """
        if isinstance(dataset, RealtimeData):
            super(HistoryDeal, self).__init__(stocks, cash, fee=fee, leverage=leverage, dataset=dataset,
                                              min_hand=min_hand, strategies=strategies)

        else:
            raise ValueError('RealtimeData')
