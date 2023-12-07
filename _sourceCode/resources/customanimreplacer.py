import os
import re
import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import logging

# Define the regex pattern for the broken animation GUID
guid_pattern = re.compile(r'guid: (\w+)')

class AnimatorControllerFixApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Animator Controller Fix Tool")
        self.geometry("800x400")

        self.create_widgets()

    def create_widgets(self):
        # Frame for left and right sections
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True)
        right_frame = ctk.CTkFrame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        # Variables to store file paths and statistics
        self.animator_controller_var = tk.StringVar()
        self.old_animations_var = tk.StringVar()
        self.new_animations_var = tk.StringVar()
        self.total_replaced = 0
        self.total_errors = 0

        # Function to open a file dialog and set the selected path to a variable
        def select_file(var):
            file_path = ctk.filedialog.askopenfilename()
            if file_path:
                var.set(file_path)

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

        # Function to process the Animator Controller
        def process_animator_controller():
            self.total_replaced = 0
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

            update_log("Processing Animator Controller...\n")

            # Validate selected files
            if not os.path.exists(self.animator_controller_var.get()):
                update_log("Error: Animator Controller file does not exist.", log_level=logging.ERROR)
                return

            if not os.path.exists(self.old_animations_var.get()):
                update_log("Error: Old Animations Folder does not exist.", log_level=logging.ERROR)
                return

            if not os.path.exists(self.new_animations_var.get()):
                update_log("Error: New Animations Folder does not exist.", log_level=logging.ERROR)
                return

            # Step 1: Extract old animation GUIDs
            update_log("Extracting old animation GUIDs...\n")
            old_animation_guids = {}
            for root, _, files in os.walk(self.old_animations_var.get()):
                for file in files:
                    if file.endswith(".meta"):
                        animation_clip_guid = extract_guid_from_meta(os.path.join(root, file))
                        if animation_clip_guid:
                            old_animation_guids[animation_clip_guid] = animation_clip_guid

            # Step 2: Extract new animation GUIDs
            update_log("Extracting new animation GUIDs...\n")
            new_animation_guids = {}
            for root, _, files in os.walk(self.new_animations_var.get()):
                for file in files:
                    if file.endswith(".meta"):
                        animation_clip_guid = extract_guid_from_meta(os.path.join(root, file))
                        if animation_clip_guid:
                            new_animation_guids[animation_clip_guid] = animation_clip_guid

            # Step 3: Read the Animator Controller file
            update_log("Processing Animator Controller...\n")
            animator_controller_file = self.animator_controller_var.get()
            with open(animator_controller_file, 'r', encoding='utf-8') as controller_file:
                controller_data = controller_file.read()

            # Step 4: Replace old animation GUIDs with new animation GUIDs
            for old_guid, new_guid in zip(old_animation_guids, new_animation_guids):
                if old_guid in controller_data:
                    controller_data = controller_data.replace(old_guid, new_guid)
                    self.total_replaced += 1

            # Step 5: Write the updated data back to the Animator Controller file
            with open(animator_controller_file, 'w', encoding='utf-8') as controller_file:
                controller_file.write(controller_data)

            update_log("Animator Controller processing completed.\n")
            update_log(f"GUIDs replaced: {self.total_replaced}\n")
            update_log(f"Total errors encountered: {self.total_errors}\n")

        # Left Section: Input
        input_frame = ctk.CTkFrame(left_frame)
        input_frame.pack(padx=10, pady=10, fill="both")

        # Animator Controller File
        ctk.CTkLabel(input_frame, text="Animator Controller File").grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.animator_controller_var, width=250).grid(row=0, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_file(self.animator_controller_var)).grid(row=0, column=2)

        # Old Animations Folder
        ctk.CTkLabel(input_frame, text="Old Animations Folder").grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.old_animations_var, width=250).grid(row=1, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_directory(self.old_animations_var)).grid(row=1, column=2)

        # New Animations Folder
        ctk.CTkLabel(input_frame, text="New Animations Folder").grid(row=2, column=0, padx=10, pady=5)
        ctk.CTkEntry(input_frame, textvariable=self.new_animations_var, width=250).grid(row=2, column=1)
        ctk.CTkButton(input_frame, text="Browse", command=lambda: select_directory(self.new_animations_var)).grid(row=2, column=2)

        # Right Section: Output
        log_text = ctk.CTkTextbox(right_frame, wrap=ctk.WORD, height=20, width=400, state="disabled")
        log_text.pack(padx=10, pady=10, fill="both", expand="yes")

        process_button = ctk.CTkButton(left_frame, text="Process Animator Controller", command=process_animator_controller)
        process_button.pack(padx=10, pady=5)

if __name__ == "__main__":
    app = AnimatorControllerFixApp()
    app.mainloop()
