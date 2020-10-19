# -*- coding: UTF-8 -*-
"""
AUTHOR:   MIAN
DATE:     2020/10/20
DESCRIBE: 驱动程序
"""
import tool, contents, config
import os

if __name__ == '__main__':
    # 读入
    addr = tool.get_file()
    con = contents.Contents(addr)
    # 处理
    con.reform()
    s = con.output()
    # 输出
    (filepath, temp_filename) = os.path.split(addr)
    (filename, extension) = os.path.splitext(temp_filename)
    if not config.over:
        addr = filepath + "/" + filename + "_修改后" + extension
    with open(addr, "w", encoding=config.write_code) as file:
        file.write(s)
