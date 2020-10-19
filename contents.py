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
        last.next = self
        self.last = last

    def delete(self):
        """将自己从链表中脱链
        """
        Content.Num -= 1
        if self.last is None:
            self.next = None
            Content.head = None
            # 头节点，函数链需特别注意
        elif self.next is None:
            self.last = None
            # 尾节点
        else:
            self.last.next = self.next
            self.next.last = self.last
            self.next = None
            self.last = None

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
        pass


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


class Enter(Content):
    # 空行
    def __init__(self):
        super().__init__()
        self.text = tool.newline()

    def reform(self):
        super().reform()


class Chapter(Content):
    # 第？章
    def __init__(self, n: int):
        super().__init__()
        self.text = "第{}章".format(n)
        self.reform()

    def reform(self):
        super().reform()


class Volume(Content):
    # 第？卷
    def __init__(self, n: int):
        super().__init__()
        self.text = "第{}卷".format(n)
        self.reform()

    def reform(self):
        super().reform()


class Contents:
    # 容纳所有content
    def __init__(self, addr: str):
        """
        :param addr:需要被格式化的字符串地址
        """
        # 首尾指针
        self.head = Content.Head
        self.last = Content.Head
        self.reader = reader.Reader
