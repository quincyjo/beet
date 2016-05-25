'''
video_provider_ftp.py
=====================
Video provider for managing fetching the newest video from the beemon server
through frp protocol. Relies on the ftp service.
'''

import os
import re
import ftplib
import ntpath

from beet.video_provider import VideoProvider

__author__ = "gurnben"


class FtpVideoProvider(VideoProvider):

    def __init__(self, args):
        self.args = args
        self.file = open(args.auth[0], 'r')
        self.ftp = ftplib.FTP(self.file.readline()[:-1])
        self.ftp.login(self.file.readline()[:-1], self.file.readline()[:-1])
        self.ftp.cwd(self.file.readline()[:-1])
        self.file.close()


    def get_video_source_direct(self, direct):
        if direct.endswith(".h264"):
            with open("beet/temp/" + ntpath.basename(direct), 'wb') as r:
                self.ftp.retrbinary("RETR " + self.ftp.pwd() + direct, r.write)
                return [r.name]
        else:
            answer = []
            #download every file into the temp folder and close the ftp.
            self.ftp.cwd(self.ftp.pwd() + "/" + direct)
            for file in self.ftp.nlst():
                if file.endswith(".h264"):
                    with open("beet/temp/" + file, 'wb') as r:
                        self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + file, r.write)
            self.ftp.close()
            #make a list of the created files and return it.
            for file in os.listdir("beet/temp/"):
                if file.endswith(".h264"):
                    answer.append(os.path.join("beet/temp/", file))
            return answer


    def get_video_source(self):
        #If the hive is not specified:
        if self.args.hive[0] is None:
            print("Choose a Hive from those listed below.")
            for file in self.ftp.nlst():
                print(file)
            hive = input("Enter your choice:")
            while hive not in self.ftp.nlst():
                print("Choose a hive from those listed below.")
                for file in self.ftp.nlst():
                    print(file)
                hive = input("Enter your choice:")
            self.ftp.cwd(self.ftp.pwd() + "/" + hive)

        #If a hive is set directly navigate to the appropriate raspberry pi directory
        else:
            self.ftp.cwd(self.ftp.pwd() + "/rpi" + str(self.args.hive[0]))

        #initial date/folder input

        print("Choose from the following dates: ")
        for file in self.ftp.nlst():
            print(file)
        folder = input("Enter Your Choice: ")

        #input validation

        while folder not in self.ftp.nlst():
            print("Please enter a date from the list: ")
            for file in self.ftp.nlst():
                print(file)
            folder = input("Enter Your Choice: ")

        #Once they enter a valid folder navigate to it.

        self.ftp.cwd(self.ftp.pwd() + "/" + folder)

        #Prompt to analyze every file in the folder (defaults to no).
        directory = input("Analzye every file in the directory? (Y/N): ")

        #If they want to run it on the entire directory do this:
        if directory.lower() == "y" or directory.lower() == "yes":
            answer = []
            #navigate to video folder
            self.ftp.cwd(self.ftp.pwd() + "/video/")
            #download every file into the temp folder and close the ftp.
            for file in self.ftp.nlst():
                if file.endswith(".h264"):
                    with open("beet/temp/" + folder + " - " + file, 'wb') as r:
                        self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + file, r.write)
            self.ftp.close()
            #make a list of the created files and return it.
            for file in os.listdir("beet/temp/"):
                answer.append(os.path.join("beet/temp/", file))
            return answer

        #If they do not want to analyze all files:
        else:
            # Go into video directory
            self.ftp.cwd(self.ftp.pwd() + "/video/")
            #Initial file choice:
            print("Choose from the following files: ")
            for file in self.ftp.nlst():
                print(file)
            fil = input("Enter Your Choice: ")
            #input validation:
            while fil not in self.ftp.nlst():
                print("Please enter one of the following files: ")
                for file in self.ftp.nlst():
                    print(file)
                fil = input("Enter Your Choice: ")
            # With a valid file, save it to the temp folder and return the location.
            with open("beet/temp/" + folder + " - " + fil, 'wb') as r:
                self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + fil, r.write)
                self.ftp.close()
                return [r.name]


    def end(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
