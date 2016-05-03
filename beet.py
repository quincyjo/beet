#!/usr/bin/python

'''
beet.py
=======
Cli utility for tracking bees in the beemon project.
'''

import argparse

import cv2

import beet.kalman_track
from beet.video_policy import VideoPolicy

__author__ = "verbetam"

inputfile = ""
verbose = False
mask = False
visible = False
remote = False
auth = False
tracks = False
contours = False
boundary = False


def parse_args(parser):
    global inputfile, verbose, mask, visible, remote, auth, tracks,\
            boundary, contours

    parser.add_argument(
        '-i', '--input',
        help="Input file path",
        dest="input",
        required=True)
    parser.add_argument(
        '-V', '--verbose',
        help="Produce verbose output",
        action="store_true",
        dest="verbose",
        default=False)
    parser.add_argument(
        '-m', '--mask',
        help="Show masked video",
        action="store_true",
        dest="mask",
        default=False)
    parser.add_argument(
        '-v', '--visible',
        help="Show source video",
        action="store_true",
        dest="visible",
        default=False)
    parser.add_argument(
        '-r', '--remote',
        help="Access source files through FTP",
        action="store_true",
        dest="remote",
        default=False)
    parser.add_argument(
        '-t', '--tracks',
        help="Draw tracks",
        action="store_true",
        dest="tracks",
        default=False)
    parser.add_argument(
        '-c', '--contours',
        help="Draw contours",
        action="store_true",
        dest="contours",
        default=False)
    parser.add_argument(
        '-b', '--boundary',
        help="Draw boundary",
        action="store_true",
        dest="boundary",
        default=False)
    parser.add_argument(
        '-a', '--auth',
        help="Access source files via FTP with info in given file",
        default=False)
    args = parser.parse_args()

    inputfile = args.input
    verbose = args.verbose
    mask = args.mask
    visible = args.visible
    remote = args.remote
    auth = args.auth
    tracks = args.tracks
    contours = args.contours
    boundary = args.boundary
    return args


def main():
    parser = argparse.ArgumentParser(description='Bee tracker utility')
    args = parse_args(parser)
    video_policy = VideoPolicy(args)
    source = video_policy.get_video()

    app = beet.kalman_track.App(invisible=visible,
                                draw_contours=contours,
                                draw_tracks=tracks,
                                draw_boundary=boundary)
    app.openNewVideo(source)
    app.run()

    if(verbose):
        print("Arrivals: {0} Departures: {1}".format(app.arrivals,
                                                     app.departures))
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
