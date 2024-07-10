# Logs display area with scrollbar
logs_frame = customtkinter.CTkFrame(self, fg_color="transparent")
logs_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))
logs_frame.grid_rowconfigure(0, weight=1)
logs_frame.grid_columnconfigure(0, weight=1)

self.canvas = tkinter.Canvas(logs_frame, bg=self.cget("background"))
self.canvas.grid(row=0, column=0, sticky="nsew")

self.scrollbar_y = customtkinter.CTkScrollbar(logs_frame, command=self.canvas.yview)
self.scrollbar_y.grid(row=0, column=1, sticky="ns")

self.scrollbar_x = customtkinter.CTkScrollbar(logs_frame, command=self.canvas.xview, orient="horizontal")
self.scrollbar_x.grid(row=1, column=0, sticky="ew")

self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

self.log_labels_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
self.canvas.create_window((0, 0), window=self.log_labels_frame, anchor="nw")

self.log_labels_frame.bind("<Configure>", self.on_frame_configure)
