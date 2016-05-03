# Beet

Tracks beens moving in and out from the hive, keeping track of arrivals and departures.

### Running
#### FTP
Live mode is designed to access a serve by ftp. Create a file named 'auth' in the source directory structured as:
```
<user>
<pwd>
<server>
```
The live_mode.py script will use this information to retrieve files for tracking.

#### Live Mode
With Anaconda3:
```bash
// Install opencv3
$ conda install -c https://conda.anaconda.org/menpo opencv3
// May be needed base on windows manager
$ conda install asmeurer pango
$ cd source
$ python live_mode.py
```
The script will currently run in Anaconda2, but will not support it in the future.
