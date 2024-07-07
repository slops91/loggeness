import threading
import re
import os
from queue import Queue

# Define the sequence of lines to search for
sequence_of_lines = [
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

# Regular expression to match timestamped lines
timestamped_line_regex = re.compile(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \d+ \d+ \d+ [IDE] .*")

# Function to search for the sequence in a chunk of the file
def search_sequence_chunk(filename, patterns, start, end, results_queue):
    try:
        regexes = [re.compile(pattern) for pattern in patterns]
        
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            file.seek(start)
            if start > 0:
                file.readline()  # Skip partial line
            
            current_pattern_index = 0
            line_number = start
            
            while file.tell() < end:
                line = file.readline()
                line_number += 1
                
                if not timestamped_line_regex.match(line):
                    continue  # Skip lines that do not match timestamped line format
                
                if regexes[current_pattern_index].search(line):
                    results_queue.put((line_number, line.strip()))
                    current_pattern_index += 1
                    if current_pattern_index == len(patterns):
                        break
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to manage multithreaded searching
def search_sequence_multithreaded(filename, patterns, num_threads=4):
    try:
        file_size = os.path.getsize(filename)
        chunk_size = file_size // num_threads
        threads = []
        results_queue = Queue()

        def thread_target(thread_index):
            search_sequence_chunk(filename, patterns, thread_index * chunk_size, (thread_index + 1) * chunk_size if thread_index < num_threads - 1 else file_size, results_queue)

        for i in range(num_threads):
            thread = threading.Thread(target=thread_target, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if not results_queue.empty():
            print("Sequence found in the file.")
            while not results_queue.empty():
                result = results_queue.get()
                print(f"Pattern found at line {result[0]}: {result[1]}")
        else:
            print("Sequence not found in the file.")
        
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
    except IOError:
        print(f"An error occurred while reading the file {filename}.")

# Example usage
search_sequence_multithreaded('sample.txt', sequence_of_lines)
