#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

file_info = '''
 @Time    : 18/1/7 13:34
 @Author  : oujianhua
 @mail  : ojhtyy@163.com
 引用时, 要把本第一个 import , 以免打印不出 , 如git 
 '''

import logging
from  logging import config

#如果日志目录不存在, 在当前工作目录下创建Log文件夹 ,之后如果程序使用 os.chdir 切换目录 , 也不影响

log_dir="logs"  #跟配置文件中的 日志目录保持一致
if not log_dir in os.listdir(os.getcwd()):
     os.mkdir(log_dir)


#这里的路径 配对于执行者的路径 , 不是本文件的路径 这里,如果不同路径的执行者调用本脚本时, 会导致 找不到配置文件,
#config.fileConfig('conf/logging.conf')
#改成 获取到本文件的路径 再添加配置文件的路径 , 这样就可以把路径固定 不会出错
conf_file_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logging.cfg')
config.fileConfig(conf_file_full_path)

#通过调用时指定配置文件 调用时如： main.py dev|prod
env=None
try:
    env = sys.argv[1]
except IndexError as e:
    print("usage : python main.py dev|prod , please input parameter")
    sys.exit(0)
if env=='dev':
    logger = logging.getLogger('console')
else:
    logger = logging.getLogger('file')
if __name__=='__main__':
    #log = logging.getLogger('root') #获取 配置文件中的 root节点 通过root节点来处理日志
    #errorlog=logging.getLogger("error")  #通过配置文件中的error 节点处理日志 ,处理的信息会交给 root 再次处理
    #errorlog.error("9898989889") #传给  error 这个 logger 处理 后, 又给到 root再次处理

    logger.error("444444444")
    logger.info("iiiiiiiiiiii")

