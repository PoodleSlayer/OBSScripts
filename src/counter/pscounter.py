import obspython as obs
import os

### This script allows you to increment and decrement a counter to display on your stream overlay via hotkeys!

# version 0.0.1
# by PoodleSlayer with <3

counter_filepath = ""
counter_filename = ""
file_created = False
file_not_found_msg = "Please specify a folder for the count file c:"
counter_increment_hotkey = "counter_increment_hotkey"
counter_decrement_hotkey = "counter_decrement_hotkey"
file_path_setting = "file_path"

# script description displayed in the Scripts dialog window of OBS
def script_description():
    script_info = "PSCounter\n\n"
    script_info += "This script allows you to update a counter you can use on your stream overlay. "
    script_info += "The count is stored in a user-specified location."
    script_info += "by PoodleSlayer\n"
    script_info += "v0.0.1"
    return script_info

# id of the hotkeys set by OBS
increment_hotkey_id = obs.OBS_INVALID_HOTKEY_ID
decrement_hotkey_id = obs.OBS_INVALID_HOTKEY_ID

# this is called when the script is loaded
def script_load(settings):
    # create hotkey settings in OBS
    global increment_hotkey_id, decrement_hotkey_id, counter_filepath

    # increment hotkey
    increment_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PSCounter Up", on_increment_hotkey)
    increment_hotkey_save_array = obs.obs_data_get_array(settings, counter_increment_hotkey)
    obs.obs_hotkey_load(increment_hotkey_id, increment_hotkey_save_array)
    obs.obs_data_array_release(increment_hotkey_save_array)

    # decrement hotkey
    decrement_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PSCounter Down", on_decrement_hotkey)
    decrement_hotkey_save_array = obs.obs_data_get_array(settings, counter_decrement_hotkey)
    obs.obs_hotkey_load(decrement_hotkey_id, decrement_hotkey_save_array)
    obs.obs_data_array_release(decrement_hotkey_save_array)

    # create counter file if it doesn't exist
    counter_filepath = obs.obs_data_get_string(settings, file_path_setting)
    create_count_file()
    print("*** PSCounter loaded! ***")

# this is called before data settings are saved
def script_save(settings):
    # save the hotkey info
    # increment hotkey
    increment_hotkey_save_array = obs.obs_hotkey_save(increment_hotkey_id)
    obs.obs_data_set_array(settings, counter_increment_hotkey, increment_hotkey_save_array)
    obs.obs_data_array_release(increment_hotkey_save_array)

    # decrement hotkey
    decrement_hotkey_save_array = obs.obs_hotkey_save(decrement_hotkey_id)
    obs.obs_data_set_array(settings, counter_decrement_hotkey, decrement_hotkey_save_array)
    obs.obs_data_array_release(decrement_hotkey_save_array)

# sets the default value of the various properties
def script_defaults(settings):
    obs.obs_data_set_default_string(settings, file_path_setting, "")

# displays the properties in the Script UI
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, file_path_setting, "File Path", obs.OBS_PATH_DIRECTORY, "", None)
    return props

# called when OBS Script Settings are updated via the GUI
def script_update(settings):
    global counter_filepath
    counter_filepath = obs.obs_data_get_string(settings, file_path_setting)
    if counter_filepath != None and counter_filepath != "":
        create_count_file()
        print(f"PSCounter will write to a file in: {counter_filepath}")

# creates the counter file if one doesn't exist
def create_count_file():
    global counter_filepath, counter_filename, file_created
    if counter_filepath != None and counter_filepath != "":
        try:
            counter_filename = os.path.join(counter_filepath, "count.txt")
            # the get_path function from OBS uses Unix-style forward slashes, so replace for Windows
            counter_filename = counter_filename.replace('/', '\\')
            if not os.path.exists(counter_filename):
                with open(counter_filename, 'w+') as counter_file:
                    counter_file.write(str(0))
                    print(f"file was created at {counter_filename}")
            file_created = True
        except:
            print("some kinda I/O exception occurred")
    else:
        print(file_not_found_msg)

# callback for the increment hotkey to increase the count
def on_increment_hotkey(pressed):
    global counter_filename
    if pressed:
        if file_created is False:
            print(file_not_found_msg)
            return
        with open(counter_filename, 'r+') as counter_file:
            current_count = int(counter_file.read())
            counter_file.seek(0)
            counter_file.write(str(current_count + 1))
            counter_file.truncate()

# callback for the decrement hotkey to decrease the count
def on_decrement_hotkey(pressed):
    global counter_filename
    if pressed:
        if file_created is False:
            print(file_not_found_msg)
            return
        with open(counter_filename, 'r+') as counter_file:
            current_count = int(counter_file.read())
            if current_count > 0:
                counter_file.seek(0)
                counter_file.write(str(current_count - 1))
                counter_file.truncate()

# event for script unload. might not need this but just in case
def script_unload():
  print("*** script was unloaded ***")

print("Thanks for using PoodleSlayer's Counter script!")
