import os
import sys
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_lactionreplacer_path():
    return os.path.join(get_base_dir(), "LActionReplacer.exe")


def run_lactions_replacer(directory, result_label):
    exe_path = get_lactionreplacer_path()

    if not os.path.exists(exe_path):
        result_label.configure(text=f"LActionReplacer.exe not found")
        return

    try:
        result = subprocess.run(
            [exe_path],
            cwd=directory,
            capture_output=True,
            text=True,
        )

        # After fixing ReadKey, should always be 0 on success
        if result.returncode == 0:
            result_label.configure(text="LActionReplacer completed successfully.")
        else:
            result_label.configure(text=f"Failed (code {result.returncode})")

    except Exception as e:
        result_label.configure(text=f"Error: {e}")


def run_lactions_replacer_thread(directory):
    t = threading.Thread(
        target=run_lactions_replacer,
        args=(directory, app.result_label),
        daemon=True,
    )
    t.start()


class LActionsReplacerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LActions Replacer")
        self.geometry("400x400")

        self.directory_entry = ctk.CTkEntry(self, width=200)
        self.directory_entry.pack(pady=30)

        browse_entry_button = ctk.CTkButton(
            self, text="Browse Directory", command=self.browse_directory
        )
        browse_entry_button.pack()

        run_button = ctk.CTkButton(
            self, text="Run Script", command=self.confirm_and_run
        )
        run_button.pack(pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:")
        self.appearance_mode_label.pack()

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.pack()
        self.appearance_mode_optionmenu.set("System")

        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:")
        self.scaling_label.pack()

        self.scaling_optionmenu = ctk.CTkOptionMenu(
            self, values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event
        )
        self.scaling_optionmenu.pack()
        self.scaling_optionmenu.set("100%")

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
            confirmation = tk.messagebox.askyesno(
                "Confirmation", "Are you sure you want to run the script?"
            )
            if confirmation:
                run_lactions_replacer_thread(directory)


if __name__ == "__main__":
    app = LActionsReplacerApp()
    app.mainloop()
