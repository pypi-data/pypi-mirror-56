#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-08-15 10:20
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import values
import threading
import do
from iapp import App
import time

model_map = {}

import schedule
import time

import asyncio

d = {}

# async def task():
#     global d
#     while 1:
#         await asyncio.sleep(3)
#         d['t'] = time.ctime()
#         print(d)


from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job('interval', seconds=3)
async def task_plus():
    d['t'] = time.ctime()
    print(d)
scheduler.start()


def tick():
    print('Tick! The time is: %s' % datetime.now())


scheduler = AsyncIOScheduler()
scheduler.add_job(tick, 'interval', seconds=3)
scheduler.start()

def update(**kwargs):
    time.sleep(10)

    model_map.update(kwargs)

    return model_map


f1 = lambda **kwargs: model_map
f2 = lambda **kwargs: d


def api(**kwargs):
    print(kwargs)
    print(kwargs.get('method')[0])
    a = eval(kwargs.get('method')[0])(**kwargs)
    return a


##############

app = App()

# app.app.add_task(task_plus)  #
# update
app.add_route("/update", update, time=time.ctime())

app.add_route("/f1", f1, time=time.ctime())

app.add_route("/f2", f2, time=time.ctime())

app.add_route("/api", api, time=time.ctime())

app.run(workers=1, access_log=True, port=9955)
