# PSTimestamp  - PoodleSlayer's Timestamp Script

This script allows you to easily mark timestamps within your stream, but rather than marking them with a message in chat it writes the timestamp to a `.txt` file per-stream with convenient timings to help you track down when the exciting things happened in your VOD!

## Setup

### OBS Setup

**Important:** make sure that you have done the [necessary setup for OBS](../../README.md) in order to use scripts. This is just installing the correct Python version and pointing OBS at the location, so nothing too crazy!

### File Path
Import the script into OBS Studio's Scripts manager. Before first-time use you **must** specify a folder in which to save the timestamp files. Currently this is written with Windows-style file system paths but ideally in the future I'll test this on all platforms that OBS supports. 

![file path](imgs/pstimestamp_1.png)

### Hotkey
In your OBS hotkey settings (File -> Settings -> Hotkeys) look for the entry labeled `PSTimestamp`, probably near the bottom (I used a namespace to avoid the many other possible timestamp scripts that are out there). Specify the hotkey(s) of your liking and hit "Apply" and then "Ok". **Note:** any time you reload your scripts you will need to re-specify hotkeys. I'm not sure if there is a way around this but I noticed this during my testing.

## Using the Script

Timestamp files are created automatically when you start streaming or recording, and the files are named with a timestamp and placed in the file path you specified during initial setup. While you are streaming or recording simply hit whatever hotkey you assigned earlier and the script will write a line to the timestamp file including:
- time since the stream/recording started
- time since the previous timestamp
- your current local time

Hopefully between these three pieces of information you can easily track down what you're looking for!
