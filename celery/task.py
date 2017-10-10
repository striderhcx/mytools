#coding=utf-8
from celery import Celery
import time

app = Celery('tasks', broker='redis://localhost//0', backend='redis://localhost//0')

@app.task()
def add(x ,y):
    time.sleep(2)
    return int(x+y)
