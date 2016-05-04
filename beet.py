#!/usr/bin/python

'''
beet.py
=======
Cli utility for tracking bees in the beemon project.
'''

import argparse
import os

import cv2

import beet.kalman_track
from beet.video_policy import VideoPolicy

__author__ = "verbetam"


def parse_args(parser):
    parser.add_argument(
        'files',
        metavar='FILE',
        nargs='*')
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
        '-l', '--log',
        type=argparse.FileType('w'),
        help="Specifies where where to log output to",
        dest="log",
        default='beet.log'
    )
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
    return args


def main():
    parser = argparse.ArgumentParser(description='Bee tracker utility')
    args = parse_args(parser)
    if (args.files is None and not args.remote):
        print("\nPlease provide an input file(s) or specifiy remote (-r)\n")
        return
    video_policy = VideoPolicy(args)
    source = video_policy.get_video()

    # Process each file given.
    for filepath in source:
        # If the file is valid.
        if os.path.exists(filepath):
            # Create a new app with given options.
            app = beet.kalman_track.App(invisible=not args.visible,
                                        draw_contours=args.contours,
                                        draw_tracks=args.tracks,
                                        draw_boundary=args.boundary,
                                        draw_mask=args.mask)
            # Open the current file.
            app.openNewVideo(filepath)
            # Run the app.
            app.run()

            # If verbose, print results.
            if(args.verbose):
                line = "File: {0}\n  Arrivales: {1}\n  Departures: {2}\n"
                print(line.format(filepath, app.arrivals,
                                  app.departures, app.departures))

            # If logging, log results.
            if(args.log):
                line = "File: {0}\n  Arrivales: {1}\n  Departures: {2}\n"
                args.log.write(line.format(filepath, app.arrivals,
                                           app.departures))

            cv2.destroyAllWindows()

        # If file is invalid.
        else:
            line = "Error: {0} is not a valid file path\n".format(filepath)
            # Print error.
            print(line)

            # If logging, log error.
            if(args.log):
                args.log.write(line)


if __name__ == "__main__":
    main()
