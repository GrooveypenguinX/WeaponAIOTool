import os
import re
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import logging

# Define the regex pattern for the broken script GUID
guid_pattern = re.compile(r'guid: (\w+)')

class GuidScriptFixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GUID Script Fix Tool")
        self.geometry("1200x600")

        self.create_widgets()

    def create_widgets(self):
        # Frame for left and right sections
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        # Variables to store folder paths and statistics
        self.broken_var = tk.StringVar()
        self.working_var = tk.StringVar()
        self.project_var = tk.StringVar()
        self.total_processed = 0
        self.total_patched = 0
        self.total_skipped = 0
        self.total_errors = 0

        # Function to open a directory dialog and set the selected path to a variable
        def select_directory(var):
            directory = ctk.filedialog.askdirectory()
            if directory:
                var.set(directory)

        # Function to extract the GUID from a .meta file
        def extract_guid_from_meta(meta_file_path):
            with open(meta_file_path, 'r', encoding='utf-8') as meta_file:
                meta_data = meta_file.read()
            match = guid_pattern.search(meta_data)
            if match:
                return match.group(1)
            return None

        # Function to process the scripts
        def process_scripts():
            self.total_processed = 0
            self.total_patched = 0
            self.total_skipped = 0
            self.total_errors = 0

            def update_log(message, log_level=logging.INFO):
                log_text.configure(state="normal")
                log_text.insert(ctk.END, message)
                log_text.configure(state="disabled")
                log_text.see(ctk.END)  # Scroll to the end
                log_text.update_idletasks()  # Update the GUI immediately

                # Log the message to a file
                if log_level == logging.ERROR:
                    logging.error(message)
                else:
                    logging.info(message)

            update_log("Processing scripts...\n")

            # Validate selected directories
            if not os.path.exists(self.project_var.get()):
                update_log("Error: Main Assets Folder does not exist.", log_level=logging.ERROR)
                process_button.configure(state="normal")
                return

            if not os.path.exists(self.broken_var.get()):
                update_log("Error: Broken Script Folder does not exist.", log_level=logging.ERROR)
                process_button.configure(state="normal")
                return

            if not os.path.exists(self.working_var.get()):
                update_log("Error: Working Script Folder does not exist.", log_level=logging.ERROR)
                process_button.configure(state="normal")
                return

            # Step 1: Extract broken GUIDs and relative paths from the "Broken Script Folder"
            update_log("Extracting broken GUIDs and relative paths...\n")
            broken_guids = {}
            for root, _, files in os.walk(self.broken_var.get()):
                for file in files:
                    if file.endswith(".meta"):
                        relative_path = os.path.relpath(os.path.join(root, file), self.broken_var.get())
                        broken_guid = extract_guid_from_meta(os.path.join(root, file))
                        if broken_guid:
                            broken_guids[broken_guid] = relative_path

            # Step 2: Search for working GUIDs in the "Working Script Folder" based on relative paths
            update_log("Searching for working GUIDs...\n")
            working_guids = {}
            for broken_guid, relative_path in broken_guids.items():
                working_meta_file = os.path.join(self.working_var.get(), relative_path)
                if os.path.exists(working_meta_file):
                    working_guid = extract_guid_from_meta(working_meta_file)
                    if working_guid:
                        working_guids[broken_guid] = working_guid

            # Step 3: Create a set of all broken GUIDs to be replaced
            broken_guid_set = set(broken_guids.keys())

            # Step 4: Iterate through the "Main Assets Folder" and patch files
            update_log("Patching files...\n")
            patched_scripts = []  # List to store successfully patched scripts
            for root, _, files in os.walk(self.project_var.get()):
                for file in files:
                    if file.endswith((".unity", ".prefab", ".controller", ".asset")):
                        file_path_proj = os.path.join(root, file)
                        try:
                            with open(file_path_proj, 'r', encoding='utf-8') as file:
                                file_data = file.read()
                            guid_updated = False  # Flag to check if GUIDs were updated
                            # Replace all instances of broken GUIDs in the file data
                            for broken_guid, working_guid in working_guids.items():
                                if broken_guid in file_data:
                                    guid_updated = True
                                    file_data = file_data.replace(broken_guid, working_guid)
                            if guid_updated:
                                # Write the updated data back to the file
                                with open(file_path_proj, 'w', encoding='utf-8') as file:
                                    file.write(file_data)
                                self.total_patched += 1
                                patched_scripts.append(file_path_proj)  # Add to patched_scripts list
                                update_log(f"- Updated: {file_path_proj}\n")
                            else:
                                self.total_skipped += 1  # No GUIDs were updated
                                update_log(f"- Skipped: {file_path_proj} (No GUIDs were updated)\n")
                        except Exception as e:
                            self.total_errors += 1
                            update_log(f"- Error processing: {file_path_proj}\n{str(e)}\n")

            update_log("Script completed.\n")
            update_log(f"Files successfully patched: {self.total_patched}\n")
            update_log(f"Files skipped: {self.total_skipped}\n")
            update_log(f"Total errors encountered: {self.total_errors}\n")

            # Display the number of broken scripts without matching working scripts
            broken_scripts_without_match = broken_guid_set.difference(set(working_guids.keys()))
            update_log(f"Broken scripts without matching working scripts: {len(broken_scripts_without_match)}\n")

        # Left Section: Input
        input_frame = ctk.CTkFrame(left_frame)
        input_frame.pack(padx=10, pady=10, fill="both")

        # Main Assets Folder
        ctk.CTkLabel(input_frame, text="Main Assets Folder").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.project_var, width=250).grid(row=0, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_directory(self.project_var)).grid(row=0, column=2)

        # Broken Script Folder
        ctk.CTkLabel(input_frame, text="Broken Script Folder").grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.broken_var, width=250).grid(row=1, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_directory(self.broken_var)).grid(row=1, column=2)

        # Working Script Folder
        ctk.CTkLabel(input_frame, text="Working Script Folder").grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.working_var, width=250).grid(row=2, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_directory(self.working_var)).grid(row=2, column=2)

        # Right Section: Output
        log_text = ctk.CTkTextbox(right_frame, wrap=ctk.WORD, height=20, width=550, state="disabled")
        log_text.pack(padx=10, pady=10, fill="both", expand="yes")

        process_button = ctk.CTkButton(left_frame, text="Process Scripts", command=process_scripts)
        process_button.pack(padx=10, pady=5)

        # Frame for Appearance and Scaling Options
        options_frame = ctk.CTkFrame(left_frame)
        options_frame.pack(side="bottom", fill="x")

        # Appearance Option
        self.appearance_mode_label = ctk.CTkLabel(options_frame, text="Appearance:")
        self.appearance_mode_label.pack(side="left", padx=(10, 0))

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(options_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.pack(side="left", fill="x", expand=True)

        self.appearance_mode_optionmenu.set("System")  # Set default value

        # Scaling Option
        self.scaling_label = ctk.CTkLabel(options_frame, text="Scaling:")
        self.scaling_label.pack(side="left", padx=(10, 0))

        self.scaling_optionmenu = ctk.CTkOptionMenu(options_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionmenu.pack(side="left", fill="x", expand=True)

        self.scaling_optionmenu.set("100%")  # Set default value


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = GuidScriptFixApp()
    app.mainloop()
