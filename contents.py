# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 用来存放数据的contents
"""
from abc import *
from typing import *
import tool
import reader
from config_file import config


class Content(ABC):
    # 接口，为方便使用以链表形式组织
    Num = 0
    Head = None  # 头节点

    @abstractmethod
    def __init__(self):
        Content.Num += 1
        self.last = None
        self.next = None
        self.reformed = False
        self.text = None
        if Content.Head is not None:
            Content.Head = self

    def inject(self, last: object):
        """
        将此节点插入到某点之后
        :param last: 希望被插入的节点
        """
        if last is None:
            # 由程序结构决定只有这种可能
            Content.Head = self
            return
        t = last.next
        last.next = self
        self.last = last
        self.next = t
        if t is not None:
            t.last = self

    def delete(self):
        """将自己从链表中脱链
        """
        Content.Num -= 1
        if self.last is None:
            Content.head = None
            # 头节点，函数链需特别注意
        elif self.next is None:
            self.last.next = None
            # self.last = None  不必进行这一步，不清空可以让迭代器不失效
            # 尾节点
        else:
            self.last.next = self.next
            self.next.last = self.last
            # self.next = None
            # self.last = None

    def swap(self, node):
        """与某点
        :param node:
        """
        if self == node:
            return
        if node.next == self:
            # 减少需要处理的情况
            node.swap(self)
            return

        if self == Content.Head:
            Content.Head = node
        elif node == Content.Head:
            Content.Head = self

        sl = self.last
        sn = self.next
        nl = node.last
        nn = node.next

        if self.next == node:
            # 相邻
            if sl is not None:
                sl.next = node
            node.next = self
            self.next = nn
            if nn is not None:
                nn.last = self
            self.last = node
            node.last = sl
            return

        node.next = sn
        node.last = sl
        self.last = nl
        self.next = nn
        # 交换本身
        if sl is not None:
            sl.next = node
        if sn is not None:
            sn.last = node
        if nl is not None:
            nl.next = self
        if nn is not None:
            nn.last = self

    @abstractmethod
    def reform(self):
        """将自身格式化
        """
        self.reformed = True

    @abstractmethod
    def output(self) -> str:
        """输出内容
        """
        return self.text


class Text(Content):
    # 单行文本
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def reform(self):
        super().reform()
        # 去除首位的空格
        self.text = self.text.strip()
        # 补空格
        self.text = tool.space_para() + self.text + tool.newline()
        for i in range(config.text_enter):
            self.text += tool.newline()

    def output(self) -> str:
        return self.text


class Enter(Content):
    # 空行
    def __init__(self):
        super().__init__()
        self.text = tool.newline()

    def reform(self):
        super().reform()

    def output(self) -> str:
        return self.text


class Chapter(Content):
    # 第？章
    def __init__(self, n: int, name: str):
        super().__init__()
        self.text = "第{}章".format(n)
        self.num = n  # 用来作比较的，留着
        if name != "":
            self.text += " " + name
        self.text += tool.newline()
        self.child = []
        for i in range(config.chapter_enter):
            self.child.append(Enter())
            # 预先添加

    def reform(self):
        """
        将后面的正文节点全部折叠进此章节点内
        """
        # 将所有的子成员脱链后放进child数组
        super().reform()
        p = self.next
        while p is not None:
            if type(p) is Chapter:
                break
            elif type(p) is Volume:
                break
            elif type(p) is Text:
                p.reform()
                self.child.append(p)
                p.delete()
            elif type(p) is Enter:
                if config.delete_enter:
                    p.delete()  # 重整空行
                else:
                    self.child.append(p)
                    p.reform()
            p = p.next

    def output(self) -> str:
        r = self.text
        for c in self.child:
            r += c.output()
        return r


class Volume(Content):
    # 第？卷
    def __init__(self, n: int, name: str):
        super().__init__()
        self.text = "第{}卷".format(n)
        self.num = n  # 用来作比较的，留着
        if name != "":
            self.text += " " + name
        self.text += tool.newline()
        self.child = []
        for i in range(config.volume_enter):
            self.child.append(Enter())
            # 预先添加
        self.chap_num = 0  # TODO:增加更加泛用的统计

    def reform(self):
        # 将所有的子成员脱链后放进child数组
        super().reform()
        p = self.next
        while p is not None:
            if type(p) is Chapter:
                p.reform()
                self.child.append(p)
                self.chap_num += 1
            elif type(p) is Volume:
                break
            elif type(p) is Text:  # 仅文字空行被收入列表
                if self.chap_num == 0:
                    # TODO: 此处以及其他地方可以确认是否插入卷语与书语作为隐式章节

                    # 卷前语，仅在本卷第一章可能存在
                    if len(self.child) == config.volume_enter:
                        # 章节仅存在卷前回车
                        if config.debug:
                            print("第", self.num, "卷插入卷前语")
                        c = Chapter(0, "卷前语")
                        c.reform()
                        self.inject(c)
                        self.child.append(c)

                    p.reform()
                    self.child.append(p)
                    p.delete()
                else:
                    print("第", self.num, "卷，出现格式化错误，请检查程序")
            elif type(p) is Enter:
                if config.delete_enter:
                    p.delete()  # 重整空行
                else:
                    self.child.append(p)
                    p.reform()
            p = p.next

    def output(self) -> str:
        r = self.text
        if len(self.child) <= 10 and self.text != "第0卷 书前语\n":
            # 不用考虑吧不在卷内的章的情况
            print("第", self.num, "卷章节过少,请进行检查")
        for c in self.child:
            t = c.output()
            if type(c) is Chapter:
                if len(t) < 2000 and c.text != "第0章 卷前语\n":
                    # 因为 章一定在卷内所以字数判断放这里
                    print("第", self.num, "卷 第", c.num, "章字数过少,请进行检查")
                    # 这里会出现一个黄色提示，是因为pycharm只识别到我在v里面加了enter，而识别不到reform环节加的其他
            r += t
        return r


class Contents:
    # 容纳所有content
    def __init__(self, addr: str):
        """
        :param addr:需要被格式化的字符串地址
        """
        # 首尾指针
        self.head = Content.Head
        self.last = Content.Head
        self.reader = reader.Reader(addr)
        self.child = []
        no_chap = True
        no_volume = True
        tool.ready("生成文本链")
        for a in self.reader.gene():
            if a is not None:
                if self.head is None:
                    self.head = a
                a.inject(self.last)
                self.last = a
            if type(a) is Chapter:
                no_chap = False
            if type(a) is Volume:
                no_volume = False
        tool.done()

        tool.ready("插入隐式章卷")
        if no_chap:
            # 就是一段话没有章节划分
            c = Chapter(1, "总章")
            c.inject(self.head)
            c.swap(self.head)  # 插在最前
            self.head = c
        if no_volume:
            # 不分卷
            no = None
            c = None
            if type(self.head) is not Chapter:
                # 需要插入卷前语的时候

                no = 0
                c = Volume(no, "书前语")
                if config.debug:
                    print("插入隐式书前语")
            else:
                no = 1
                c = Volume(no, "自动生成卷")
                if config.debug:
                    print("插入隐式卷", no)

            c.inject(self.head)
            c.swap(self.head)  # 插在最前
            self.head = c
            last_chap = -1  # 上一章章节号

            # 扫描以生成隐式张卷
            p = self.head
            while p is not None:
                if type(p) is Chapter:
                    if p.num == 1 and (last_chap == -1 or last_chap > 5):
                        # 为了避免重复的第一章或短范围乱章被当成新的卷
                        no += 1
                        v = Volume(no, "自动生成卷")
                        v.inject(p.last)
                        if config.debug:
                            print("插入隐式卷", no)
                    last_chap = p.num
                p = p.next
        else:
            # 有卷的时候也需要检查是否需要插入书首语
            if type(self.head) is not Volume:
                # 需要插入书前语的时候
                if config.debug:
                    print("插入隐式书前语")
                c = Volume(0, "书前语")  # 对于存在0为卷号的情况会触发问题进行修复（我决定不修复了 TODO：修不修？）
                c.inject(self.head)
                c.swap(self.head)  # 插在最前

                self.head = c
        tool.done()

    def reform(self):
        """进行重整
        """
        p = self.head
        if p is None:
            p = Text("空文本")
        tool.ready("对各内容节点进行格式化并归并为连续结构")
        while p is not None:
            if type(p) is Chapter:
                p.reform()  # todo:这个情况是不可能的，应该抛个错误
            elif type(p) is Volume:
                p.reform()
                self.child.append(p)
            elif type(p) is Text:
                p.reform()
                self.child.append(p)
            elif type(p) is Enter:
                if config.delete_enter:
                    p.delete()  # 重整空行
                else:
                    p.reform()
                    self.child.append(p)
            p = p.next
        tool.done()
        self.cv_sort()
        self.delete_reduplicate()

    def delete_reduplicate(self):
        """
