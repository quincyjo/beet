'''
video_policy.py
===============
Determines which video provider to use to retrieve the source video from
based on the info given by the cli application.
'''

from beet.video_provider import VideoProvider
from beet.video_provider_ftp import FtpVideoProvider

__author__ = "verbetam"


class VideoPolicy:

    def __init__(self, args):
        self._args = args

    def get_video(self):
        return self._get_video_provider()

    def _get_video_provider(self):
        if self._args.remote and self._args.ftp is None:
            self._provider = FtpVideoProvider(self._args)
            return self._provider.get_video_source()
        elif self._args.remote and not (self._args.ftp is None):
            self._provider = FtpVideoProvider(self._args)
            return self._provider.get_video_source_direct(self._args.ftp[0])
        else:
            self._provider = VideoProvider(path=self._args.files)
            return self._provider.get_video_source()
    def end(self, filepath):
            FtpVideoProvider.end(self, filepath)

