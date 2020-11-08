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
over = False  # 是否覆盖原文件
read_code = "gbk"  # 源文件编码
write_code = "utf-8"  # reform后编码

max_chap_len = 30  # 最大章节名长度，超过会被当成普通文本，主要还是为了避免有些特殊情况
max_vol_len = 30

debug = True