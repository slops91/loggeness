import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import zipfile
import tkinterdnd2 as tkdnd

class LogAnalysisApp(tkdnd.TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("LogAnalysis")
        self.geometry("600x600")
        self.test_case_label = tk.Label(self, text="Enter Test Case:")
        self.test_case_label.pack(pady=10)
        self.test_case_entry = tk.Entry(self, width=50)
        self.test_case_entry.pack(pady=10)
        self.browse_button = tk.Button(self, text="Browse File", command=self.browse_file)
        self.browse_button.pack(pady=10)
        self.drop_area = tk.Label(self, text="Drag and Drop Files Here", bg="lightgrey", width=50, height=10)
        self.drop_area.pack(pady=20)
        self.drop_area.drop_target_register(tkdnd.DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.handle_drop)
        self.dest_dir_button = tk.Button(self, text="Choose Destination Directory (Optional)", command=self.choose_dest_dir)
        self.dest_dir_button.pack(pady=10)
        self.file_content_label = tk.Label(self, text="File Contents:")
        self.file_content_label.pack(pady=10)
        self.file_content_text = tk.Text(self, height=15, width=70)
        self.file_content_text.pack(pady=10)
        self.dest_dir = os.getcwd()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.handle_file(file_path)

    def handle_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            self.handle_file(file)

    def handle_file(self, file_path):
        if self.is_zip_file(file_path):
            extracted_files = self.extract_zip(file_path)
            for file in extracted_files:
                if file.endswith('.log'):
                    self.process_file(file)
        else:
            if file_path.endswith('.log'):
                self.process_file(file_path)

    def is_zip_file(self, file_path):
        return zipfile.is_zipfile(file_path)

    def extract_zip(self, zip_path):
        extraction_dir = os.path.join(self.dest_dir, os.path.splitext(os.path.basename(zip_path))[0])
        os.makedirs(extraction_dir, exist_ok=True)
        log_files = []
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.log'):
                    zip_ref.extract(file, extraction_dir)
                    log_files.append(os.path.join(extraction_dir, file))
        messagebox.showinfo("Success", f"Extracted .log files from '{zip_path}' to '{extraction_dir}'")
        return log_files

    def process_file(self, file_path):
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(self.dest_dir, file_name)
        shutil.copy(file_path, dest_path)
        self.display_file_contents(file_path)
        messagebox.showinfo("Success", f"File '{file_name}' has been copied to '{self.dest_dir}'")

    def display_file_contents(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            self.file_content_text.delete(1.0, tk.END)
            self.file_content_text.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {str(e)}")

    def choose_dest_dir(self):
        self.dest_dir = filedialog.askdirectory()
        if self.dest_dir:
            messagebox.showinfo("Destination Directory", f"Selected Directory: {self.dest_dir}")
        else:
            self.dest_dir = os.getcwd()

app = LogAnalysisApp()
app.mainloop()
