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

    while p is not None:
        if type(p) is contents.Chapter:
            # 省略中间连续的，更快找出症结
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


def analyse_list(head):  # todo:debug
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

    volumes = []
    p = 0
    chaps = []  # 卷前章
    v_nums = []
    while p != len(nodes):
        n = nodes[p]
        if n[0] == 1:
            chaps.append(n[1])
            p += 1
        if n[0] == 2:
            v_nums.append(n[1])
            if len(chaps) != 0 and len(volumes) == 0:
                volumes.append(chaps)
                # 卷前章
            p2 = p + 1
            chaps = []
            while p2 != len(nodes):
                t1, n1 = nodes[p2]
                if t1 == 2:
                    break
                if t1 == 1:
                    chaps.append(n1)
                    p2 += 1
            volumes.append(chaps)
            p = p2
    if len(volumes) == 0:
        volumes.append(chaps)  # 当没有章卷结构时
    for v in volumes:
        min_i = 0
        max_i = len(v) - 1
        for i in range(len(v)):
            if min_i < i < max_i:
                # 上面这个是什么玩意。。。
                if (v[i - 1] + 1 == v[i] or v[i-1] == -1) and v[i] + 1 == v[i + 1]:
                    v[i] = -1
    for vol_index in range(len(volumes)):
        v = volumes[vol_index]
        print("卷", v_nums[vol_index])
        skip = False
        for i in range(len(v)):
            err = ""
            chap = v[i]
            # 末章单独处理
            if i == len(v) - 1:
                print("  章", chap)
                continue
            # 第一章
            if i == 0:
                if chap != 1 and chap != 0:
                    err = "[本卷不以第一章开头]"
                    print("  章", chap, err)
                    continue
                else:
                    print("  章", chap, err)
                    continue
            pre = v[i - 1]
            next_n = v[i + 1]
            # 选择性打印省略号
            if chap == -1:
                if not skip:
                    print("  ...")
                    skip = True
                    continue
                else:
                    continue
            else:
                skip = False
            if pre == -1:
                print("  章", chap, err)
                continue
            if v[i - 2] + 1 == chap:
                continue

            if pre + 2 == next_n:
                err = "[乱章]"
            elif pre < chap:
                err = "[缺章]"
            elif pre > chap:
                err = "[错章]"
            elif pre == chap:
                err = "[重复]"
            print("  章", chap, err)


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
