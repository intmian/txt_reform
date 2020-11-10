# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 基础设备
"""

from config_file import config
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
    last_cap = -1
    # todo：解决当连续章节出错时显示的问题例如 1 2 2 2 3 or 1 2 5 3
    while p is not None:
        if type(p) is contents.Chapter:
            # 省略中间连续的，更快找出症结
            # todo: 更加优化，可以找出错误类型（缺章、错章、重复）并打出。可以全部打进列表
            n = p.num
            if n == last_cap + 1:
                pass
            elif n == 1:
                print("  章 ", 1)
            else:
                print("  ...")
                print("  章 ", last_cap)
                err = ""
                if last_cap == n:
                    err = "[与上一章重复]"
                if last_cap < n - 1:
                    err = "[与上一章不连续，中间缺章]"
                if last_cap > n:
                    # 此处不严谨，应该结合下个章节再判断
                    err = "[与上一章不连续，错章]"
                print("  章 ", n, err)
            last_cap = n
        elif type(p) is contents.Volume:
            if last_cap != -1:
                print("  ...")
                print("  章 ", last_cap)
                print("卷 ", p.num)
            else:
                print("卷 ", p.num)
        elif type(p) is contents.Text:
            pass
        elif type(p) is contents.Enter:
            pass
        p = p.next
    print("  ...")
    print("  章 ", last_cap)


def analyse_list(head):
    """
    打印链表,并分析错误
    """
    node = head
    nodes = []
    while node is not None:
        if type(node) is contents.Chapter:
            nodes.append((1, node.num))
        elif type(node) is contents.Volume:
            nodes.append((2, node.num))
        node = node.next

    t = []
    p = 0
    t2 = []  # 卷前章
    while p != len(nodes):
        n = nodes[p]
        if n[0] == 1:
            t2.append(n[1])
            p += 1
        if n[0] == 2:
            if len(t2) != 0:
                t.append(t2)
            p2 = p + 1
            t2 = []
            while p2 != len(nodes):
                t, n = node[p2]
                if t == 2:
                    p = p2
                    break
                if t == 1:
                    t2.append(n)
                    p2 += 1
            t.append(t2)
    if len(t) == 0:
        t.append(t2)
    for v in t:
        min_i = 0
        max_i = len(v) -1
        for i in range(v):
            if min_i < i < max_i:
                # 上面这个是什么玩意。。。
                if v[i - 1] + 1 == v[i] and v[i] + 1 == v[i + 1]:
                    v[i] = -1
    for v in t:
        print("卷 ", p.num)
        for i in range(v):

            chap = v[i]
            if i == 1:
                if chap != 1 and chap != 0:
                    pass






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


def ready(s):
    print(s + "... ")


def done():
    print("done")


if __name__ == '__main__':
    print(get_file())
