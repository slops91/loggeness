import re
import os
from datetime import datetime

# Define the sequence of lines to search for
sequence_of_lines = [
    r"SecBluetoothBroadcastSource: startBroadcast By user action",
    r"BluetoothLeBroadcast: startBroadcasting",
    r"bt stack: \[INFO:broadcaster.c\(652\)\] CreateAudioBroadcast CreateAudio Broadcast",
    r"bt stack: \[INFO:broadcaster.cc\(1118\)\] OnStateMachineEvent broadcast id\d+ state=CONFIGURED",
    r"LeAudioService: startBroadcast",
    r"bt_stack: \[INFO:state_machine.cc\(423\)\] CreateBig broadcast_id= \d+",
    r"bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.c:603 HandleHciEvent. BIG create BIG complete, big_ id=1",
    r"bluetooth: packages/modules/Bluetooth/system/ba/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=\d+",
    r"bluetooth: packages/modules/Bluetoöth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerlsoDatapathSetup: conn_hdl=\d+",
    r"bt stack: \[INFO:broadcaster.cc\(1118\)\] OnStateMachineEvent broadcast id\d+ state=STREAMING"
]

# Regular expression to match timestamped lines with various log levels
timestamped_line_regex = r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \d+ \d+ \d+ [IDE] .*"

# Function to search for the sequence in the file
def search_sequence_in_file(filename, patterns):
    try:
        regexes = [re.compile(pattern) for pattern in patterns]
        timestamped_line_regex_compiled = re.compile(timestamped_line_regex)
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            current_pattern_index = 0
            line_number = 0
            in_timestamped_block = False  # Flag to indicate if currently in a block of timestamped lines
            results = [None] * len(patterns)
            errors = []

            for line in file:
                line_number += 1
                
                # Check if line matches timestamped line format
                if timestamped_line_regex_compiled.match(line):
                    in_timestamped_block = True
                    continue  # Skip this line and go to the next one
                
                # If in timestamped block, check if line matches current pattern in the sequence
                if in_timestamped_block:
                    if regexes[current_pattern_index].search(line):
                        results[current_pattern_index] = (line_number, line.strip())
                        current_pattern_index += 1
                        if current_pattern_index == len(patterns):
                            print("Sequence found in the file.")
                            for i, result in enumerate(results):
                                if result:
                                    print(f"Pattern {i + 1} found at line {result[0]}: {result[1]}")
                            return True
                    elif current_pattern_index > 0 and not regexes[current_pattern_index-1].search(line):
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        errors.append((timestamp, f"Error between patterns {current_pattern_index} and {current_pattern_index + 1} at line {line_number}"))
                else:
                    # If not in timestamped block, continue to next line
                    continue
                
                # Reset flag when we no longer match a timestamped line
                in_timestamped_block = False
            
            if errors:
                print("Errors detected:")
                for error in errors:
                    print(f"{error[0]} - {error[1]}")
            
            print("Sequence not found in the file.")
            return False
        
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except IOError:
        print(f"An error occurred while reading the file {filename}.")

# Example usage
search_sequence_in_file('sample.txt', sequence_of_lines)
