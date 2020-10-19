# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 用来存放数据的contents
"""
import functools
from abc import *
from typing import *
import tool
import reader
import config


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
        """将此节点插入到某点之后
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

    def reform(self):
        # 将所有的子成员脱链后放进child数组
        super().reform()
        p = self.next
        while p is not None:
            if type(p) is Chapter:
                p.reform()
                self.child.append(p)
            elif type(p) is Volume:
                break
            elif type(p) is Text:
                p.reform()
                self.child.append(p)
                p.delete()
                # 仅仅当出现在本卷第一章前作为卷语可以
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

        # todo：还需要处理空文本或者其他奇形怪状的不规范文本，不过这次算了
        if no_chap:
            # 就是一段话没有章节划分
            c = Chapter(1, "总章")
            self.head.inject(c)
            c.swap(self.head)  # 插在最前
        if no_volume:
            # 不分卷
            # 就是一段话没有章节划分
            c = Volume(1, "总卷")
            self.head.inject(c)
            c.swap(self.head)  # 插在最前

    def reform(self):
        """进行重整
        """
        p = self.head
        if p is None:
            p = Text("空文本")
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

        def cmp(a, b):
            # 专门为内部排序写的，只考虑可能的情况
            if type(a) is Text or type(a) is Enter:
                return False
            elif type(b) is Text or type(b) is Enter:
                return True
            elif a.num < b.num:
                return False
            return True

        for c in self.child:
            if type(p) is Volume:
                # 每一卷进行卷内排序
                c.child.sort(key=functools.cmp_to_key(cmp))
        # python3 删除了自定义的比较函数，所以只能这样写...
        self.child.sort(key=functools.cmp_to_key(cmp))

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
                                    print("第", cc.num, "章重复已被删除")
                    c.child = new_child2
                else:
                    if config.debug:
                        print("第", c.num, "卷重复已被删除")
        self.child = new_child

    def output(self) -> str:
        r = ""
        for c in self.child:
            r += c.output()
        return r
