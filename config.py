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

para_space = 0  # 添加几个英文空格在段首
para_chi_space = 2  # 添加几个中文空格在段首
