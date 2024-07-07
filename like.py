import re

# Define the patterns to search for
patterns = [
    r"SecBluetoothBroadcastSource: startBroadcast By user action",
    r"BluetoothLeBroadcast: startBroadcasting",
    r"bt stack: \[INFO:broadcaster\.cc \(652\)\] CreateAudioBroadcast CreateAudioBroadcast",
    r"LeAudioService: startBroadcast",
    r"bt_stack: \[INFO:state_machine\.cc\(423\)\] CreateBig broadcast_id=\d+",
    r"bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine\.cc:603 HandleciEvent: BIG create BIG complete, big_id=1",
    r"bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine\.c:533 TriggerIsoDatapathSetup: conn_hdl=\d+",
    r"bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine\.cc:533 TriggerIsoDatapathSetup: conn_hdl=\d+",
    r"bt_stack: \[INFO:broadcaster\.cc \(1118\)\] OnStateMachineEvent broadcast id\d+ state=STREAMING"
]

# Regular expression to match timestamped lines with various log levels
timestamped_line_regex = re.compile(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \d+ \d+ \d+ [IDE] .*")

# Function to search for patterns in the file
def search_patterns(filename, patterns):
    try:
        regexes = [re.compile(pattern) for pattern in patterns]
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                if not timestamped_line_regex.match(line):
                    continue  # Skip lines that do not match timestamped line format
                
                for regex in regexes:
                    if regex.search(line):
                        print(line.strip())
                        break
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except IOError:
        print(f"An error occurred while reading the file {filename}.")

# Example usage
search_patterns('sample.txt', patterns)
