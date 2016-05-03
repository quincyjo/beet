'''
video_provider.py
=================
Abstract class for video providers. Also provides the base behaviour of simply
returning the path to the target file.
'''

import abc

__author__ = "verbetam"


class VideoProvider:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path=""):
        self._path = path

    @abc.abstractmethod
    def get_video_source(self):
        return self._path
