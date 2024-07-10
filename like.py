import tkinter
import customtkinter
from tkinter import ttk
import re
from datetime import datetime
from check2 import search_patterns
customtkinter.set_appearance_mode("Dark")  # Set dark mode
customtkinter.set_default_color_theme("blue")

class LogViewer(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Log Viewer")
        self.geometry("1200x1000")
        self.file_name="sample.txt"
        # Configure grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Top bar with filter in the top right corner
        top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(10, 10))
        

        search_entry = customtkinter.CTkEntry(top_frame, placeholder_text="Search...🔍", fg_color="transparent", width=800)
        search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)


        # Error count display
        error_count_frame = customtkinter.CTkFrame(top_frame, fg_color="transparent")
        error_count_frame.pack(side="right", padx=10, pady=10)

        error_summary_label = customtkinter.CTkLabel(error_count_frame, text="Errors:", font=("Helvetica", 16), fg_color="transparent")
        error_summary_label.pack(anchor="center")

        self.error_count_label = customtkinter.CTkLabel(error_count_frame, text="0", font=("Helvetica", 48, "bold"), fg_color="transparent")
        self.error_count_label.pack(anchor="center")
        
        # Filters section on the left
        filters_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        filters_frame.grid(row=1, column=0, sticky="nsw", padx=(10, 10), pady=(10, 10))
        
        filters_label = customtkinter.CTkLabel(filters_frame, text="FILTERS", fg_color="transparent")
        filters_label.pack(anchor="nw", padx=10, pady=5)
        
        self.filter_buttons = []
        filters = ["Log Type", "Log Level", "Tags"]
        for filter_item in filters:
            button = customtkinter.CTkButton(filters_frame, text=filter_item, command=lambda item=filter_item: self.filter_logs(item))
            button.pack(anchor="nw", padx=10, pady=5)
            self.filter_buttons.append(button)
        
        # Logs display area with scrollbar
        logs_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        logs_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))
        logs_frame.grid_rowconfigure(0, weight=1)
        logs_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(logs_frame, bg=self.cget("background"))
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = customtkinter.CTkScrollbar(logs_frame, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.log_labels_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.log_labels_frame, anchor="nw")

        self.log_labels_frame.bind("<Configure>", self.on_frame_configure)

        self.logs = []
        self.max_logs = 50
        self.populate_logs()
    
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def parse_logs(self, log_lines):
        log_pattern = re.compile(r'(\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d) \d+ \d+ \d+ ([IDEW]) (.*)')
        logs = []

        for log in log_lines:
            match = log_pattern.match(log)
            if match:
                timestamp_str, level, message = match.groups()
                timestamp = datetime.strptime(timestamp_str, '%m-%d %H:%M:%S.%f')
                logs.append((timestamp, level, message, log))

        return sorted(logs, key=lambda x: x[0])

    def populate_logs(self):
        patterns = [
    "06-07 13:11:20.109 1000 30688 30688 I SecBluetoothBroadcastSource: startBroadcast By user action",
    "06-07 13:11:20.115 1000 30688 30688 D BluetoothLeBroadcast: startBroadcasting",
    "06-07 13:11:20.366 1002 3965 4183 I bt stack: [INFO:broadcaster.cc (652)] CreateAudioBroadcast CreateAudioBroadcast",
    "06-07 13:11:20.387 1002 3965 5071 D LeAudioService: startBroadcast",
    "06-07 13:11:20.393 1002 3965 4183 I bt_stack: [INFO:state_machine.cc(423)] CreateBig broadcast_id=1328137",
    "06-07 13:11:20.490 1002 3965 4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleciEvent: BIG create BIG complete, big_id=1",
    "06-07 13:11:20.491 1002 3965 4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.c:533 TriggerIsoDatapathSetup: conn_hdl=16",
    "06-07 13:11:20.497 1002 3965 4183 I bluetooth: packages /modules/Bluetooth/system/bta/le_ audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17",
    "06-07 13:11:20.499 1002 3965 4183 I bt_stack: [INFO:broadcaster.cc (1118)] OnStateMachineEvent broadcast id1328137 state=STREAMING"
]
        log_lines, error_count= search_patterns(self.file_name,patterns)
        logs = self.parse_logs(log_lines)
        
        for timestamp, level, message, log in logs:
            self.add_log_entry(timestamp, level, message, log)
        
        self.update_error_count(error_count)

    def add_log_entry(self, timestamp, level, message, log):
        log_text = f"{timestamp.strftime('%m-%d %H:%M:%S.%f')} {log[24:]}"  # Formatted log text
        log_entry_frame = customtkinter.CTkFrame(self.log_labels_frame, fg_color="transparent")
        log_entry_frame.pack(fill="x", padx=10, pady=1)
        color = "red" if level == 'E' else "blue"
        log_color_frame = customtkinter.CTkFrame(log_entry_frame, fg_color=color, width=5, height=30)
        log_color_frame.pack(side="left", fill="y", padx=(0, 10), pady=1)

        log_label = customtkinter.CTkLabel(log_entry_frame, text=log_text, anchor="w", height=30, fg_color="transparent")
        log_label.pack(side="left", fill="x", expand=True, padx=10, pady=1)

        self.logs.append(log_entry_frame)
        if len(self.logs) > self.max_logs:
            self.logs[0].destroy()
            self.logs.pop(0)

        self.log_labels_frame.update_idletasks()
        self.canvas.yview_moveto(1)

    def update_error_count(self, count):
        self.error_count_label.configure(text=f"{count:,}")
    
    def filter_logs(self, filter_item):
        print(f"Filtering logs by: {filter_item}")

if __name__ == "__main__":
    app = LogViewer()
    app.mainloop()

