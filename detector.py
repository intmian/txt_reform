# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/28
DESCRIBE: 章卷嗅探器
"""
import re
from abc import *
from typing import *
import enum

import tool


class TYPE(enum.Enum):
    CHAPTER = 1
    VOLUME = 2
    # 合理情况下以下的不会被访问到
    TEXT = 3
    ENTER = 4


class Detector(ABC):
    @abstractmethod
    def detect(self, s) -> (bool, TYPE):
        pass

    @abstractmethod
    def num(self, s) -> str:
        pass

    @abstractmethod
    def name(self, s) -> str:
        pass


def uni_get_num(t: str) -> str:
    """
从t中取出第一个中文或阿拉伯数字
    :param t: 来源
    :return: 取出的数字
    """
    num = re.findall("[0-9０-９零一二三四五六七八九十百千万]+", t)[0]
    # 转换为阿拉伯
    if num == "十":
        num = "10"
    elif num[0] == "十":
        num = "1" + num
    elif num[-1] == "十":
        num += "0"
    elif num[-1] == "百":
        num += "00"
    elif num[-1] == "千":
        num += "000"
    elif num[-1] == "万":
        num += "0000"
    s = ""
    n = {"１": "1", "２": "2", "３": "3", "４": "4", "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
         "０": "0",
         "一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9",
         "零": "0",
         "十": "", "百": "", "千": "", "万": ""}
    for c in num:
        if c in n:
            s = s + n[c]
        else:
            s += c
    return s

#todo: 看一看有没有比match更好的，其实不需要返回值
class Chap1(Detector):
    # 第*章 ***
    def detect(self, s) -> (bool, TYPE):
        return re.match(" *(第)? *0*[0-9０-９零一二三四五六七八九十百千万]+ *章 .*", s), TYPE.CHAPTER

    def num(self, s) -> str:
        return uni_get_num(s)

    def name(self, s) -> str:
        name = s[s.find("章") + 1:].strip()  # 章节名，如果没有就是空字符串构造函数里面有处理
        if name == "章":  # 这个和上面的做法合并才能搞出正确的结果
            name = ""
        return name


class Chap2(Detector):
    # *、 ***
    def detect(self, s) -> (bool, TYPE):
        return re.match(" *[0-9０-９零一二三四五六七八九十百千万]+、【.*】*", s), TYPE.CHAPTER

    def num(self, s) -> str:
        return uni_get_num(s)

    def name(self, s) -> str:
        name = s[s.find("、") + 1:].strip()  # 章节名，如果没有就是空字符串构造函数里面有处理
        if name == "、":  # 这个和上面的做法合并才能搞出正确的结果
            name = ""
        return name


class Chap3(Detector):
    # 第*章
    def detect(self, s) -> (bool, TYPE):
        return re.match(" *(第)?[0-9０-９零一二三四五六七八九十百千万]+章", s), TYPE.CHAPTER

    def num(self, s) -> str:
        return uni_get_num(s)

    def name(self, s) -> str:
        return ""


class Vol1(Detector):
    # 第*卷 aaa
    def detect(self, s) -> (bool, TYPE):
        return re.match(" *第 *0*[0-9０-９零一二三四五六七八九十百千万]+ *卷 *.*", s), TYPE.VOLUME

    def num(self, s) -> str:
        return uni_get_num(s)

    def name(self, s) -> str:
        name = s[s.find("卷") + 1:].strip()  # 章节名，如果没有就是空字符串构造函数里面有处理
        if name == "卷":  # 这个和上面的做法合并才能搞出正确的结果
            name = ""
        return name


class Vol2(Detector):
    # 第*卷
    def detect(self, s) -> (bool, TYPE):
        return re.match(" *第[0-9０-９零一二三四五六七八九十百千万]+卷", s), TYPE.VOLUME

    def num(self, s) -> str:
        return uni_get_num(s)

    def name(self, s) -> str:
        name = s[s.find("卷") + 1:].strip()  # 章节名，如果没有就是空字符串构造函数里面有处理
        if name == "卷":  # 这个和上面的做法合并才能搞出正确的结果
            name = ""
        return name


class Detectors:
    def __init__(self):
        # 添加新的detectors应在此处配置
        t = []
        from config_file.detect_config import enable
        if enable["Chap1"]:
            t.append(Chap1())
        if enable["Chap2"]:
            t.append(Chap2())
        if enable["Chap3"]:
            t.append(Chap3())
        if enable["Vol1"]:
            t.append(Vol1())
        if enable["Vol2"]:
            t.append(Vol2())

        self.detectors = t

    def detect(self, s: str) -> (TYPE, str, str):
        """
将文本解析为具体的content类型，并提取内容
        :param s: 文本
        :return : (类型，数字（仅对于章卷），内容)
        """
        if s == "":
            return TYPE.ENTER, "", ""
        for d in self.detectors:
            b, t = d.detect(s)
            if b:
                return t, d.num(s), d.name(s)
        return TYPE.TEXT, "", s


DETECTORS = Detectors()
