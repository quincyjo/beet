'''
ftp_service.py
==============
Manages the FTP connection to the remote for data transfer with the info in
auth file. This file path is passed to this service on construction.
'''

import ftplib

__author__ = "verbetam"


class FtpService:

    def __init__(self, auth):
        self._get_ftp_info(auth)

    def connect(self):
        self._ftp = ftplib.FTP(self._server,
                               self._user,
                               self._pw)
        print("FtpService connected")

    def disconnect(self):
        self._ftp.quit()
        print("FtpService disconnected")

    def _get_ftp_info(self, auth):
        with open(auth, 'r') as auth:
            self._user = auth.readline().strip()
            self._pw = auth.readline().strip()
            self._server = auth.readline().strip()
            auth.close()
