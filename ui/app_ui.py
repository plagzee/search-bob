import customtkinter as ctk
from tkinter import filedialog, StringVar
import tkinter.messagebox as tkm
import subprocess
import threading
import os

class XPFileSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Windows XP Search")
        self.geometry("700x500")
        self.configure(padx=20, pady=20)

        self.search_path = StringVar()
        self.filename_query = StringVar()
        self.global_search = ctk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # File name entry
        self.entry_label = ctk.CTkLabel(self, text="Search for file name:")
        self.entry_label.pack(anchor="w", pady=(0, 5))

        self.filename_entry = ctk.CTkEntry(self, textvariable=self.filename_query, width=400)
        self.filename_entry.pack(anchor="w", pady=(0, 10))

        # Folder selector
        self.browse_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.browse_frame.pack(anchor="w", fill="x")

        self.folder_entry = ctk.CTkEntry(self.browse_frame, textvariable=self.search_path, width=400)
        self.folder_entry.pack(side="left", padx=(0, 10))

        self.browse_button = ctk.CTkButton(self.browse_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="left")

        # Global Search Checkbox
        self.global_checkbox = ctk.CTkCheckBox(
            self,
            text="Search Globally (all drives)",
            variable=self.global_search,
            command=self.toggle_global_search
        )
        self.global_checkbox.pack(anchor="w", pady=(10, 0))

        # Search Button
        self.search_button = ctk.CTkButton(self, text="Search", command=self.start_search)
        self.search_button.pack(anchor="w", pady=(20, 10))

        # Results Display
        self.result_box = ctk.CTkTextbox(self, height=300, wrap="none", scrollbar_button_color="lightblue")
        self.result_box.pack(fill="both", expand=True, pady=(10, 0))
        self.result_box.insert("end", "🔍 Search results will appear here...\n")
        self.result_box.configure(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.search_path.set(folder)

    def start_search(self):
        filename = self.filename_query.get().strip()
        is_global = self.global_search.get()
        folder = self.search_path.get().strip()

        if not filename:
            tkm.showwarning("Error", "Please enter a file name to search for.")
            return

        if not is_global and not folder:
            tkm.showwarning("Error", "Please select a folder to search in.")
            return

        # Write to search.bin
        with open("search.bin", "w") as f:
            f.write(f"{filename}\n")
            f.write("\n" if is_global else folder.strip())


        # Show loading message
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", "⏳ Searching... Please wait.\n")
        self.result_box.configure(state="disabled")

        # Start threaded search
        thread = threading.Thread(target=self.run_search_process, daemon=True)
        thread.start()

    def run_search_process(self):
        try:
            subprocess.run(["search.exe"], check=True)
            self.display_results()
        except subprocess.CalledProcessError:
            self.result_box.configure(state="normal")
            self.result_box.delete("1.0", "end")
            self.result_box.insert("end", "❌ Failed to execute search.exe\n")
            self.result_box.configure(state="disabled")

    def display_results(self):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")

        if not os.path.exists("searched.bin"):
            self.result_box.insert("end", "❌ No results found or error occurred.\n")
        else:
            with open("searched.bin", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                if not lines:
                    self.result_box.insert("end", "🔍 No files found matching your query.\n")
                else:
                    self.result_box.insert("end", f"✅ Found {len(lines)} result(s):\n\n")
                    for line in lines:
                        self.result_box.insert("end", line.strip() + "\n")

        self.result_box.configure(state="disabled")

    def toggle_global_search(self):
        if self.global_search.get():
            self.folder_entry.configure(state="disabled")
            self.browse_button.configure(state="disabled")
        else:
            self.folder_entry.configure(state="normal")
            self.browse_button.configure(state="normal")
