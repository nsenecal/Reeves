# Reeves

Written in python 3.8.
Goal: Censor questionable language in Youtube videos.

#Version

Beta 0.2.1

#Changelog

-Added media bar to control playback
-Added fullscreen/windowed button
-Fixed issue where censoring function didn't recognize a change
-Added file loading based on video URL from local directory  
-Removed filetest.py as it is unnecessary
-Deleted Test.txt as it is unnecessary
-Merged stomping_ground to master and removed the stomping_ground branch

#Current Dependencies:
-pafy
-python-vlc (Currently using vlc.py)
-pyautogui

#Status

Currently being developed.

#Compilation for OS'

N/A as of this point

#Testing

-Download and extract source files to local directory
-Install python 3.8
-pip install the following: pafy and pyautogui
-run Reeves.py from the command line
-Load this video: https://www.youtube.com/watch?v=f0j--Y6G4Fg and it will censor the first four "swears" in the video.

#Known issues

-Volume sometimes drops off after using the media bar
