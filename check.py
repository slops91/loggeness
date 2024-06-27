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
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

class App(customtkinter.CTk,TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        # configure window
        self.title("Log Analysis App")
        self.geometry(f"{1100}x700")
        self.TkdndVersion = TkinterDnD._require(self)
        self.file_path=""
        self.dest_directory=""
        # configure grid layout (3x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Log Analysis", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Recently Viewed", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="ew")

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter Test Case and Time of Issue")
        self.entry.grid(row=4, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="ew")

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
        self.choose_label.grid(row=2, column=1, padx=(90,40), pady=(20, 0), sticky="ns")


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
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=400)
    def on_submit(self):
        test_case = self.entry.get()
        if test_case:
            if self.file_path:
                self.start_loading_bar()
                self.extract_and_read_7z(self.file_path, self.dest_directory)
            else:
                tkinter.messagebox.showinfo("Test Case", f"Test Case: {test_case}")
    def browse_file(self):
        self.file_path = tkinter.filedialog.askopenfilename()
        if self.file_path:
            if self.file_path.endswith(".7z"): 
                self.extract_and_read_7z()
            tkinter.messagebox.showinfo("Selected File", f"Selected File: {self.file_path}")
            self.start_loading_bar()

    def on_drop(self, event):
        # Get the file path from the event
        self.file_path = event.data
        # Display the file path
        print(self.file_path)
        self.start_loading_bar()

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

        # Read the contents of the extracted files (example for text files)
        for file_name in extracted_files:
            file_path = os.path.join(self.dest_directory, file_name)
            if file_name.endswith('.log'):  # Adjust this condition based on the file types you're expecting
                with open(file_path, 'r') as file:
                    content = file.read()
                    print(f"Contents of {file_name}:")
                    print(content)
                    print('-' * 40)
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
    def start_loading_bar(self):
        self.progress_bar.grid(row=2, column=1, columnspan=3, pady=20)
        self.progress_bar.start()
        threading.Thread(target=self.run_loading_bar).start()

    def run_loading_bar(self):
        time.sleep(10)  # Simulate a 10-second processing time
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        tkinter.messagebox.showinfo("Processing Complete", "The log file has been processed.")

    

app = App()
app.mainloop()

