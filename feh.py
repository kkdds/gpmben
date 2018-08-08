import pexpect
import re

from threading import Thread
from time import sleep

class FEH(object):

    _LAUNCH_CMD = '/usr/bin/feh -FD 2 %s'
    _QUIT_CMD = 'q'

    def __init__(self, imgdir):
        cmd = self._LAUNCH_CMD % (imgdir)
        #print(cmd)
        self._process = pexpect.spawn(cmd)

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)


from os import system
class TURN_OFF(object):
    def __init__(self):
        #return
        #print('turn off')
        system('sudo halt')

class RESTART(object):
    def __init__(self):
        system('sudo reboot')

class KILL_PY(object):
    def __init__(self):
        system('sudo killall -9 python3')
