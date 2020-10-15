# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/15
DESCRIBE: 配置
"""
from enum import Enum, auto


class System(Enum):
    LINUX = auto()
    WIN = auto()


env = System.WIN

