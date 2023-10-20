import os
import customtkinter as ctk
from tkinter import filedialog
import shutil
import json

# Define the blacklist of files to exclude
blacklist = [
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
    "assets.content/weapons/additional_hands/client_assets.bundle"
]

class TarkovFileCopyTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tarkov File Copy Tool")
        self.geometry("1000x800")

        # Left Frame (JSON Section and Directory Entries)
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True)

        # JSON Section Label
        json_label = ctk.CTkLabel(left_frame, text="Paste JSON Section:")
        json_label.pack()

        # JSON Entry
        self.json_entry = ctk.CTkTextbox(left_frame, height=200, width=350)
        self.json_entry.pack(fill="both", expand=True, padx=(20, 0), pady=(20, 20))

        # Tarkov Data 'Windows' folder
        assets_folder_label = ctk.CTkLabel(left_frame, text="Please select \n EscapefromTarkov_Data\StreamingAssets\Windows\n directory:")
        assets_folder_label.pack(padx=(5, 5), pady=(5, 5))
        self.assets_folder_entry = ctk.CTkEntry(left_frame, width=250)
        self.assets_folder_entry.pack(padx=(5, 5), pady=(5, 5))

        # Browse for Tarkov Data 'Windows' folder
        assets_folder_button = ctk.CTkButton(left_frame, text="Browse", command=self.browse_assets_directory)
        assets_folder_button.pack(padx=(5, 5), pady=(5, 5))

        # Export Folder Label
        export_folder_label = ctk.CTkLabel(left_frame, text="Select Export Folder:")
        export_folder_label.pack(padx=(5, 5), pady=(5, 5))
        self.export_folder_entry = ctk.CTkEntry(left_frame, width=250)
        self.export_folder_entry.pack(padx=(5, 5), pady=(5, 5))

        # Browse for Export Folder
        export_folder_button = ctk.CTkButton(left_frame, text="Browse", command=self.browse_export_directory)
        export_folder_button.pack(padx=(5, 5), pady=(5, 5))

        # Result Label
        self.result_label = ctk.CTkLabel(left_frame, text="")
        self.result_label.pack()

        # Copy Tarkov Files Button
        copy_button = ctk.CTkButton(left_frame, text="Grab Tarkov Files", command=self.copy_tarkov_files)
        copy_button.pack()

        # Right Frame (Logging Text)
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        # Logging Text
        self.logging_text = ctk.CTkTextbox(right_frame, height=200, width=350, state="disabled", padx=10, pady=10)
        self.logging_text.pack(fill="both", expand=True, padx=(20, 20), pady=(20, 20))

        # Frame for Appearance and Scaling Options
        options_frame = ctk.CTkFrame(left_frame)
        options_frame.pack(side="bottom", fill="x", expand=True)

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

    def browse_assets_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.assets_folder_entry.delete(0, ctk.END)
        self.assets_folder_entry.insert(0, directory)

    def browse_export_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.export_folder_entry.delete(0, ctk.END)
        self.export_folder_entry.insert(0, directory)

    def copy_tarkov_files(self):
        data = self.json_entry.get("0.0", ctk.END)
        assets_folder = self.assets_folder_entry.get()
        export_folder = self.export_folder_entry.get()

        self.logging_text.configure(state="normal")
        self.logging_text.delete("0.0", ctk.END)

        try:
            data = json.loads(data)

            for container_name, container_data in data.items():
                dependencies = [dep for dep in container_data["Dependencies"] if dep not in blacklist]

                # Add the main container to dependencies if not already present
                if container_name not in dependencies:
                    dependencies.append(container_name)

                for dep in dependencies:
                    source_dep_path = os.path.join(assets_folder, dep)
                    destination_dep_path = os.path.join(export_folder, dep)

                    # Handle files with the same name
                    while os.path.exists(destination_dep_path):
                        base, ext = os.path.splitext(destination_dep_path)
                        destination_dep_path = f"{base}_copy{ext}"

                    os.makedirs(os.path.dirname(destination_dep_path), exist_ok=True)
                    shutil.copy2(source_dep_path, destination_dep_path)

                    self.logging_text.insert(ctk.END, f"Copied: {dep}\n")

            self.logging_text.insert(ctk.END, "Files copied successfully!\n")
        except Exception as e:
            self.logging_text.insert(ctk.END, f"Error: {str(e)}\n")

        self.logging_text.configure(state="disabled")

if __name__ == "__main__":
    app = TarkovFileCopyTool()
    app.mainloop()
