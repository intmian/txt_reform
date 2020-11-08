# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/19
DESCRIBE: 一个用来处理输入流的类
"""
import contents
from config_file import config
import tool
import re
import filter, detector


# 记录一个非常奇怪的现象我写from contents import * 程序就报错说类未定义，令人不解
# 可能是因为contents还没完整跑完一遍就跳到这了，其实我也不清楚

class Reader:
    # 从输入流中读入
    def __init__(self, file_addr: str):
        """
        :param file_addr: 需要被读入的地址
        """
        self.exhausted = False  # 因为new里面有个迭代器可以调用，当一轮跑完时重新跑就返回None
        self.addr = file_addr
        # todo: 未来有时间的话这里写一个用chardet判断格式的
        self.f = open(file_addr, 'r', encoding=config.read_code)
        tool.done()

    def __del__(self):
        self.f.close()

    def gene(self):
        """
返回Content迭代器，如果为空则返回None
        """
        text = self.f.read()
        temp = ""
        for c in text:
            # 注意:用python的r模式读文件时根据系统的区别会用\n代替\n\r
            if c == "\n":
                temp += c
                # 将有效内容拿出
                t = ""
                if config.env == config.System.WIN:
                    if temp[-1:] == tool.newline():
                        t = temp[:-1]
                    else:
                        continue
                elif config.env == config.System.LINUX:
                    if temp[-1:] == tool.newline():
                        t = temp[:-1]
                    else:
                        continue
                else:
                    pass
                    # todo:报错，出现了不一样的换行符
                t = t.strip()  # 去除首尾空格
                signals = filter.FILTERS.filt(t)
                ty, num, name = detector.DETECTORS.detect(t)
                if ty == detector.TYPE.CHAPTER and \
                        filter.SIGNAL.REJECT_CHAP not in signals and \
                        filter.SIGNAL.REJECT_ALL not in signals and \
                        filter.SIGNAL.REJECT_CV not in signals:
                    # 章
                    yield contents.Chapter(int(num), name)
                elif ty == detector.TYPE.VOLUME and \
                        filter.SIGNAL.REJECT_VOL not in signals and \
                        filter.SIGNAL.REJECT_ALL not in signals and \
                        filter.SIGNAL.REJECT_CV not in signals:
                    # 卷
                    yield contents.Volume(int(num), name)
                elif ty == detector.TYPE.ENTER:
                    # 空行
                    yield contents.Enter()
                elif ty == detector.TYPE.TEXT:
                    # 段
                    yield contents.Text(name)
                temp = ""
                continue
            else:
                temp += c
        yield None


if __name__ == '__main__':
    addr = tool.get_file()
    r = Reader(addr)
    a = []
    for r in r.gene():
        a.append(r)

    print(a)
