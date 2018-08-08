import pexpect
import re

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _LAUNCH_CMD = '/usr/bin/omxplayer --no-osd --blank --loop --orientation 90 --win 0,0,800,480 %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'
    _IMG_FILE = 'q'

    _VOF=1

    def __init__(self, mediafile):
        self.play(mediafile)

    def play(self, mediafile):
        cmd = self._LAUNCH_CMD % (mediafile)
        self._process = pexpect.spawn(cmd)
        self._end_thread = Thread(target=self._get_end)
        self._end_thread.start()

    def _get_end(self):
        while True:
            sleep(0.5)
            index = self._process.expect([pexpect.TIMEOUT,
                                            pexpect.EOF])
            if index == 1:
                print('video press stop EOF '+str(index))
                #self.stop()
                break
            else:
                print('video TIMEOUT '+str(index))
                #self.stop()
                #break
                continue
        self._VOF=0
        #self.stop()
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
        if index != 1:
            self.play('/home/pi/gpmb/video.mp4')

    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)
        #self._process = pexpect.spawn('feh -F '+self._IMG_FILE)

