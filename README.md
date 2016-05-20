# Beet

Tracks beens moving in and out from the hive, keeping track of arrivals and departures.

### Running

```bash
$ python beet.py [tags...] [file/files/directories]
```

### Tags

  "-V" or "--verbose" : Produces Verbose Output
  
  "-m" or "--mask" : Show Masked Video
  
  "-v" or "--visible": Show Source Video
  
  "-l" or "--log" [filepath/file] : Specifies Where the Log Outputs.  Appends the log file or creates a new one if a file with that name is not found!

  "-al" or "--altlog" [filename] : Alternate logging option.  Creates a log listing the file name, total number of bees counted (arrivals + departures), and the file size.  Useful for file size analytics!  Appends the log file or creates a new one if a file with that name is not found!
  
  "-r" or "--remote" : Access Files Through FTP (WIP: NOT FUNCTIONING)
  
  "-t" or "--tracks" : Draw Tracks
  
  "-c" or "--contours" : Draw Contours
  
  "-b" or "--boundary" : Draw Entrance Boundary
  
  "-B" or "--Bounds" [X][Y][HEIGHT][WIDTH] : Allows you to change the boundaries for the entrance manually.  All parameters required.  (X, Y) are the coordinates of the from the top-left corner of the video to the top-left corner of the entrance bound.  (HEIGHT, WIDTH) are the height and width of the bounds.  Cannot be specified alongside "-H".  
  
  "-H" or "--Hive" [RPi #] : Provides preset boundaries for specific hives based off of Raspberry Pi Number.  Currently pre-configured for RPi 21 and 22. *more will be added in the future* Cannot be specified alongside "-B".  
  
  "-a" or "--auth" [filepath/file] : Access source files via FTP with info in given file.  (WIP: NOT FUNCTIONING)
  
### NOTES

  -If "-B" and "-H" are not specified, the default bounds are X=200, Y=200, HEIGHT=100, and WIDTH=200.  
  -Will run on all .h264 files in a directory if given a directory.  
  -Will run on any number of files/directories given!

#### FTP - WIP: Not Currently Functioning, Will Be Fixed in a Future Update!
beet is designed to access a serve by ftp. Create a file named 'auth' in the source directory structured as:

```
<user>
<pwd>
<server>
```

The beet.py script will use this information to retrieve files for tracking.

#### Beet
With Anaconda3:

```bash
// Install opencv3
$ conda install -c https://conda.anaconda.org/menpo opencv3
// May be needed base on windows manager
$ conda install asmeurer pango
$ cd source
$ python live beet.py [necessary tags] [file location]
```

The script will currently run in Anaconda2, but will not support it in the future.

### Future Work

  -Fix FTP
  -Add more preset hives
  -Integrate better logging (include RPi #, date, time, and arrivals and departures)
  -Automated operation and logging on an entire folder of video files
  
### Further Out
  
  -GUI to replace command line utility
  -GUI integration into the Beemon Utility

