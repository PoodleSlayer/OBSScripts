import obspython as obs
import os

### This script allows you to increment and decrement two counters to display on your stream overlay via hotkeys!

# version 0.0.1
# by PoodleSlayer with <3

counter_filepath = ""
counter1_filename = ""
counter2_filename = ""
files_created = False
files_not_found_msg = "Please specify a folder for the count files!"
counter1_increment_hotkey = "counter1_increment_hotkey"
counter1_decrement_hotkey = "counter1_decrement_hotkey"
counter2_increment_hotkey = "counter2_increment_hotkey"
counter2_decrement_hotkey = "counter2_decrement_hotkey"
file_path_setting = "file_path"

# script description displayed in the Scripts dialog window of OBS
def script_description():
    script_info = "PS_MultiCounter\n\n"
    script_info += "This script allows you to update two counters you can use on your stream overlay. "
    script_info += "The counts are stored in a user-specified location.\n"
    script_info += "by PoodleSlayer\n"
    script_info += "v0.0.1"
    return script_info

# id of the hotkeys set by OBS
increment1_hotkey_id = obs.OBS_INVALID_HOTKEY_ID
decrement1_hotkey_id = obs.OBS_INVALID_HOTKEY_ID
increment2_hotkey_id = obs.OBS_INVALID_HOTKEY_ID
decrement2_hotkey_id = obs.OBS_INVALID_HOTKEY_ID

# this is called when the script is loaded
def script_load(settings):
    # create hotkey settings in OBS
    global increment1_hotkey_id, decrement1_hotkey_id, increment2_hotkey_id, decrement2_hotkey_id, counter_filepath

    # increment1 hotkey
    increment1_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PS_MultiCounter1 Up", on_increment1_hotkey)
    increment1_hotkey_save_array = obs.obs_data_get_array(settings, counter1_increment_hotkey)
    obs.obs_hotkey_load(increment1_hotkey_id, increment1_hotkey_save_array)
    obs.obs_data_array_release(increment1_hotkey_save_array)

    # decrement1 hotkey
    decrement1_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PS_MultiCounter1 Down", on_decrement1_hotkey)
    decrement1_hotkey_save_array = obs.obs_data_get_array(settings, counter1_decrement_hotkey)
    obs.obs_hotkey_load(decrement1_hotkey_id, decrement1_hotkey_save_array)
    obs.obs_data_array_release(decrement1_hotkey_save_array)

    # increment2 hotkey
    increment2_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PS_MultiCounter2 Up", on_increment2_hotkey)
    increment2_hotkey_save_array = obs.obs_data_get_array(settings, counter2_increment_hotkey)
    obs.obs_hotkey_load(increment2_hotkey_id, increment2_hotkey_save_array)
    obs.obs_data_array_release(increment2_hotkey_save_array)

    # decrement2 hotkey
    decrement2_hotkey_id = obs.obs_hotkey_register_frontend(script_path(), "PS_MultiCounter2 Down", on_decrement2_hotkey)
    decrement2_hotkey_save_array = obs.obs_data_get_array(settings, counter2_decrement_hotkey)
    obs.obs_hotkey_load(decrement2_hotkey_id, decrement2_hotkey_save_array)
    obs.obs_data_array_release(decrement2_hotkey_save_array)

    # create counter file if it doesn't exist
    counter_filepath = obs.obs_data_get_string(settings, file_path_setting)
    create_count_files()
    print("*** PS_MultiCounter loaded! ***")

# this is called before data settings are saved
def script_save(settings):
    # save the hotkey info

    # increment1 hotkey
    increment1_hotkey_save_array = obs.obs_hotkey_save(increment1_hotkey_id)
    obs.obs_data_set_array(settings, counter1_increment_hotkey, increment1_hotkey_save_array)
    obs.obs_data_array_release(increment1_hotkey_save_array)

    # decrement1 hotkey
    decrement1_hotkey_save_array = obs.obs_hotkey_save(decrement1_hotkey_id)
    obs.obs_data_set_array(settings, counter1_decrement_hotkey, decrement1_hotkey_save_array)
    obs.obs_data_array_release(decrement1_hotkey_save_array)

    # increment2 hotkey
    increment2_hotkey_save_array = obs.obs_hotkey_save(increment2_hotkey_id)
    obs.obs_data_set_array(settings, counter2_increment_hotkey, increment2_hotkey_save_array)
    obs.obs_data_array_release(increment2_hotkey_save_array)

    # decrement2 hotkey
    decrement2_hotkey_save_array = obs.obs_hotkey_save(decrement2_hotkey_id)
    obs.obs_data_set_array(settings, counter2_decrement_hotkey, decrement2_hotkey_save_array)
    obs.obs_data_array_release(decrement2_hotkey_save_array)

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
        create_count_files()
        print(f"PS_MultiCounter will write to files in: {counter_filepath}")

# creates the counter file if one doesn't exist
def create_count_files():
    global counter_filepath, counter1_filename, counter2_filename, files_created
    if counter_filepath != None and counter_filepath != "":
        try:
            counter1_filename = os.path.join(counter_filepath, "count1.txt")
            counter2_filename = os.path.join(counter_filepath, "count2.txt")
            # the get_path function from OBS uses Unix-style forward slashes, so replace for Windows
            counter1_filename = counter1_filename.replace('/', '\\')
            counter2_filename = counter2_filename.replace('/', '\\')
            
            if not os.path.exists(counter1_filename):
                with open(counter1_filename, 'w+') as counter1_file:
                    counter1_file.write(str(0))
                    print(f"file was created at {counter1_filename}")
            
            if not os.path.exists(counter2_filename):
                with open(counter2_filename, 'w+') as counter2_file:
                    counter2_file.write(str(0))
                    print(f"file was created at {counter2_filename}")
            files_created = True
            print(f"Files were created, files_created set to {files_created}")
        except:
            print("some kinda I/O exception occurred")
    else:
        print(files_not_found_msg)

# callback for the increment1 hotkey to increase the count
def on_increment1_hotkey(pressed):
    global counter1_filename
    if pressed:
        increment_file(counter1_filename)

# callback for the decrement1 hotkey to decrease the count
def on_decrement1_hotkey(pressed):
    global counter1_filename
    if pressed:
        decrement_file(counter1_filename)

# callback for the increment2 hotkey to increase the count
def on_increment2_hotkey(pressed):
    global counter2_filename
    if pressed:
        increment_file(counter2_filename)

# callback for the decrement2 hotkey to decrease the count
def on_decrement2_hotkey(pressed):
    global counter2_filename
    if pressed:
        decrement_file(counter2_filename)

def increment_file(filename):
    if files_created is False:
        print(files_not_found_msg)
        return
    with open(filename, 'r+') as counter_file:
        current_count = int(counter_file.read())
        counter_file.seek(0)
        counter_file.write(str(current_count + 1))
        counter_file.truncate()

def decrement_file(filename):
    if files_created is False:
        print(files_not_found_msg)
        return
    with open(filename, 'r+') as counter_file:
        current_count = int(counter_file.read())
        if current_count > 0:
            counter_file.seek(0)
            counter_file.write(str(current_count - 1))
            counter_file.truncate()

# event for script unload. might not need this but just in case
def script_unload():
  print("*** script was unloaded ***")

print("Thanks for using PoodleSlayer's MultiCounter script!")
