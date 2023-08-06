#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : gunicorn
# @Time         : 2019-11-21 11:00
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
# https://www.jianshu.com/p/fecf15ad0c9a
import gevent.monkey

gevent.monkey.patch_all()

import multiprocessing

# debug = True
# loglevel = 'debug'
bind = '0.0.0.0:9000'
# logfile = 'log/debug.log'
# pidfile = "log/gunicorn.pid"
# accesslog = "log/access.log"
# errorlog = "log/debug.log"
daemon = True

# 启动的进程数
workers = 1  # multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'

if __name__ == '__main__':
    import os

    # os.system("gunicorn -w 1 -b 0.0.0.0:9000 flask_app:app -k gevent")
    os.system("gunicorn --threads 1 -c gun.py flask_app:app -k gevent")
