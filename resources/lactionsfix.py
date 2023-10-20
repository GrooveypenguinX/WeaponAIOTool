import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def run_lactions_replacer(directory):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(script_dir, "LActionReplacer.exe")

    try:
        subprocess.run([exe_path], cwd=directory, shell=True, check=True)
        result_label.configure(text="Execution successful.")
    except subprocess.CalledProcessError:
        result_label.configure(text="Execution failed.")

def run_lactions_replacer_thread(directory):
    t = threading.Thread(target=run_lactions_replacer, args=(directory,))
    t.start()

class LActionsReplacerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LActions Replacer")
        self.geometry("400x400")

        # Directory Entry
        self.directory_entry = ctk.CTkEntry(self, width=200)
        self.directory_entry.pack(pady=30)

        browse_entry_button = ctk.CTkButton(self, text="Browse Directory", command=self.browse_directory)
        browse_entry_button.pack()

        # Buttons
        run_button = ctk.CTkButton(self, text="Run Script", command=self.confirm_and_run)
        run_button.pack(pady=10)

        # Configure appearance mode and scaling options
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.pack()

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.pack()
        self.appearance_mode_optionmenu.set("System")  # Set default value

        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:")
        self.scaling_label.pack()

        self.scaling_optionmenu = ctk.CTkOptionMenu(self, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionmenu.pack()
        self.scaling_optionmenu.set("100%")  # Set default value

        self.selected_directory_label = ctk.CTkLabel(self, text="")
        self.selected_directory_label.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def browse_directory(self):
        directory = ctk.filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, ctk.END)
            self.directory_entry.insert(0, directory)

    def confirm_and_run(self):
        directory = self.directory_entry.get()
        if directory:
            confirmation = tk.messagebox.askyesno("Confirmation", "Are you sure you want to run the script?")
            if confirmation:
                run_lactions_replacer_thread(directory)

if __name__ == "__main__":
    app = LActionsReplacerApp()
    app.mainloop()
