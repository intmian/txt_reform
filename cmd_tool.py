# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2021/2/10
DESCRIBE: 一些解耦出来的小模块
"""
import contents
import tool
from filter import FILTERS
from detector import DETECTORS
import sys


def judge_line(s: str):
    """
输出嗅探器与探测器对于
    :param s: 
    """
    sig = FILTERS.filt(s)
    ty = DETECTORS.detect(s)
    print(sig)
    print(ty[0], ty[1], ty[2])


def detect_struct():
    tool.ready("正在读入文件")
    addr = tool.get_file()
    if addr == "":
        return
    con = contents.Contents(addr)
    # 处理
    tool.ready("文本结构展示")
    tool.analyse_list(con.head)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("参数不足")
        exit(0)
    mode = sys.argv[1]
    if mode == "df":
        s = sys.argv[2]
        judge_line(s)
    elif mode == "show":
        detect_struct()
    else:
        exit(0)
