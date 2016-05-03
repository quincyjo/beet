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
        self._get_video_provider()
        return self._provider.get_video_source()

    def _get_video_provider(self):
        if (self._args.remote):
            self._provider = FtpVideoProvider(self._args.auth)
        else:
            self._provider = VideoProvider(path=self._args.input)
