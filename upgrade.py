#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
import requests,asyncio
import jinja2,aiohttp_jinja2
import urllib.request
from aiohttp import web
import zipfile

from os import system
system('sudo ifdown wlan0')
import pexpect
import re
from threading import Thread
from time import sleep

class WAM_AP(object):
    def _get_end(self):
        while True:
            sleep(5)
    def __init__(self):
        self._process = pexpect.spawn('sudo create_ap --no-virt -n -g 192.168.11.22 wlan0 zmj001 66341703')
        self._end_thread = Thread(target=self._get_end)
        self._end_thread.start()
WAM_AP()


@asyncio.coroutine
def sys_update(request):
    global softPath
    hhdd=[('Access-Control-Allow-Origin','*')]
    posted = yield from request.post()
    #print(posted)
    tbody= '成功'
    if posted['tp']=='core':
        try:
            upedfile=posted['cfile']
            ufilename = upedfile.filename
            ufilecont = upedfile.file
            content = ufilecont.read()
            with open('/home/pi/gpmb/gpmb.zip', 'wb') as f:
                f.write(content)

            #解压缩
            try:
                fz = zipfile.ZipFile('/home/pi/gpmb/gpmb.zip','r')
                for file in fz.namelist():
                    fz.extract(file,'/home/pi/gpmb/')
                fz.close()
            except:
                tbody='解压失败'
        except:
            tbody='失败'
    return web.Response(headers=hhdd ,body=tbody.encode('utf-8'),content_type='application/json')


@aiohttp_jinja2.template('upgrade.html')
def upgrade(request):
    #使用aiohttp_jinja2  methed 2
    return {'html': 'upgrade',"ver":"20161111"}


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    #使用aiohttp_jinja2
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('/home/pi/gpmb'))
    app.router.add_route('*', '/sys_update', sys_update)
    app.router.add_route('*', '/', upgrade)
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 9002)
    print(' started at http://9002... ')
    return srv

loop = asyncio.get_event_loop()
tasks = [init(loop)]#loop_info持续发送状态
loop.run_until_complete(asyncio.wait(tasks))
loop.run_forever()