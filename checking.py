import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import ttk
from PIL import Image
from tkinterdnd2 import TkinterDnD, DND_ALL
import threading
import time
import py7zr
import os
from datetime import datetime
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")
import re
class App(customtkinter.CTk,TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Log Analysis App")
        self.geometry(f"{1200}x1000")
        self.TkdndVersion = TkinterDnD._require(self)
        self.file_path=""
        self.dest_directory=""
        self.timestamp=""
        self.file_name="dumpState_F741BXXU1AXET_202406071315.log"
        self.test_case=""
        self.test_cases={"1. BT Settings 2. Broadcast Sound from this Phone 3. Start Broadcast":1,"1. BT settings 2. Broadcast sound from this phone 3. Change Broadcast Name 4. Change Password 5. Start Broadcast":2,"1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Stop Broadcast":3,
"1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Play music 5. Stop broadcast":4,"1. Buds connected 2. BT settings 3. Broadcast sound from this phone 4. Start Broadcast 5. Play music 6. Stop broadcast":5,
"1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Play music 5. Turn off BT":6}
        self.patterns = {
1:
{"06-07 13:11:20.109  1000 30688 30688 I SecBluetoothBroadcastSource: startBroadcast By user action":-1
,"06-07 13:11:20.115  1000 30688 30688 D BluetoothLeBroadcast: startBroadcasting":-1
,"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1
,"06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1
,"06-07 13:11:20.393  1002  3965  4183 I bt_stack: [INFO:state_machine.cc(423)] CreateBig broadcast_id=1328137":-1
,"06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1
,"06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1
,"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1
,"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1},
2:{"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1,
   "06-07 13:11:20.386  1002  3965  5071 I bt_stack: [INFO:com_android_bluetooth_le_audio.cpp(1185)] OnBroadcastCreated":-1,
   "06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1,
   "06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1,
   "06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1,
"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1,
"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1},
3:{"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1,
   "06-07 13:11:20.386  1002  3965  5071 I bt_stack: [INFO:com_android_bluetooth_le_audio.cpp(1185)] OnBroadcastCreated":-1,
   "06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1,
   "06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1,
   "06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1,
"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1,
"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1,
"Missing: LeAudioService: stopBroadcast":-1,
"06-07 13:11:35.551  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=16":-1,
"06-07 13:11:35.570  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=17":-1,
"06-07 13:11:35.828  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:642 HandleHciEvent: BIG terminate BIG cmpl, reason=22 big_id=1":-1,
"Missing:bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STOPPED":-1,
"Missing:LeAudioBroadcasterNativeInterface: onBroadcastDestroyed: broadcastId=1328137":-1},
4:{"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1,
   "06-07 13:11:20.386  1002  3965  5071 I bt_stack: [INFO:com_android_bluetooth_le_audio.cpp(1185)] OnBroadcastCreated":-1,
   "06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1,
   "06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1,
   "06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1,
"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1,
"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1,
"06-07 13:11:21.134  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1436)] OnAudioResume":-1,
"06-07 13:11:21.134  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/audio_hal_client/audio_broadcast_source_hal_client.cc:364 ConfirmStreamingRequest:":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioProviderStub: sehStreamStarted - SessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, status=SUCCESS":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioSessionAidl: ReportControlStatus - status=SUCCESS for SehSessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, bluetooth_audio=0x0900 started":-1,
"Missing: LeAudioService: stopBroadcast":-1,
"06-07 13:11:35.551  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=16":-1,
"06-07 13:11:35.570  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=17":-1,
"06-07 13:11:35.828  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:642 HandleHciEvent: BIG terminate BIG cmpl, reason=22 big_id=1":-1,
"Missing:bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STOPPED":-1,
"Missing:LeAudioBroadcasterNativeInterface: onBroadcastDestroyed: broadcastId=1328137":-1},
5:{"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1,
   "06-07 13:11:20.386  1002  3965  5071 I bt_stack: [INFO:com_android_bluetooth_le_audio.cpp(1185)] OnBroadcastCreated":-1,
   "06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1,
   "06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1,
   "06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1,
"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1,
"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1,
"06-07 13:11:20.502  1002  3965  5071 D LeAudioService: addLocalSource: BC:93:07:37:A2:49":-1,
"06-07 13:11:20.502  1002  3965  5071 D BassClientService: addLocalSource : handover group size = 0":-1,
"06-07 13:11:20.507  1002  3965  5221 D BassClientStateMachine: (BC:93:07:37:A2:49) AddSource : Src 07:BB:DC:64:04:EF Bid 1328137 PA_Sync 1 SubGroup 1 [ [0] BIS_Sync 0x2 (Sel) ]":-1,
"06-07 13:11:20.510  1002  3965  5221 D BassClientStateMachine: (BC:93:07:37:A2:5F) AddSource : Src 07:BB:DC:64:04:EF Bid 1328137 PA_Sync 1 SubGroup 1 [ [0] BIS_Sync 0x1 (Sel) ]":-1,
"06-07 13:11:21.326  1002  3965  5071 D BassClientStateMachine: (BC:93:07:37:A2:49) processPASyncState : Initiate local broadcast PAST for: 07:BB:DC:64:04:EF, advSID/Handle: 1, serviceData: 258":-1,
"06-07 13:11:21.796  1002  3965  5071 D BassClientStateMachine: (BC:93:07:37:A2:49) processPASyncState : state - 2, source 07:BB:DC:64:04:EF BIS Sync state - [2]":-1,
"06-07 13:11:21.803  1002  3965  5071 D BassClientStateMachine: (BC:93:07:37:A2:5F) processPASyncState : state - 2, source 07:BB:DC:64:04:EF BIS Sync state - [1]":-1,
"06-07 13:11:21.134  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1436)] OnAudioResume":-1,
"06-07 13:11:21.134  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/audio_hal_client/audio_broadcast_source_hal_client.cc:364 ConfirmStreamingRequest:":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioProviderStub: sehStreamStarted - SessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, status=SUCCESS":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioSessionAidl: ReportControlStatus - status=SUCCESS for SehSessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, bluetooth_audio=0x0900 started":-1,
"Missing: LeAudioService: stopBroadcast":-1,
"06-07 13:11:35.551  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=16":-1,
"06-07 13:11:35.570  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:582 TriggerIsoDatapathTeardown: conn_hdl=17":-1,
"06-07 13:11:35.828  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:642 HandleHciEvent: BIG terminate BIG cmpl, reason=22 big_id=1":-1,
"Missing:bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STOPPED":-1,
"Missing:LeAudioBroadcasterNativeInterface: onBroadcastDestroyed: broadcastId=1328137":-1
        },
6:{"06-07 13:11:20.366  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(652)] CreateAudioBroadcast CreateAudioBroadcast":-1,
   "06-07 13:11:20.386  1002  3965  5071 I bt_stack: [INFO:com_android_bluetooth_le_audio.cpp(1185)] OnBroadcastCreated":-1,
   "06-07 13:11:20.387  1002  3965  5071 D LeAudioService: startBroadcast":-1,
   "06-07 13:11:20.490  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:603 HandleHciEvent: BIG create BIG complete, big_id=1":-1,
   "06-07 13:11:20.491  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=16":-1,
"06-07 13:11:20.497  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/broadcaster/state_machine.cc:533 TriggerIsoDatapathSetup: conn_hdl=17":-1,
"06-07 13:11:20.499  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1118)] OnStateMachineEvent broadcast_id1328137 state=STREAMING":-1,
"06-07 13:11:21.134  1002  3965  4183 I bt_stack: [INFO:broadcaster.cc(1436)] OnAudioResume":-1,
"06-07 13:11:21.134  1002  3965  4183 I bluetooth: packages/modules/Bluetooth/system/bta/le_audio/audio_hal_client/audio_broadcast_source_hal_client.cc:364 ConfirmStreamingRequest:":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioProviderStub: sehStreamStarted - SessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, status=SUCCESS":-1,
"06-07 13:11:21.134  1041  1532  1544 I BTAudioSessionAidl: ReportControlStatus - status=SUCCESS for SehSessionType=LE_AUDIO_BROADCAST_HARDWARE_OFFLOAD_ENCODING_DATAPATH, bluetooth_audio=0x0900 started":-1,
"Missing:BluetoothMapService: STATE_TURNING_OFF":-1,
"Missing:BtOppService: Bluetooth state changed: STATE_TURNING_OFF":-1,
"Missing: SecBluetoothBroadcastSource: BT is disabled":-1
}
        }
        self.timestamped_line_regex = re.compile(r"\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} .*")
        # configure grid layout (3x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Log Analysis", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.show_home)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Recently Viewed", command=self.sidebar_button_event)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        # self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Charts", command=self.sidebar_button_event)
        # self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="ew")

        # create main entry and button
        self.entry = customtkinter.CTkOptionMenu(self,values=["1. BT Settings 2. Broadcast Sound from this Phone 3. Start Broadcast","1. BT settings 2. Broadcast sound from this phone 3. Change Broadcast Name 4. Change Password 5. Start Broadcast","1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Stop Broadcast",
"1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Play music 5. Stop broadcast","1. Buds connected 2. BT settings 3. Broadcast sound from this phone 4. Start Broadcast 5. Play music 6. Stop broadcast",
"1. BT settings 2. Broadcast sound from this phone 3. Start Broadcast 4. Play music 5. Turn off BT"])
        self.entry.set("Enter Test Case and Time of Issue(eg: 'Test1 06-07 13:11:20.491')")
        self.entry.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="ew")
        # self.entry.pack(side="left", fill="x", expand=True)
        # self.timeofissue= customtkinter.CTkEntry(self, placeholder_text="Enter Time of Issue(Optional)")
        # self.timeofissue.grid(row=4,column=3,padx=(20,20),pady=(20,20),sticky="ew")
        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent",text="Submit",command=self.on_submit,border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=4, padx=(20, 20), pady=(20, 20), sticky="ew")

        # create image buttons
        self.dragdrop_image = customtkinter.CTkImage(Image.open("dragndrop.png"), size=(400, 150))
        self.choose_image = customtkinter.CTkImage(Image.open("choose.png"), size=(150, 150))

        button_width = 150
        button_height = 150

        # self.browse_button = customtkinter.CTkButton(self, image=self.browse_image, text="", command=self.browse_file, fg_color="transparent", width=button_width, height=button_height)
        # self.browse_button.grid(row=1, column=1, padx=20, pady=(40, 0), sticky="ew")
        self.dragdrop_button = customtkinter.CTkButton(self, image=self.dragdrop_image,command=self.browse_file, text="", fg_color="transparent", width=button_width, height=button_height)
        self.dragdrop_button.grid(row=1, column=1, padx=(100,40), pady=(75, 0), sticky="ns")
        self.dragdrop_button.drop_target_register(DND_ALL)
        self.dragdrop_button.dnd_bind('<<Drop>>', self.on_drop)
        # self.dragdrop_button.bind("<Button-1>", self.browse_file)
        self.choose_button = customtkinter.CTkButton(self, image=self.choose_image, text="", command=self.choose_destination, fg_color="transparent", width=button_width, height=button_height)
        self.choose_button.grid(row=3, column=1, padx=(100, 40), pady=(20, 0), sticky="ns")

        self.choose_label = customtkinter.CTkLabel(self, text="Choose Destination Directory")
        self.choose_label.grid(row=2, column=1, padx=(90,40), pady=(60, 0), sticky="ns")


        # self.browse_label = customtkinter.CTkLabel(self, text="Browse Files")
        # self.browse_label.grid(row=1, column=1, padx=20, pady=(260, 20), sticky="ew")
        # self.dragdrop_label = customtkinter.CTkLabel(self, text="Drag & Drop")
        # self.dragdrop_label.grid(row=1, column=2, padx=20, pady=(260, 20), sticky="ew")
        self.animated_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.animated_label.grid(row=0, column=1, columnspan=3, padx=20, pady=(20, 0), sticky="ew")
        self.animated_label = customtkinter.CTkLabel(self, text="", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.animated_label.grid(row=0, column=1, columnspan=3, padx=20, pady=(20, 0), sticky="ew")
        self.text_sequence = ["Welcome to the Log Analysis App!", "\t  Please enter the test case, time of issue and choose the log file from below"]
        self.sequence_index = 0
        self.index = 0
        self.animate_text()
        self.home_widgets = [
            (self.entry, {"row": 4, "column": 1, "columnspan": 3, "padx": (20, 20), "pady": (20, 20), "sticky": "ew"}),
            (self.main_button_1, {"row": 4, "column": 4, "padx": (20, 20), "pady": (20, 20), "sticky": "ew"}),
            (self.dragdrop_button, {"row": 1, "column": 1, "padx": (100, 40), "pady": (75, 0), "sticky": "ns"}),
            (self.choose_button, {"row": 3, "column": 1, "padx": (100, 40), "pady": (20, 0), "sticky": "ns"}),
            (self.choose_label, {"row": 2, "column": 1, "padx": (90, 40), "pady": (20, 0), "sticky": "ns"}),
            (self.animated_label, {"row": 0, "column": 1, "columnspan": 3, "padx": 20, "pady": (20, 0), "sticky": "ew"})]
            # (self.timeofissue, {"row":4,"column":3,"padx":(20,20),"pady":(20,20),"sticky":"ew"})]
        self.dashboard_widgets = []
        self.show_home()
    def on_submit(self):
        self.test_case = self.entry.get()
        self.timestamp=self.show_timestamp_entry()
    def show_timestamp_entry(self):
        self.timestamp_frame = customtkinter.CTkFrame(self)
        self.timestamp_frame.grid(row=5, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        
        self.timestamp_entry = customtkinter.CTkEntry(self.timestamp_frame, placeholder_text="Enter Timestamp (optional)")
        self.timestamp_entry.pack(pady=10, padx=20, fill="x")
        
        submit_button = customtkinter.CTkButton(self.timestamp_frame, text="Submit", command=self.on_timestamp_submit)
        submit_button.pack(pady=10)

    def on_timestamp_submit(self):
        self.timestamp = self.timestamp_entry.get()
        self.timestamp_frame.destroy()  # Remove the timestamp entry and submit button after submitting
        if self.file_path and self.file_path.endswith(".7z"):
                self.extract_and_read_7z()
        elif self.file_path:
                self.show_dashboard()

    def browse_file(self):
        self.file_path = tkinter.filedialog.askopenfilename()
        count=0
        if self.file_path:
            if self.file_path.endswith(".7z"): 
                self.extract_and_read_7z()
            else:
                tkinter.messagebox.showinfo("Selected File", f"Selected File: {self.file_path}")
                # if self.file_path.endswith('.log'):  # Adjust this condition based on the file types you're expecting
                #     try:
                #         with open(self.file_path, 'r',errors='ignore') as file:
                #             for line in file:
                #                 print(line.strip()," line: ",count)
                #                 count=count+1
                #                 print('-' * 40)
                #     except FileNotFoundError:
                #         print("This file does not exist.")
                #     except IOError:
                #         print("An error occured.")

    def on_drop(self, event):
        # Get the file path from the event
        self.file_path = event.data
        # Display the file path
        print(self.file_path)

    def choose_destination(self):
        self.dest_directory = tkinter.filedialog.askdirectory()
        if self.dest_directory:
            tkinter.messagebox.showinfo("Chosen Destination Directory", f"Chosen Destination Directory: {self.dest_directory}")
        else:
            self.dest_directory = os.getcwd()
    def extract_and_read_7z(self):
        if not self.dest_directory:
            self.dest_directory = os.getcwd()
        
        # Ensure the extraction directory exists
        os.makedirs(self.dest_directory, exist_ok=True)

        # Open the .7z file and extract its contents
        with py7zr.SevenZipFile(self.file_path, mode='r') as archive:
            archive.extractall(path=self.dest_directory)

        print(f"Extraction completed. Files are extracted to {self.dest_directory}")

        # List the files in the extraction directory
        extracted_files = os.listdir(self.dest_directory)
        print(f"Extracted files: {extracted_files}")
        count=0
        # Read the contents of the extracted files (example for text files)
        for file_name in extracted_files:
            file_path = os.path.join(self.dest_directory, file_name)
            if file_name.endswith('.log'):  # Adjust this condition based on the file types you're expecting
                try:
                    with open(file_path, 'r',errors='ignore') as file:
                        for line in file:
                            print(line.strip()," line: ",count)
                            count=count+1
                            print('-' * 40)
                except FileNotFoundError:
                    print("This file does not exist.")
                except IOError:
                    print("An error occured.")
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def animate_text(self):
        current_text = self.text_sequence[self.sequence_index]
        self.animated_label.configure(text=current_text[:self.index])
        self.index += 1
        if self.index <= len(current_text):
            self.after(50, self.animate_text)
        else:
            self.sequence_index += 1
            if self.sequence_index < len(self.text_sequence):
                self.index = 0
                self.after(600, self.clear_text)  # Pause before clearing the text

    def clear_text(self):
        self.animated_label.configure(text="")
        self.after(50, self.animate_text)  
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
# Regular expression to match timestamped lines with various log levels
# Function to search for patterns in the file
    def search_patterns(self):
        try:
            line_no=0
            err_count=0
            flag=0
            log_lines=[]
            num=self.test_cases[self.test_case]
            patterns=self.patterns[num]
            cur_index=0
            with open(self.file_name, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    line_no+=1
                    if not self.timestamped_line_regex.match(line):
                        continue  # Skip lines that do not match timestamped line format
                    line=line.strip()
                    line=line.replace("'","")
                    parts=line.split()
                    if len(parts)<6:
                        continue
                    if parts[5]=='E':
                        err_count+=1
                    if line in patterns:
                        patterns[line]=1
                        # self.add_log_entry(line,0)
                        # if line==patterns[0]:
                        #     flag=1
                        # elif line==patterns[len(patterns)-1]:
                        #     flag=0
            self.update_error_count(err_count)
            for key in patterns.keys():
                self.add_log_entry(key,patterns[key])
        except FileNotFoundError:
            print(f"The file {self.file_name} does not exist.")
        except IOError:
            print(f"An error occurred while reading the file {self.file_name}.")
    def add_log_entry(self,log,e):
        log_entry_frame = customtkinter.CTkFrame(self.log_labels_frame, fg_color="transparent")
        log_entry_frame.pack(fill="x", padx=10, pady=1)
        color = "yellow" if e ==-1 else "blue"
        log_color_frame = customtkinter.CTkFrame(log_entry_frame, fg_color=color, width=5, height=30)
        log_color_frame.pack(side="left", fill="y", padx=(0, 10), pady=1)

        log_label = customtkinter.CTkLabel(log_entry_frame, text=log, anchor="w", height=30, fg_color="transparent")
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

    def show_home(self):
        # Hide dashboard widgets
        for widget, grid_info in self.dashboard_widgets:
            widget.grid_forget()

        # Show home widgets
        for widget, grid_info in self.home_widgets:
            widget.grid(**grid_info)

    def show_dashboard(self):
        # Hide home widgets
        for widget, grid_info in self.home_widgets:
            widget.grid_forget()

        # Create dashboard widgets if not already created
        if not self.dashboard_widgets:
            # Top bar with filter in the top right corner
            top_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.dashboard_widgets.append((top_frame, {"row": 0, "column": 1, "columnspan": 2, "sticky": "ew", "pady": (10, 10), "padx": (10, 10)}))

            search_entry = customtkinter.CTkEntry(top_frame, placeholder_text="Search...🔍 ", fg_color="transparent", width=800)
            search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            # Error count display
            error_count_frame = customtkinter.CTkFrame(top_frame, fg_color="transparent")
            error_count_frame.pack(side="right", padx=10, pady=10)
            error_summary_label = customtkinter.CTkLabel(error_count_frame, text="Errors:", font=("Helvetica", 16), fg_color="transparent")
            error_summary_label.pack(anchor="center")

            self.error_count_label = customtkinter.CTkLabel(error_count_frame, text="0", font=("Helvetica", 48, "bold"), fg_color="transparent")
            self.error_count_label.pack(anchor="center")

            # Filters section on the left

            # Logs display area with scrollbar
            logs_frame = customtkinter.CTkFrame(self, fg_color="transparent")
            self.dashboard_widgets.append((logs_frame, {"row": 1, "column": 1, "sticky": "nsew", "padx": (10, 10), "pady": (10, 10)}))
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
            self.search_patterns()
            self.test_case=""
        for widget, grid_info in self.dashboard_widgets:
            widget.grid(**grid_info)
        # Create dashboard widgets if not already created
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    

app = App()
app.mainloop()
