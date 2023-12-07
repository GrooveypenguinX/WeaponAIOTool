import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AnimationRenamerReplacer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Animation Renamer and Replacer")
        self.geometry("900x600")  # Adjusted the width to accommodate the layout

        # Left Side (Buttons and Directory Selection)
        left_frame = ctk.CTkFrame(self)
        left_frame.pack(side="left", fill="both", expand=True)

        working_directory_label = ctk.CTkLabel(left_frame, text="Select Working Animations Directory:")
        working_directory_label.pack(pady=(10, 0))

        self.working_directory_var = ctk.StringVar()
        working_directory_entry = ctk.CTkEntry(left_frame, textvariable=self.working_directory_var, width=150)
        working_directory_entry.pack(pady=5)

        working_directory_button = ctk.CTkButton(left_frame, text="Browse", command=self.select_working_directory)
        working_directory_button.pack(pady=(0, 10))

        broken_directory_label = ctk.CTkLabel(left_frame, text="Select 'Broken' Exported Animations Directory:")
        broken_directory_label.pack(pady=(10, 0))

        self.broken_directory_var = ctk.StringVar()
        broken_directory_entry = ctk.CTkEntry(left_frame, textvariable=self.broken_directory_var, width=150)
        broken_directory_entry.pack(pady=5)

        broken_directory_button = ctk.CTkButton(left_frame, text="Browse", command=self.select_broken_directory)
        broken_directory_button.pack(pady=(0, 10))

        rename_button = ctk.CTkButton(left_frame, text="Rename Animations", command=self.rename_animations)
        rename_button.pack(pady=(10, 5))

        compare_button = ctk.CTkButton(left_frame, text="Compare Directories", command=self.compare_directories)
        compare_button.pack(pady=5)

        replace_button = ctk.CTkButton(left_frame, text="Replace Broken Animations", command=self.replace_animations)
        replace_button.pack(pady=(5, 10))

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


        
    def log_message(self, message):
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.update()  # Update the widget to display the inserted message

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


    def select_working_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.working_directory_var.set(directory)

    def select_broken_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.broken_directory_var.set(directory)

    def rename_animations(self):
        working_directory = self.working_directory_var.get()
        try:
            if not os.path.exists(working_directory):
                tk.messagebox.showerror("Directory Not Found", "The selected working directory does not exist.")
                return

            for root, _, files in os.walk(working_directory):
                for file in files:
                    if file.endswith(('.anim', '.anim.meta')):
                        new_filename = file.replace("Armature_", "").replace("_Base Layer", "")
                        old_path = os.path.join(root, file)
                        new_path = os.path.join(root, new_filename)
                        os.rename(old_path, new_path)
                        self.log_text.insert(ctk.END, f"Renamed '{file}' to '{new_filename}'\n")

            tk.messagebox.showinfo("Renaming Completed", "Animations have been successfully renamed.")
        except Exception as e:
            self.log_text.insert(ctk.END, f"Error: {str(e)}\n")
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def compare_directories(self):
        working_directory = self.working_directory_var.get()
        broken_directory = self.broken_directory_var.get()
        try:
            if not os.path.exists(working_directory) or not os.path.exists(broken_directory):
                tk.messagebox.showerror("Directory Not Found", "The selected directories do not exist.")
                return

            working_animations = set(os.listdir(working_directory))
            broken_animations = set(os.listdir(broken_directory))

            missing_in_broken = working_animations - broken_animations
            missing_in_working = broken_animations - working_animations

            for animation in missing_in_broken:
                self.log_text.insert(ctk.END, f"Animation '{animation}' missing in broken folder\n")

            for animation in missing_in_working:
                self.log_text.insert(ctk.END, f"Animation '{animation}' missing in working folder\n")

            tk.messagebox.showinfo("Comparison Completed", "Directory comparison is complete.")
        except Exception as e:
            self.log_text.insert(ctk.END, f"Error: {str(e)}\n")
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def replace_animations(self):
        working_directory = self.working_directory_var.get()
        broken_directory = self.broken_directory_var.get()
        try:
            if not os.path.exists(working_directory) or not os.path.exists(broken_directory):
                tk.messagebox.showerror("Directory Not Found", "The selected directories do not exist.")
                return

            for root, _, files in os.walk(working_directory):
                for file in files:
                    if file.endswith('.anim'):
                        working_path = os.path.join(root, file)
                        broken_path = os.path.join(broken_directory, file)
                        os.replace(working_path, broken_path)
                        self.log_text.insert(ctk.END, f"Replaced '{file}'\n")

            tk.messagebox.showinfo("Replacement Completed", "Animations have been successfully replaced in the broken directory.")
        except Exception as e:
            self.log_text.insert(ctk.END, f"Error: {str(e)}\n")
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = AnimationRenamerReplacer()
    app.mainloop()
