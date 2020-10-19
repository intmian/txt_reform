# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/19
DESCRIBE: 一个用来处理输入流的类
"""
import contents
import config
import tool
import re

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
        self.f = open(file_addr, 'r', encoding="utf-8")

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
                # 整行就是一个换行
                if temp == tool.newline():
                    yield contents.Enter()
                    temp = ""
                    continue
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
                # todo：处理中文数字放在章节名里的
                if re.match("(第)? *0*[0-9]+ *章 *.*", t):
                    name = t[t.rfind("章"):].strip()  # 章节名，如果没有就是空字符串构造函数里面有处理
                    yield contents.Chapter(int(re.findall(r'\d+', t)[0]), name)
                    temp = ""
                    continue
                elif re.match("(第)? *0*[0-9]+ *卷 *.*", t):
                    name = t[t.rfind("卷"):].strip()
                    yield contents.Volume(int(re.findall(r'\d+', t)[0]), name)
                    temp = ""
                    continue
                else:
                    yield contents.Text(t)
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
