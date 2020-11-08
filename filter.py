# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/11/7
DESCRIBE: 适配过滤器
"""
from abc import *
from typing import *
import enum
from config_file.config import *


class SIGNAL(enum.Enum):
    # 由filters返回的信号
    REJECT_ALL = 1  # 拒绝所有
    REJECT_CHAP = 2  # 拒绝章
    REJECT_VOL = 3  # 拒绝卷
    REJECT_CV = 4  # 拒绝章卷
    REJECT_TEXT = 5  # 拒绝正文
    REJECT_ENTER = 6  # 拒绝空行
    REJECT_TE = 7  # 拒绝正文空行
    OK = 8


class Filter(ABC):
    @abstractmethod
    def filt(self, s: str) -> SIGNAL:
        pass


class MaxChapLen(Filter):
    # 超过章限长
    def filt(self, s: str) -> SIGNAL:
        if len(s) > max_chap_len:
            return SIGNAL.REJECT_CHAP
        else:
            return SIGNAL.OK


class MaxVolLen(Filter):
    # 超过章限长
    def filt(self, s: str) -> SIGNAL:
        if len(s) > max_vol_len:
            return SIGNAL.REJECT_VOL
        else:
            return SIGNAL.OK


class StrictEnd(Filter):
    # 末尾不能为。
    def filt(self, s: str) -> SIGNAL:
        if s[-1] in ["。"]:
            return SIGNAL.REJECT_CV


class Filters:
    def __init__(self):
        from config_file.filter_config import enable
        t = []
        # 新的filter这里也要配好
        if enable["max_chap_len"]:
            t.append(MaxChapLen())
        if enable["max_vol_len"]:
            t.append(MaxVolLen())
        if enable["strict_end"]:
            t.append(StrictEnd())
        self.filters = t

    def filt(self, s: str) -> []:
        t = []
        for f in self.filters:
            r = f.filt(s)
            if r not in t:
                t.append(r)
        return t


FILTERS = Filters()
