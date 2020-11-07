# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/20
DESCRIBE: 驱动程序
"""
import tool, contents
from config_file import config
import os


def main():
    # 各个阶段也加入打表信息，并与debug分离
    # 读入
    tool.ready("正在读入文件")
    addr = tool.get_file()
    if addr == "":
        return
    con = contents.Contents(addr)
    # 处理
    tool.ready("文本结构展示")
    tool.debug_list(con.head)
    tool.done()
    con.reform()
    tool.ready("重整为单一文本")
    s = con.output()
    tool.done()
    # 输出
    tool.ready("导出")
    (filepath, temp_filename) = os.path.split(addr)
    (filename, extension) = os.path.splitext(temp_filename)
    if not config.over:
        addr = filepath + "/" + filename + "_修改后" + extension
    with open(addr, "w", encoding=config.write_code) as file:
        file.write(s)
    tool.done()


if __name__ == '__main__':
    main()
