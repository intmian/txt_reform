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


env = System.WIN  # 根据系统环境选
para_space = 0  # 添加几个英文空格在段首
para_chi_space = 2  # 添加几个中文空格在段首
delete_enter = True  # 删除所有空行？（不包括后面的
chapter_enter = 1  # 章节名后添加几个空行
volume_enter = 1  # 卷后添加几个空行
text_enter = 1  # 段后额外添加几个空行
debug = True
over = False  # 是否覆盖原文件
