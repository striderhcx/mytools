#!/usr/bin/python
#coding=utf-8
import os
import commands
import sys

'''
用法:
sudo cp search_open.py  /usr/bin/
1. search_open.py -i task  #忽略大小写，在当前路径,搜索task字符串
2. search_open.py  task    #大小写敏感，在当前路径，搜索task字符串
'''

def test():
    print("\033[1;32m这是一段测试\033[0m")  # 1 高亮  32前景色绿色
    print("\033[1;42m这是一段测试\033[0m")  #  42背景色绿色
    print("\033[1;31;40m;这是一段测试\n123456") # 1高亮  31 红色   41黑色背景
    print("\033[4;31m这是一段测试\033[0m\n123")  #某段内容  4下划线

def log(*args, **kwargs):
    if  kwargs == {}:
        print(args)
    else:
        print(args, kwargs)

def main(*args, **kwargs):

    log("You wan to search: {}".format(sys.argv[1]))
    if len(sys.argv) == 3 and  '-i' in sys.argv[1]:
        ret, output = commands.getstatusoutput("grep -irn {} ./".format(sys.argv[2]))
    else:
        ret, output = commands.getstatusoutput("grep -rn {} ./".format(sys.argv[1]))
    lines = output.split('\n')
    opencomamnds=[]
    for index, line in enumerate(lines):
        #log(line.split(':', 2)[0], line.split(':', 2)[1])
        '''
        when noting found in current diretory, just return!
        '''
        if len(lines) == 1 and lines[0] == '':
            log("Noting found!")
            return
        try:
            result = lines[index].split(':',2)[-1]
            opencomamnds.append("vim {} +{}".format(line.split(':', 2)[0],  line.split(':', 2)[1]))
            '''
            这里用log函数，log不出高亮的颜色，why？
            '''
            print("command index={}  {}  \033[1;32m{}\033[0m".format(index, opencomamnds[-1], result))
        except IndexError:
            '''
            when a binary file match,will caught IndexError: list index out of range,we just print it
            '''
            print("\033[1;32m{}\033[0m".format(result))
    while True:
        sel = raw_input("please select your select:")
        log("You select command index={}".format(sel))
        try:
            os.system(opencomamnds[int(sel)])
        except IndexError:
            log("!!!!!!!!!!!!!error invalide index!!!!!!!!!!!!")

main()
