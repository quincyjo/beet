'''
video_provider.py
=================
Abstract class for video providers. Also provides the base behaviour of simply
returning the path to the target file.
'''

import abc
import os

__author__ = "verbetam"


class VideoProvider:
    __metaclass__ = abc.ABCMeta

    def __init__(self, path=""):
        self._path = path

    def get_video_source(self):
        answer = []
        for path in self._path:
            if path.endswith(".h264"):
                answer.append(path)
            else:
                for file in os.listdir(path):
                    answer.append(os.path.join(path, file))
        return answer