递归删除child的重复章卷
        """
        tool.ready("删除重复章卷")
        # 删除重复卷
        new_child = []
        last_num = -1  # 上一个章节号
        for c in self.child:
            if type(c) is Text:
                new_child.append(c)
            if type(c) is Enter:
                new_child.append(c)
            if type(c) is Volume:
                if c.num != last_num:
                    new_child.append(c)
                    last_num = c.num
                    # todo： 优化重复章删除，优先删除空章，而非删除除第一个的
                    # 删除重复章
                    new_child2 = []
                    last_num_2 = -1  # 上一个章节号
                    for cc in c.child:
                        if type(cc) is Text:
                            new_child2.append(cc)
                        if type(cc) is Enter:
                            new_child2.append(cc)
                        if type(cc) is Chapter:
                            if cc.num != last_num_2:
                                new_child2.append(cc)
                                last_num_2 = cc.num
                            else:
                                if config.debug:
                                    print("第", c.num, "卷 第", cc.num, "章重复已被删除")
                    c.child = new_child2
                else:
                    if config.debug:
                        print("第", c.num, "卷重复已被删除")
        self.child = new_child
        tool.done()

    def cv_sort(self):
        """
递归排序卷和章
        """

        # 排序必须是稳定的，不然卷前语和书前语顺序可能改变
        def key(a):
            # 专门为内部排序写的，只考虑可能的情况.所有非段卷只可能在最前面，保持不变
            if type(a) is Text or type(a) is Enter:
                return 0
            else:
                return a.num

        tool.ready("章卷排序")
        for c in self.child:
            if type(c) is Volume:
                # 每一卷进行卷内排序
                c.child.sort(key=key)
        # python3 删除了自定义的比较函数，所以只能这样写...
        self.child.sort(key=key)
        tool.done()

    def output(self) -> str:
        r = ""
        for c in self.child:
            r += c.output()
        return r
