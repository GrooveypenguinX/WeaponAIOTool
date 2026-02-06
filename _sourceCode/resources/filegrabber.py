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
    
import json
import shutil
import customtkinter as ctk
from tkinter import filedialog

# Define the blacklist of files to exclude
BLACKLIST = [
    "cubemaps",
    "shaders",
    "assets/systems/effects/smoke.bundle",
    "assets/systems/effects/muzzleflash/muzzleflash.bundle",
    "assets/systems/effects/heathaze/defaultheathaze.bundle",
    "assets/content/weapons/animations/simple_animations.bundle",
    "assets/content/weapons/animations/spirit_animations.bundle",
    "assets/content/weapons/weapon_root_anim_fix.bundle",
    "assets/commonassets/physics/physicsmaterials.bundle",
    "assets/content/weapons/wip/kibas tuning prefabs/muzzlejets_templates/default_assets.bundle",
    "assets/content/audio/blendoptions/assets.bundle",
    "assets/content/weapons/additional_hands/client_assets.bundle",
]

class TarkovFileCopyTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tarkov File Copy Tool")
        self.geometry("1000x800")

        self.windows_data = None

        # Left Frame
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        eft_folder_label = ctk.CTkLabel(left_frame, text="Select EFT Folder:")
        eft_folder_label.pack()

        self.eft_folder_entry = ctk.CTkEntry(left_frame, width=300)
        self.eft_folder_entry.pack(pady=5)

        eft_folder_button = ctk.CTkButton(left_frame, text="Browse", command=self.browse_eft_folder)
        eft_folder_button.pack(pady=5)

        export_folder_label = ctk.CTkLabel(left_frame, text="Select Export Folder:")
        export_folder_label.pack()

        self.export_folder_entry = ctk.CTkEntry(left_frame, width=300)
        self.export_folder_entry.pack(pady=5)

        export_folder_button = ctk.CTkButton(left_frame, text="Browse", command=self.browse_export_folder)
        export_folder_button.pack(pady=5)

        self.copy_button = ctk.CTkButton(
            left_frame, text="Copy Selected Bundle", command=self.copy_selected_bundle, state="disabled"
        )
        self.copy_button.pack(pady=10)

        # Right Frame
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        search_label = ctk.CTkLabel(right_frame, text="Search Bundles:")
        search_label.pack(pady=5)

        self.search_entry = ctk.CTkEntry(right_frame, width=300)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_bundles)

        self.bundle_listbox = ctk.CTkTextbox(right_frame, state="normal", height=600, width=400)
        self.bundle_listbox.pack(fill="both", expand=True)
        self.bundle_listbox.bind("<ButtonRelease-1>", self.on_bundle_select)

        self.logging_text = ctk.CTkTextbox(right_frame, height=200, state="disabled")
        self.logging_text.pack(fill="x", expand=False, pady=5)

        self.config_path = os.path.join(os.path.curdir, "WeaponAIOTool_Paths.json")
        
        # Load saved paths after initializing UI
        self.load_config()

    def log(self, message):
        self.logging_text.configure(state="normal")
        self.logging_text.insert("end", f"{message}\n")
        self.logging_text.see("end")
        self.logging_text.configure(state="disabled")

    def load_config(self):
        """Load saved folder paths from the configuration file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    eft_folder = config.get("eft_folder", "")
                    self.eft_folder_entry.delete(0, "end")
                    self.eft_folder_entry.insert(0, eft_folder)

                    # Automatically load windows.json if EFT folder is valid
                    if eft_folder and os.path.exists(eft_folder):
                        self.load_windows_json()
                        
            except Exception as e:
                self.log(f"Error loading config: {e}")

    def save_config(self):
        """Save current folder paths while preserving existing config properties"""
        try:
            # Load existing config if it exists
            config = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    config = json.load(f)
            
            # Update only the specific value we want to change
            config["eft_folder"] = self.eft_folder_entry.get()
            
            # Write back the merged config
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)  # Added indent for better human readability
                
        except Exception as e:
            self.log(f"Error saving config: {e}")

    def browse_eft_folder(self):
        folder = filedialog.askdirectory()
        if folder:  # Check if a folder was selected (not cancelled)
            self.eft_folder_entry.delete(0, "end")
            self.eft_folder_entry.insert(0, folder)
            self.save_config()  # Save the new path
            self.load_windows_json()

    def browse_export_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.export_folder_entry.delete(0, "end")
            self.export_folder_entry.insert(0, folder)
            self.save_config()  # Save the new path

    def load_windows_json(self):
        eft_folder = self.eft_folder_entry.get()
        windows_json_path = os.path.join(eft_folder, "EscapeFromTarkov_Data", "StreamingAssets", "Windows", "windows.json")

        if not os.path.exists(windows_json_path):
            self.log("Error: windows.json not found.")
            return

        try:
            with open(windows_json_path, "r") as file:
                self.windows_data = json.load(file)
            self.populate_bundle_list()
            self.log("Loaded windows.json successfully.")
        except Exception as e:
            self.log(f"Error loading windows.json: {e}")

    def populate_bundle_list(self):
        self.bundle_listbox.delete("1.0", "end")
        for bundle in self.windows_data.keys():
            self.bundle_listbox.insert("end", f"{bundle}\n")

    def filter_bundles(self, event=None):
        search_term = self.search_entry.get().lower()
        self.bundle_listbox.delete("1.0", "end")

        for bundle in self.windows_data.keys():
            if search_term in bundle.lower():
                self.bundle_listbox.insert("end", f"{bundle}\n")

    def on_bundle_select(self, event=None):
        try:
            selected_text = self.bundle_listbox.get("sel.first", "sel.last").strip()
            if selected_text:
                self.copy_button.configure(state="normal")
            else:
                self.copy_button.configure(state="disabled")
        except Exception:
            self.copy_button.configure(state="disabled")

    def copy_selected_bundle(self):
        selected_text = self.bundle_listbox.get("sel.first", "sel.last").strip()
        if not selected_text:
            self.log("No bundle selected.")
            return

        export_folder = self.export_folder_entry.get()
        eft_folder = self.eft_folder_entry.get()

        if not export_folder or not eft_folder:
            self.log("Error: Export folder or EFT folder not selected.")
            return

        if selected_text not in self.windows_data:
            self.log("Error: Selected bundle not found in windows.json.")
            return

        dependencies = self.windows_data[selected_text]["Dependencies"]
        dependencies = [dep for dep in dependencies if dep not in BLACKLIST]
        dependencies.append(selected_text)

        for dep in dependencies:
            source_path = os.path.join(eft_folder, "EscapeFromTarkov_Data", "StreamingAssets", "Windows", dep)
            destination_path = os.path.join(export_folder, dep)

            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            try:
                shutil.copy2(source_path, destination_path)
                self.log(f"Copied: {dep}")
            except Exception as e:
                self.log(f"Failed to copy {dep}: {e}")

        self.log("Finished copying bundle and dependencies.")

if __name__ == "__main__":
    app = TarkovFileCopyTool()
    app.mainloop()
