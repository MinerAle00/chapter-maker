import customtkinter as ctk
from tkinter import filedialog, ttk
import csv
import os
import subprocess

class ModernChapterMaker:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Chapter Maker")
        self.app.geometry("1000x700")
        
        # Force dark mode
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Store chapters and current file path
        self.chapters = []
        self.current_file = None
        
        self.create_gui()
        self.update_treeview_colors()

    def create_gui(self):
        # Create main container with padding
        self.main_container = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Top frame for title
        top_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title = ctk.CTkLabel(
            top_frame,
            text="Chapter Maker",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left")
        
        # Button frame
        button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        # Select CSV button
        self.select_button = ctk.CTkButton(
            button_frame,
            text="Select CSV File",
            command=self.select_file,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.select_button.pack(side="left", padx=(0, 10))
        
        # Copy button
        self.copy_button = ctk.CTkButton(
            button_frame,
            text="Copy All Chapters",
            command=self.copy_all,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.copy_button.pack(side="left", padx=(0, 10))
        
        # Save button
        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Chapters",
            command=self.save_chapters,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.save_button.pack(side="left")
        
        # Status label
        self.status_var = ctk.StringVar()
        self.status_label = ctk.CTkLabel(
            button_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.status_label.pack(side="left", padx=20)
        
        # Create treeview frame
        self.tree_frame = ctk.CTkFrame(self.main_container)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        self.style = ttk.Style()
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("Time", "Chapter"),
            show="headings"
        )
        
        # Configure columns
        self.tree.heading("Time", text="Time")
        self.tree.heading("Chapter", text="Chapter")
        self.tree.column("Time", width=200)
        self.tree.column("Chapter", width=600)
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self.tree_frame,
            command=self.tree.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        
        # Configure treeview
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)

    def update_treeview_colors(self):
        # Dark theme colors
        bg_color = "#2b2b2b"
        fg_color = "white"
        selected_bg = "#1f538d"
        heading_bg = "#1f538d"
        heading_fg = "white"
        
        self.style.configure(
            "Treeview",
            background=bg_color,
            foreground=fg_color,
            fieldbackground=bg_color,
            rowheight=30
        )
        
        self.style.configure(
            "Treeview.Heading",
            background=heading_bg,
            foreground=heading_fg,
            relief="flat"
        )
        
        self.style.map(
            "Treeview",
            background=[('selected', selected_bg)],
            foreground=[('selected', 'white')]
        )

    def show_status(self, message, duration=2000):
        self.status_var.set(message)
        self.app.after(duration, lambda: self.status_var.set(""))

    def macos_copy_to_clipboard(self, text):
        try:
            process = subprocess.Popen(
                'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        except:
            return False

    def copy_all(self):
        if not self.chapters:
            self.show_status("No chapters to copy")
            return
            
        text_to_copy = '\n'.join([f"{time} {note}" for time, note in self.chapters])
        if self.macos_copy_to_clipboard(text_to_copy):
            self.show_status("✓ Chapters copied to clipboard!")
        else:
            self.show_status("Failed to copy to clipboard")

    def format_time(self, time_str):
        parts = time_str.split(':')
        if len(parts) == 4:  # HH:MM:SS:FF format
            # Take only minutes and seconds
            return f"{parts[1]}:{parts[2]}"
        return time_str

    def select_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.current_file = filename
            self.process_csv(filename)
            self.show_status(f"✓ Loaded: {os.path.basename(filename)}")

    def save_chapters(self):
        if not self.chapters:
            self.show_status("No chapters to save")
            return
        
        # Get the directory of the source file
        initial_dir = os.path.dirname(self.current_file) if self.current_file else os.getcwd()
        
        # Get source filename without extension
        suggested_name = "chapters.txt"
        if self.current_file:
            base_name = os.path.splitext(os.path.basename(self.current_file))[0]
            suggested_name = f"{base_name}_chapters.txt"
        
        # Show save dialog
        filename = filedialog.asksaveasfilename(
            initialdir=initial_dir,
            initialfile=suggested_name,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    for time, note in self.chapters:
                        file.write(f"{time} {note}\n")
                self.show_status("✓ Chapters saved successfully!")
            except Exception as e:
                self.show_status("Failed to save chapters")

    def process_csv(self, filename):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.chapters.clear()
        
        with open(filename, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                time = self.format_time(row['Record In'])
                note = row['Notes']
                if time and note:
                    self.chapters.append((time, note))
                    self.tree.insert('', "end", values=(time, note))

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = ModernChapterMaker()
    app.run()
