# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 基础设备
"""
from typing import *

import config
import contents


def get_file() -> str:
    """根据不同的系统，进行不同操作，返回路径
:return: 返回选中的文件路径
    """
    if config.env == config.System.WIN:
        import win32ui
        import win32con
        dlg = win32ui.CreateFileDialog(1, None, None, win32con.OFN_OVERWRITEPROMPT,
                                       "Text Files (*.txt)|*.txt||")  # 1表示打开文件对话框
        dlg.SetOFNInitialDir("")  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()
        return dlg.GetPathName()  # 获取选择的文件名称
    if config.env == config.System.LINUX:
        return input("请输入地址:")


def newline() -> str:
    """生成不同系统对应的换行符
:return: 返回换行符
    """
    return {config.System.WIN: "\n", config.System.LINUX: "\n"}[config.env]


def space_para() -> str:
    """
:return: 返回段首空格
    """
    # 所谓中文空格就是全角空格
    return config.para_space * " " + config.para_chi_space * "　"


def debug_list(head):
    """
    打印链表
    """
    p = head
    while p is not None:
        if type(p) is contents.Chapter:
            print("章 ", p.num)
        elif type(p) is contents.Volume:
            print("卷 ", p.num)
        elif type(p) is contents.Text:
            pass
        elif type(p) is contents.Enter:
            pass
        p = p.next


def all_do_list(head, func):
    """
对于每一个链表中的单元做func，注意：如果对于p点附近的节点做更改可能导致p失效
    :param head: 头节点
    :param func: 需要做的事func(p)
    """
    p = head
    while p is not None:
        func(p)
    p = p.next


if __name__ == '__main__':
    print(get_file())
