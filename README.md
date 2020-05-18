# Reeves

A flexible Youtube video player.

Written in python 3.8.

Goal: Censor questionable language in Youtube videos.

# Version

Beta 0.7.1

# Testing/Running
YOU MUST HAVE VLC x64 IN YOUR SYSTEM'S PATH FOR THE SCRIPT TO RUN.

-Download and extract source files to local directory

-Install python 3.8

-run Reeves.py

-Load this video: https://www.youtube.com/watch?v=f0j--Y6G4Fg and it will censor the first four "swears" in the video. (Provided you tell it to check Github)

# How to Use

Move your mouse around the screen until the control window shows up. You can toggle it by pressing alt.

Copy/Paste links into the search field for specific videos. Enter search terms and press play to search Youtube. It will enter the top result in the que. Double click on items in the que to remove them. Use the Censor button to enable/disable censoring (only applicable to videos with "censcripts").

# Current Dependencies:

**None of these need to be installed for the official release. They are already contained in the source files. If you are testing from the source code then all you need to install is VLC x64**

-bs4

-pafy

-python-vlc

-pyautogui

-youtube-dl

-requests

-pynput

-soupsieve

-six

-From vlc: libvlc.dll, libvlccore.dll the "plugins" folder

# Status

Hiatus to determine next steps.

# Compilation for OS'

Windows: Wrapped using pyinstaller

# Potential features

Playlist saving/exports/imports

Built in Censcript creator

# Known issues

-Volume sometimes drops off after using the media bar

-Show/Hide is a bit finiky
