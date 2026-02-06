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

import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

avatar_masks = []
bone_map = {}

def browse_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_widget.delete(0, 'end')
    entry_widget.insert(0, file_path)

def log_message(text):
    log_text.insert(ctk.END, text + '\n')
    log_text.see(ctk.END)  # Auto-scroll to the end of the text
def parse_avatar_bone_mapping(avatar_data):
    bone_map = {}
    in_avatar_mask = False
    inside_map_TOS = []

    for line in avatar_data.split('\n'):
        if line.strip() == "map m_TOS":
            in_avatar_mask = True
        elif in_avatar_mask:
            inside_map_TOS.append(line)
            if line.strip() == "}":
                in_avatar_mask = False

    for i, line in enumerate(inside_map_TOS):
        if "pair data" in line:
            number_line = inside_map_TOS[i + 1]
            name_line = inside_map_TOS[i + 2]
            number = int(number_line.split('=')[1].strip())
            bone_name = name_line.split('=')[1].strip().strip('" ')
            bone_map[number] = bone_name

    return bone_map

def parse_animator_controller(controller_data):
    avatar_masks = []
    parsing_body_mask = False
    parsing_skeleton_mask = False

    for line in controller_data.split('\n'):
        if parsing_body_mask:
            if "word0" in line:
                word0 = int(line.split('=')[1].strip())
            elif "word1" in line:
                word1 = int(line.split('=')[1].strip())
            elif "word2" in line:
                word2 = int(line.split('=')[1].strip())
                parsing_body_mask = False
                avatar_masks.append((word0, word1, word2, True))
        if parsing_skeleton_mask:
            if "unsigned int m_PathHash" in line:
                bone_number = int(line.split('=')[1].strip())
            elif "float m_Weight" in line:
                weight = float(line.split('=')[1].strip())
                avatar_masks.append((bone_number, weight))
        if "HumanPoseMask m_BodyMask" in line:
            parsing_body_mask = True
        if "SkeletonMask data" in line:
            parsing_skeleton_mask = True

    return avatar_masks

def generate_avatar_mask_list(bone_map, avatar_masks):
    avatar_mask_list = []

    for mask in avatar_masks:
        if len(mask) == 4:
            word0, word1, word2, enabled = mask
            avatar_mask = {
                "Word0": word0,
                "Word1": word1,
                "Word2": word2,
                "Enabled": enabled
            }
        else:
            bone_number, weight = mask
            bone_name = bone_map.get(bone_number, f"Bone {bone_number}")
            avatar_mask = {
                "Bone Name": bone_name,
                "Enabled": "Enabled" if weight > 0 else "Disabled"
            }
        avatar_mask_list.append(avatar_mask)

    return avatar_mask_list

def generate_and_dump_avatar_mask_list():
    global bone_map, avatar_masks

    if bone_map and avatar_masks:
        avatar_mask_list = []

        for mask in avatar_masks:
            if len(mask) == 4:
                word0, word1, word2, enabled = mask
                avatar_mask = {
                    "Word0": word0,
                    "Word1": word1,
                    "Word2": word2,
                    "Enabled": enabled
                }
                avatar_mask_list.append(avatar_mask)
            else:
                bone_number, weight = mask
                bone_name = bone_map.get(bone_number, f"Bone {bone_number}")
                avatar_mask = {
                    "Bone Name": bone_name,
                    "Enabled": "Enabled" if weight > 0 else "Disabled"
                }
                avatar_mask_list.append(avatar_mask)

        # Ask the user for the destination directory and file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="avatar_mask_list.txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if file_path:
            with open(file_path, "w") as dump_file:
                for mask in avatar_mask_list:
                    if "Bone Name" in mask:
                        dump_file.write(f"Bone Name: {mask['Bone Name']}, Enabled: {mask.get('Enabled', 'N/A')}\n")
                    else:
                        dump_file.write(f"Word0: {mask['Word0']}, Word1: {mask['Word1']}, Word2: {mask['Word2']}, Enabled: {mask.get('Enabled', 'N/A')}\n")

            log_message(f"Avatar mask list generated and dumped to {file_path}")


def process_dumps_and_generate_avatar_mask_list():
    global bone_map, avatar_masks

    avatar_file_path = avatar_file_entry.get()
    if not avatar_file_path:
        log_message("Please select an Avatar Dump file.")
        return

    try:
        with open(avatar_file_path, 'r') as file:
            avatar_data = file.read()
            bone_map = parse_avatar_bone_mapping(avatar_data)
            log_message("Avatar dump file processed successfully.")
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        log_message(error_message)
        return

    controller_file_path = controller_file_entry.get()
    if not controller_file_path:
        log_message("Please select an Animator Controller Dump file.")
        return

    try:
        with open(controller_file_path, 'r') as file:
            controller_data = file.read()
            avatar_masks = parse_animator_controller(controller_data)
            log_message("Animator Controller data processed successfully")
    except Exception as e:
        error_message = "An error occurred: " + str(e)
        log_message(error_message)
        return

    generate_and_dump_avatar_mask_list()
    log_message("Avatar Mask List generated and dumped to avatar_mask_list.txt.")

app = ctk.CTk()

main_frame = ctk.CTkFrame(app)
main_frame.grid(row=0, column=0, sticky=(ctk.N, ctk.W, ctk.E, ctk.S))

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

avatar_file_label = ctk.CTkLabel(main_frame, text="Select Avatar Dump:")
avatar_file_label.grid(row=0, column=0, sticky=ctk.W, padx=10, pady=5)

avatar_file_entry = ctk.CTkEntry(main_frame, width=240)
avatar_file_entry.grid(row=0, column=1, padx=10, pady=5)

avatar_file_browse_button = ctk.CTkButton(main_frame, text="Search", command=lambda: browse_file(avatar_file_entry))
avatar_file_browse_button.grid(row=0, column=2, padx=10, pady=5)

controller_file_label = ctk.CTkLabel(main_frame, text="Select Animator Controller Dump:")
controller_file_label.grid(row=1, column=0, sticky=ctk.W, padx=10, pady=5)

controller_file_entry = ctk.CTkEntry(main_frame, width=240)
controller_file_entry.grid(row=1, column=1, padx=10, pady=5)

controller_file_browse_button = ctk.CTkButton(main_frame, text="Search", command=lambda: browse_file(controller_file_entry))
controller_file_browse_button.grid(row=1, column=2, padx=10, pady=5)

process_button = ctk.CTkButton(main_frame, text="Process Dumps and generate Avatar Mask List", command=process_dumps_and_generate_avatar_mask_list)
process_button.grid(row=2, column=0, columnspan=3, pady=10)

log_text = ctk.CTkTextbox(main_frame, width=580, height=235, wrap="none")
log_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()