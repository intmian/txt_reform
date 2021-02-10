# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/2/10
DESCRIBE: 一些解耦出来的小模块
"""
from filter import FILTERS
from detector import DETECTORS


def judge_line(s: str):
    """
输出嗅探器与探测器对于
    :param s: 
    """
    sig = FILTERS.filt(s)
    ty = DETECTORS.detect(s)
    print(sig)
    print(ty[0], ty[1], ty[2])


judge_line("aaaaaaa")
