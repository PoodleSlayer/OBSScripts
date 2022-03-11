# PSCounter - PoodleSlayer's Counter Script

This script allows you to easily increment and decrement a counter value in a `.txt` file, useful for displaying a count on a stream overlay that you can control via hotkeys.

## Setup

### OBS Setup

**Important:** make sure that you have done the [necessary setup for OBS](../../README.md) in order to use scripts. This is just installing the correct Python version and pointing OBS at the location, so nothing too crazy!

### File Path
Import the script into OBS Studio's Scripts manager. Before first-time use you **must** specify a folder in which to save the counter file. Currently this is written with Windows-style file system paths but ideally in the future I'll test this on all platforms that OBS supports. 

![file path](../timestamp/imgs/pstimestamp_1.png)

### Hotkeys
In your OBS hotkey settings (File -> Settings -> Hotkeys) look for the entries labeled `PSCounter Up` and `PSCounter Down`, probably near the bottom (I used a namespace to avoid the many other possible counter scripts that are out there). Specify the hotkeys of your liking and hit "Apply" and then "Ok".

## Using the Script

The counter file is created when you first specify a file path after loading the script for convenience. The script will also attempt to create the file each time it is re-loaded in case the file is deleted but the folder is still specified. If things don't seem to be working, just check the script log - I tried to write some helpful messages!

Once the script has been set up, simply use the hotkeys you specified to increase or decrease the counter. I added a check to prevent the counter from ever going below 0, but I can change this in the future to be more flexible if people want that.
