# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 用来存放数据的contesnts
"""
from abc import *
from typing import *


class Content(ABC):
    # 接口，为方便使用以链表形式组织
    Num = 0
    Head = None  # 头节点

    @abstractmethod
    def __init__(self):
        Content.Num += 1
        self.last = None
        self.next = None
        self.text = None
        self.reformed = False
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
            #减少需要处理的情况
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
            # todo
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
