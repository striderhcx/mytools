#!/usr/bin/python
#coding=utf-8
'''
这个类是自己随手写的装饰器，主要是想写一个类的和一个普通的函数装饰器
'''

import time
import functools

def log(*args, **kwargs):
    if len(kwargs) == 0:
        print(args)
    else:
        print(args,kwargs)


#类作为装饰器
class Timer():
    def __init__(self, func):
        #将被包装函数的元信息复制到可调用实例中去
        functools.wraps(func)(self)
        self._func = func

    def __call__(self, *args, **kwargs):
        before = time.time()
        result = self._func(*args, **kwargs)
        after = time.time()
        log("cost_time: ", after - before)
        return result

'''
因为返回的那个wrapper()函数名字就是'wrapper',
所以，需要把原始函数的__name__等属性复制到wrapper()函数中，
否则，有些依赖函数签名的代码执行就会出错.
不需要编写wrapper.__name__ = func.__name__这样的代码，
Python内置的functools.wraps就是干这个事的.
'''
def function_record(log_level):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log("{} {} before function:{}".format(log_level, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),func))
            func(*args, **kwargs)
            log("{} {} after function:{}".format(log_level, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))),func))
        return wrapper
    return decorator
@Timer
@function_record('Warn')
def add(x, y=10):
    log(x+y)
    time.sleep(1)
    return x+y

def test():
    add(23,10)
    #测试不用functools.wraps的情况下，返回的__name__
    #log("wrapper:{}".format(add.__name__))
test()

