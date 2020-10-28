# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/28
DESCRIBE: 章卷嗅探器
"""
from abc import *
from typing import *

class TYPE

class Detector(ABC):
    @abstractmethod
    def detect(self) -> (bool,TYPE):
        pass

    @abstractmethod
    def num(self, s):
        pass

    @abstractmethod
    def name(self, s):
        pass

