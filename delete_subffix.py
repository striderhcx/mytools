#!/usr/bin/python2
#coding=utf-8
import os
import sys

'''
用法:
1. delete_subffix.py .txt  ./ #删除当前目录的所有.txt后缀的文件，第二个参数默认是当前目录可以不写
'''
def delete_suffix(suffix=None, delete_dirs="./"):
    foundLists = []
    for root, dirs, files in os.walk(delete_dirs):
        for name in files:
            print(os.path.join(root, name), name)
            if name != "delete_subffix.py" and suffix[1:] in name.rsplit('.',1)[-1]:
                foundLists.append(os.path.join(root, name))
                #os.remove(os.path.join(root, name))
    if len(foundLists) == 0:
        print("\"{}\" files not Found".format(suffix))
    key = raw_input("Do you really want to delete \"{}\" files?".format(suffix))
    if key in 'Yy':
        for f in foundLists:
            os.remove(f)
    else:
        print("you don't want to delete \"{}\" file".format(suffix))


def main():
    if len(sys.argv) == 3:
        print("arv[1]={0}; argv[2]={1}".format(sys.argv[1], sys.argv[2]))
        delete_suffix(suffix=sys.argv[1],delete_dirs=sys.argv[2])
    elif len(sys.argv) == 2:
        print("search suffix file:\"{}\" in current directory".format(sys.argv[1]))
        delete_suffix(suffix=sys.argv[1])
    else:
        print("Please use as the way: delete_suffix.py +suffix +delete_dirs, such as delete_suffix.py .gg ./")

main()
