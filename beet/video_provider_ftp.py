'''
video_provider_ftp.py
=====================
Video provider for managing fetching the newest video from the beemon server
through frp protocol. Relies on the ftp service.
'''

import os
import re

from beet.video_provider import VideoProvider
from beet.ftp_service import FtpService

__author__ = "verbetam"


class FtpVideoProvider(VideoProvider):

    def __init__(self, auth):
        self._ftp_service = FtpService(auth)
        self.dirs = []
        self.files = []

    def get_video_source(self):
        self._ftp_service.connect()
        newestFile = self._get_newest_video()
        with open('tempfile.h264', 'wb') as tempfile:
            ret = self._ftp_service._ftp.retrbinary(
                "RETR " + newestFile, tempfile.write)
            print(ret)
            tempfile.close()
        self._ftp_service.disconnect()
        return 'tempfile.h264'

    def _get_newest_video(self):
        self._ftp_service._ftp.cwd('/usr/local/bee/beemon/pit1')
        ret = self._ftp_service._ftp.retrlines('LIST', self._splitDirLine)
        self._sortDirsByDate()
        dirIndex = 0
        newestFile = None
        while newestFile is None:
            newestDir = self.dirs[dirIndex]
            self._ftp_service._ftp.cwd("{0}/video".format(newestDir))
            # get most recent video file
            ret = self._ftp_service._ftp.retrlines('LIST', self._splitFileLine)
            if len(self.files) > 0:
                self._sortFilesByTime()
                newestFile = self.files[0]
            else:
                dirIndex += 1
                self._ftp_service._ftp.cwd("../..")
        return newestFile

    def _splitDirLine(self, string):
        directoryName = string.split()[-1]
        if re.match("^\d{2}-\d{2}-\d{4}$", directoryName):
            self.dirs.append(directoryName)

    def _sortDirsByDate(self):
        # Sort by day
        self.dirs.sort(key=lambda dirName: dirName.split('-')[0], reverse=True)
        # Sort by month
        self.dirs.sort(key=lambda dirName: dirName.split('-')[1], reverse=True)
        # Sort by year
        self.dirs.sort(key=lambda dirName: dirName.split('-')[2], reverse=True)

    def _splitFileLine(self, string):
        fileName = string.split()[-1]
        if re.match("^\d{2}-\d{2}-\d{4}_\d{2}:\d{2}:\d{2}.h264$", fileName):
            self.files.append(fileName)

    def _sortFilesByTime(self):
        # Sort by second
        self.files.sort(key=lambda fileName:
                        fileName.split('_')[1].split(':')[2],
                        reverse=True)
        # Sort by minute
        self.files.sort(key=lambda fileName:
                        fileName.split('_')[1].split(':')[1],
                        reverse=True)
        # Sort by hour
        self.files.sort(key=lambda fileName:
                        fileName.split('_')[1].split(':')[0],
                        reverse=True)
