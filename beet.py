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

__author__ = "verbetam and gurnben"


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
        type=argparse.FileType('a'),
        help="Specifies where where to log output to",
        dest="log",
        default='beet.log')
    parser.add_argument(
        '-al', '--altlog',
        type=argparse.FileType('a'),
        help="Specifies where where to log output to",
        dest="altlog",
        default='beet.log')
    parser.add_argument(
        '-r', '--remote',
        help="Access source files through FTP",
        action="store_true",
        dest="remote",
        default=False)
    parser.add_argument(
        '-f', '--ftp',
        dest="ftp",
        help="Specify a filepath for the ftp connection.",
        type=str,
        nargs=1,
        default=None)
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
    borders = parser.add_mutually_exclusive_group()
    borders.add_argument(
        '-B', '--Bounds',
        help="Change Boundary Location.  Format: [X][Y][HEIGHT][WIDTH]",
        type=int,
        nargs=4,
        dest="coordinates",
        default=(200, 200, 100, 200))
    borders.add_argument(
        '-H', '--Hive',
        choices=(21, 22),
        help="Preset Hives",
        type=int,
        nargs=1,
        dest="hive",
        default=[None])
    parser.add_argument(
        '-a', '--auth',
        help="Access source files via FTP with info in given file",
        type=str,
        dest="auth",
        nargs='?',
        default=["beet/auth.txt"])
    args = parser.parse_args()
    return args

def main():
    # Wipe the contents of the temp folder first!
    for file in os.listdir("beet/temp/"):
        os.remove("beet/temp/" + file)
    # Now on to the utility...
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
        if os.path.exists(filepath) and filepath.endswith(".h264"):
            if args.hive[0] is None:
                roi = args.coordinates
            elif args.hive[0] is 21:
                roi = (235, 340, 100, 200)
            elif args.hive[0] is 22:
                roi = (200, 360, 115, 325)
            else:
                print("Invalid Border Setup")
                exit()
            app = beet.kalman_track.App(invisible=not args.visible,
                                        draw_contours=args.contours,
                                        draw_tracks=args.tracks,
                                        draw_boundary=args.boundary,
                                        draw_mask=args.mask,
                                        set_boundaries=tuple(roi))
            # Open the current file.
            app.openNewVideo(filepath)
            # Run the app.
            app.run()

            # If verbose, print results.
            if(args.verbose):
                line = "File: {0}\n  Arrivals: {1}\n  Departures: {2}\n"
                print(line.format(filepath, app.arrivals,
                                  app.departures))

            # If logging, log results.
            if(args.log):
                line = "File: {0}\nHive: {1}\n  Arrivals: {2}\n  Departures: {3}\n"
                if args.hive[0] is not None:
                    args.log.write(line.format(filepath, args.hive[0],
                                      app.arrivals, app.departures))
                else:
                    args.log.write(line.format(filepath, "Not Specified",
                                      app.arrivals, app.departures))
            if (args.altlog):
                line = "File: {0}\t {1:2d}\t {2}\n"
                args.altlog.write(line.format(filepath,
                                              app.arrivals + app.departures,
                                              os.path.getsize(filepath)))
            if args.remote:
                video_policy.end(filepath)

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
