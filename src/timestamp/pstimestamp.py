import obspython as obs
import os
import time
import math
from datetime import datetime

### This script allows you to create timestamps during your streams/recordings to (hopefully) easily find the interesting
### parts later on from your VOD/recording!

# version 0.0.1

timestamp_filepath = ""
timestamp_filename = ""
previous_timestamp = 0
start_timestamp = 0
keeptime = False

# script description displayed in the Scripts dialog window of OBS
def script_description():
    script_info = "PSTimestamp Helper\n\n"
    script_info += "This script allows you to create timestamps via a hotkey. "
    script_info += "The timestamp files will be placed into a user-specified folder so you can organize them "
    script_info += "per-stream, and the times are shown in the format hours:minutes:seconds except for the "
    script_info += "start and local times which are just your local time.\n\n"
    script_info += "by PoodleSlayer\n"
    script_info += "v0.0.1"
    return script_info

# id of the hotkey set by OBS
hotkey_id = obs.OBS_INVALID_HOTKEY_ID

# this is called when the script is loaded
def script_load(settings):
    global keeptime
    
    # grab the hotkey info from OBS
    global hotkey_id
    hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PSTimestamp", on_timestamp_hotkey)
    hotkey_save_array = obs.obs_data_get_array(settings, "timestamp_hotkey")
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    
    # register events callback
    obs.obs_frontend_add_event_callback(on_event)
    keeptime = False
    #print("*** script was loaded ***")

# this is called before data settings are saved
def script_save(settings):
    # save the hotkey info
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "timestamp_hotkey", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)
    #print("script was SAVED")

# sets the default value of the various properties
def script_defaults(settings):
    #obs.obs_data_set_default_string(settings, "file_name", "timestamps.txt")
    obs.obs_data_set_default_string(settings, "file_path", "")

# displays the properties in the Script UI
def script_properties():
    props = obs.obs_properties_create()

    #obs.obs_properties_add_text(props, "file_name", "File Name", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_path(props, "file_path", "File Path", obs.OBS_PATH_DIRECTORY, "", None)

    return props

# called when OBS Script Settings are updated via the GUI
def script_update(settings):
    global timestamp_filepath
    timestamp_filepath = obs.obs_data_get_string(settings, "file_path")
    #timestamp_filename = obs.obs_data_get_string(settings, "file_name")
    #print(f"Timestamp file is named: {timestamp_filename}")
    print(f"PSTimestamp files will be saved in: {timestamp_filepath}")

# event handler for events from OBS
def on_event(event):
    #print("something happened: " + event)
    global keeptime
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        #print("started streaming!")
        keeptime = True
        create_timestamp_file()
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        #print("X stopped streaming")
        keeptime = False
        close_timestamp_file()
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        #print("started recording!")
        keeptime = True
        create_timestamp_file()
    if event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        #print("X stopped recording")
        keeptime = False
        close_timestamp_file()

# called when the user starts streaming/recording, creates the timestamp file 
def create_timestamp_file():
    global timestamp_filepath, timestamp_filename, previous_timestamp, start_timestamp
    if timestamp_filepath != None and timestamp_filepath != "":
        try:
            timestamp_filename = os.path.join(timestamp_filepath, datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt")
            # the get_path function from OBS uses Unix-style forward slashes, so replace for Windows
            timestamp_filename = timestamp_filename.replace('/', '\\')
            print(f"file will be created as {timestamp_filename}")
            # write the start time to the file
            current_time = time.time()
            start_timestamp = current_time
            previous_timestamp = current_time
            write_timestamp_to_file(f"stream START - {datetime.now().strftime('%X')} local time\n")
        except:
            print("ruh roh raggy")
    else:
        print("Please specify a folder for writing timestamp files c:")

def write_timestamp_to_file(timestamp):
    global timestamp_filename
    with open(timestamp_filename, 'a+') as timestamp_file:
        timestamp_file.write(timestamp)

# this is what is called when the hotkey is pressed to mark the current timestamp
def add_new_timestamp():
    global previous_timestamp
    # write the current time into the stream, time since last timestamp,
    # and time in current user's time
    timestamp_string = f"{time_since_start()} since stream start, {time_since_previous()} since last timestamp. ({datetime.now().strftime('%X')} local time)\n"
    write_timestamp_to_file(timestamp_string)
    previous_timestamp = time.time()

# this function is called when stream/recording ends
def close_timestamp_file():
    global previous_timestamp
    timestamp_string = time_since_start() + " - stream END\n"
    write_timestamp_to_file(timestamp_string)

# get the time since the last timestamp
def time_since_previous():
    global previous_timestamp
    time_since = time.time() - previous_timestamp
    return time_to_text(time_since)

# get the time since stream started. could probably combine with the above
# but for now it's not too bad
def time_since_start():
    global start_timestamp
    time_since = time.time() - start_timestamp
    return time_to_text(time_since)

# helper function to conver amounts of time to human-readable format
# such as 1:23:45 (hours:minutes:seconds)
def time_to_text(time_amount):
    time_since = time_amount
    hours = math.floor(time_since/3600)
    time_since = time_since % 3600
    minutes = math.floor(time_since/60)
    time_since = time_since % 60
    seconds = time_since
    timeString = ""
    if hours != 0:
        timeString += str(int(hours)) + ":"
    if minutes != 0:
        timeString += str(int(minutes)).zfill(2) + ":"
    if seconds != 0:
        timeString += str(int(seconds)).zfill(2)
    return timeString

# callback for the user-specified hotkey to write timestamps
def on_timestamp_hotkey(pressed):
    global keeptime
    if pressed and keeptime == True:
        # write current timestamp to file
        #print("**** HOTKEY WAS PRESSED ****")
        print(f"PSTimestamp hotkey at {datetime.now().strftime('%X')} local time")
        add_new_timestamp()

# event for script unload. might not need this but just in case
def script_unload():
  global keeptime
  keeptime = False
  print("*** script was unloaded ***")

print("Thanks for using PoodleSlayer's Timestamp script!")
