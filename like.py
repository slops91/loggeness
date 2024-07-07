import threading
from queue import Queue

# Function to process each chunk of the log file
def process_chunk(chunk, target_lines, results_queue):
    for line in chunk.splitlines():
        if line in target_lines:
            results_queue.put(line)

# Function to read the log file in chunks
def read_log_file(file_path, chunk_size=1024*1024):
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

# Function to handle multithreaded search
def search_log_file(file_path, target_lines, num_threads=4):
    results_queue = Queue()
    threads = []
    
    for chunk in read_log_file(file_path):
        thread = threading.Thread(target=process_chunk, args=(chunk, target_lines, results_queue))
        threads.append(thread)
        thread.start()
        
        # If the number of active threads reaches the limit, wait for them to finish
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for any remaining threads to finish
    for thread in threads:
        thread.join()

    # Collect all results
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    return results

# Usage example
log_file_path = 'path_to_your_log_file.log'
target_lines = [
    "06-07 13:11:20.109 1000 30688 30688 I SecBluetoothBroadcastSource: startBroadcast By user action",
    "06-07 13:11:20.115 1000 30688 30688 D BluetoothLeBroadcast: startBroadcasting",
    "06-07 13:11:20.366 1002 3965 4183 I bt stack: [INFO:broadcaster.cc (652)] CreateAudioBroadcast CreateAudioBroadcast",
    "06-07 13:11:20.387 1002 3965 5071 D LeAudioService: startBroadcast",
    "06-07 13:11:20.393 1002 3965 4183 I bt_stack: [INFO:state_machine.cc(423)] CreateBig broadcast_id=1328137",
    "06-07 13:11:20.490 1002 3965 4183 I bluetooth: packages /modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleciEvent: BIG create BIG complete, big_id=1",
    "06-07 13:11:20.491 1002 3965 4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.c:533 TriggerIsoDatapathSetup: conn_hdl=16",
    "06-07 13:11:20.497 1002 3965 4183 I bluetooth: packages /modules/Bluetooth/system/bta/le_ audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17",
    "06-07 13:11:20.499 1002 3965 4183 I bt_stack: [INFO:broadcaster.cc (1118)] OnStateMachineEvent broadcast id1328137 state=STREAMING"
]
matches = search_log_file(log_file_path, target_lines)

# Print the matched lines
for match in matches:
    print(match)
