# imports necessary to get the path where the files are extracted in
import os
import sys

# initializing a variable containing the path where application files are stored.
application_path = ''

# attempting to get where the program files are stored
if getattr(sys, 'frozen', False):
    # if program was frozen (compiled) using pyinstaller, the pyinstaller bootloader creates a sys attribute
    # frozen=True to indicate that the script file was compiled using pyinstaller, then it creates a
    # constant in sys that points to the directory where program executable is (where program files are extracted in).
    application_path = sys._MEIPASS
else:
    # if program is not frozen (compiled) using pyinstaller and is running normally like a Python 3.x.x file.
    application_path = os.path.dirname(os.path.abspath(__file__))
    
import re
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import logging
import json

guid_pattern = re.compile(r'guid: (\w+)')

class GuidScriptFixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EFT Script GUID Fix Tool")
        self.geometry("1200x600")
        self.config_path = os.path.join(os.path.curdir, "WeaponAIOTool_Paths.json")
        
        self.project_var = tk.StringVar()
        self.sdk_var = tk.StringVar()
        
        self.create_widgets()
        self.load_config()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='guid_fix.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def create_widgets(self):
        # Main frames with adjusted proportions
        left_frame = ctk.CTkFrame(self, width=400)  # Fixed width for input section
        left_frame.pack(side="left", fill="y", expand=False, padx=10, pady=10)
        
        # Right frame takes remaining space
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Input Section (existing code remains the same)
        input_frame = ctk.CTkFrame(left_frame)
        input_frame.pack(padx=10, pady=10, fill="x")

        # Project Assets Path
        ctk.CTkLabel(input_frame, text="Exported Project 'Assets' Path:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(input_frame, textvariable=self.project_var, width=350).grid(row=0, column=1, padx=5)
        ctk.CTkButton(input_frame, text="Browse", width=90, command=lambda: self.select_directory(self.project_var)).grid(row=0, column=2, padx=5)

        # SDK Path
        ctk.CTkLabel(input_frame, text="Escape From Tarkov SDK Path:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(input_frame, textvariable=self.sdk_var, width=350).grid(row=1, column=1, padx=5)
        ctk.CTkButton(input_frame, text="Browse", width=90, command=lambda: self.select_directory(self.sdk_var)).grid(row=1, column=2, padx=5)

        # Process Button
        ctk.CTkButton(left_frame, text="Fix Script GUIDs", command=self.process_scripts).pack(pady=15)

        # Wider Log Output (expands to fill remaining space)
        self.log_text = ctk.CTkTextbox(right_frame, wrap=ctk.WORD, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Appearance Settings
        self.create_appearance_settings(left_frame)

    def create_appearance_settings(self, parent):
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Appearance Mode
        ctk.CTkLabel(options_frame, text="Appearance:").pack(side="left", padx=(10, 0))
        self.appearance_mode = ctk.CTkOptionMenu(
            options_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode.pack(side="left", fill="x", expand=True)
        self.appearance_mode.set("System")

        # UI Scaling
        ctk.CTkLabel(options_frame, text="Scaling:").pack(side="left", padx=(10, 0))
        self.ui_scaling = ctk.CTkOptionMenu(
            options_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling
        )
        self.ui_scaling.pack(side="left", fill="x", expand=True)
        self.ui_scaling.set("100%")

    def select_directory(self, target_var):
        directory = filedialog.askdirectory()
        if directory:
            target_var.set(directory)
            if target_var == self.sdk_var:
                self.save_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.sdk_var.set(config.get("sdk_path", ""))
            except Exception as e:
                self.log(f"Config load error: {str(e)}", logging.ERROR)


    def save_config(self):
        """Save current folder paths while preserving existing config properties"""
        try:
            # Load existing config if it exists
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
            
            # Update only the specific value we want to change
            config["sdk_path"] = self.sdk_var.get()
            
            # Write back the merged config
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)  # Added indent for better human readability
                
        except Exception as e:
            self.log(f"Error saving config: {e}")


    def log(self, message, level=logging.INFO):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")
        
        if level == logging.ERROR:
            logging.error(message)
        else:
            logging.info(message)

    def extract_guid_from_meta(self, meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return guid_pattern.search(f.read()).group(1)
        except Exception as e:
            self.log(f"Error reading {meta_path}: {str(e)}", logging.ERROR)
            return None

    def process_scripts(self):
        # Reset counters
        self.total_processed = 0
        self.total_patched = 0
        self.total_skipped = 0
        self.total_errors = 0
        
        # Clear log
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        # Validate paths
        project_path = self.project_var.get()
        sdk_path = self.sdk_var.get()
        
        if not all([project_path, sdk_path]):
            self.log("Error: Please select both required paths", logging.ERROR)
            return

        broken_path = os.path.join(project_path, "Scripts", "Assembly-CSharp")
        working_path = os.path.join(sdk_path, "Assets", "Scripts")

        if not all(map(os.path.exists, [project_path, broken_path, working_path])):
            self.log("Error: One or more required paths are invalid", logging.ERROR)
            return

        # Process GUIDs
        try:
            # Step 1: Collect broken GUIDs
            broken_guids = {}
            for root, _, files in os.walk(broken_path):
                for file in files:
                    if file.endswith(".meta"):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, broken_path)
                        if guid := self.extract_guid_from_meta(full_path):
                            broken_guids[guid] = rel_path

            # Step 2: Find working GUID replacements
            working_guids = {}
            for guid, rel_path in broken_guids.items():
                working_meta = os.path.join(working_path, rel_path)
                if os.path.exists(working_meta):
                    if new_guid := self.extract_guid_from_meta(working_meta):
                        working_guids[guid] = new_guid

            # Step 3: Process project files
            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.split(".")[-1] in ["unity", "prefab", "controller", "asset"]:
                        file_path = os.path.join(root, file)
                        self.process_file(file_path, working_guids)

            # Final report
            self.log("\nProcessing complete!")
            self.log(f"Patched files: {self.total_patched}")
            self.log(f"Skipped files: {self.total_skipped}")
            self.log(f"Errors: {self.total_errors}")
            if missing := len(set(broken_guids.keys()) - set(working_guids.keys())):
                self.log(f"Number of files without matching GUIDs: {missing}")

        except Exception as e:
            self.log(f"Critical error: {str(e)}", logging.ERROR)

    def process_file(self, file_path, guid_map):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original = content
            for old_guid, new_guid in guid_map.items():
                content = content.replace(old_guid, new_guid)

            if content != original:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.total_patched += 1
                self.log(f"Updated: {os.path.relpath(file_path, self.project_var.get())}")
            else:
                self.total_skipped += 1
                
        except Exception as e:
            self.total_errors += 1
            self.log(f"Error processing {file_path}: {str(e)}", logging.ERROR)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def change_scaling(self, scale):
        ctk.set_widget_scaling(int(scale.replace("%", "")) / 100)

if __name__ == "__main__":
    app = GuidScriptFixApp()
    app.mainloop()