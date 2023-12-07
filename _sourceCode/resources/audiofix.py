import os
import customtkinter as ctk
import tkinter.messagebox
import shutil

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TarkovAudioFixer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tarkov Audio Fixer")
        self.geometry("800x600")  # Adjusted the width to accommodate the layout

        # Left Side (Buttons and Directory Selection)
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True)

        main_assets_label = ctk.CTkLabel(left_frame, text="Select Main Assets Folder:")
        main_assets_label.pack(pady=(10, 0))

        self.main_assets_var = ctk.StringVar()
        main_assets_entry = ctk.CTkEntry(left_frame, textvariable=self.main_assets_var, width=200)
        main_assets_entry.pack(pady=5)

        main_assets_button = ctk.CTkButton(left_frame, text="Select Main Assets Folder", command=lambda: self.browse_folder("Main Assets"))
        main_assets_button.pack(pady=(0, 10))

        working_audio_label = ctk.CTkLabel(left_frame, text="Select Working Audio Folder:")
        working_audio_label.pack(pady=(10, 0))

        self.working_audio_var = ctk.StringVar()
        working_audio_entry = ctk.CTkEntry(left_frame, textvariable=self.working_audio_var, width=200)
        working_audio_entry.pack(pady=5)

        working_audio_button = ctk.CTkButton(left_frame, text="Select Working Audio Folder", command=lambda: self.browse_folder("Working Audio"))
        working_audio_button.pack(pady=(0, 10))

        fix_audio_button = ctk.CTkButton(left_frame, text="Fix Tarkov Audio", command=self.fix_tarkov_audio)
        fix_audio_button.pack(pady=(10, 5))

        # Create appearance mode option
        self.appearance_mode_label = ctk.CTkLabel(left_frame, text="Appearance Mode:")
        self.appearance_mode_label.pack(pady=(90, 0))

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(left_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.pack()

        self.appearance_mode_optionmenu.set("System")  # Set default value

        # Create UI scaling option
        self.scaling_label = ctk.CTkLabel(left_frame, text="UI Scaling:")
        self.scaling_label.pack(pady=10)

        self.scaling_optionmenu = ctk.CTkOptionMenu(left_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionmenu.pack()

        self.scaling_optionmenu.set("100%")  # Set default value

        # Right Side (Logging Textbox)
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="left", fill="both", expand=True)

        self.log_text = ctk.CTkTextbox(right_frame, height=550, width=450, state="normal")  # Set state to "normal"
        self.log_text.pack(fill='both', expand=True, padx=(10, 10), pady=(10, 10))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def browse_folder(self, button):
        folder_path = ctk.filedialog.askdirectory()
        if folder_path:
            if button == "Main Assets":
                self.main_assets_var.set(folder_path)
            elif button == "Working Audio":
                self.working_audio_var.set(folder_path)

    def log_message(self, message):
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.update()  # Update the widget to display the inserted message

    def fix_tarkov_audio(self):
        main_assets_folder = self.main_assets_var.get()
        working_audio_folder = self.working_audio_var.get()

        # Check if both folders are selected
        if not main_assets_folder or not working_audio_folder:
            self.log_message("Please select both Main Assets and Working Audio folders.")
            return

        # Collect working audio file names and extensions
        working_audio_files = {}
        for root, _, files in os.walk(working_audio_folder):
            for file in files:
                if file.lower().endswith('.wav'):
                    audio_name, _ = os.path.splitext(file)
                    working_audio_files[audio_name.lower()] = os.path.join(root, file)

        # Iterate through main assets and update audio files and .meta files
        log = ""
        for root, _, files in os.walk(main_assets_folder):
            for file in files:
                if file.lower().endswith('.ogg') or file.lower().endswith('.wav'):  # Process .ogg and .wav audio files
                    audio_name, audio_ext = os.path.splitext(file)
                    audio_name_lower = audio_name.lower()
                    if audio_name_lower in working_audio_files:
                        working_audio_path = working_audio_files[audio_name_lower]
                        main_assets_path = os.path.join(root, file)

                        # Check if the extension is different
                        if audio_ext != '.wav':
                            main_assets_meta_path = main_assets_path + '.meta'

                            # Copy the working audio and rename it
                            shutil.copy2(working_audio_path, main_assets_path)
                            os.rename(main_assets_path, main_assets_path.replace(audio_ext, '.wav'))

                            # Update the .meta file extension
                            if os.path.exists(main_assets_meta_path):
                                os.rename(main_assets_meta_path, main_assets_meta_path.replace(audio_ext, '.wav.meta'))

                            log += f"Updated: {file} and {file}.meta\n"
                        else:
                            # Extension is the same, just copy the audio
                            shutil.copy2(working_audio_path, main_assets_path)
                            log += f"Updated: {file}\n"
                    else:
                        # No match found, log it
                        log += f"No match found for: {file}\n"

        self.log_message(log)

if __name__ == "__main__":
    app = TarkovAudioFixer()
    app.mainloop()
