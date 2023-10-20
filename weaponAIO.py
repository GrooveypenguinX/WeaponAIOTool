import tkinter
from tkinter import messagebox
import customtkinter as ctk
import subprocess

# Set the appearance mode and default color theme using customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Create the main application class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WeaponAIOTool")
        self.geometry("1350x750")

        # Configure grid weights for resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=75)
        self.grid_rowconfigure(0, weight=1)

        # Create the sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(0, weight=1)
        self.step_buttons = []  # Define step_buttons list at the class level
        # Define the steps (instructions) for the tool
        self.steps = {
"Main Menu": """
Welcome to Tarkov Presents: The Weapon AIO Tool!

The WTT Team proudly presents our all-in-one tool/tutorial for Escape From Tarkov advanced weapon modding! Follow our step-by-step instructions to effortlessly streamline your weapon creation workflow. This guide aims to cover almost every process, from Asset Ripper, to AssetStudioGui, to Unity, and finally to Tarkov! From weapon ripping to final testing, we've got you covered.
To follow along with this guide, you will need the following:
    - Unity 2019.4.39f1
    - Escape From Tarkov SDK
    - Asset Ripper
    - Blender
    - Asset Studio GUI
    - Your choice of text editor that has formatting for .json (VSCode, VSCodium, etc)
    - .NET Framework for LActionReplacer.exe


This tool owes a big debt of gratitude to the fantastic minds of SamSwat, SSH, and Choccy, for providing the tools, info, and knowhow to help navigate this process. Special recognition to WTT's Tron, who helped hold onto my last remaining shreds of sanity while we ventured through this process.
Now, best of luck! This process is about as straightforward as herding caffeinated cats, but fear not! This guide's here to try and make your modding mayhem a tad more manageable.

            - Crafted with questionable sanity by GrooveypenguinX
""",
"Step 1: Copy Dependencies": """
                                                            **Description:**
In this step, you'll copy the weapon you are basing your custom weapon off of, and all it's dependencies from Escape From Tarkov's game files to your specified directory.
                                                            **Instructions:**
1. Locate the 'windows.json' file in EFT's game files (EscapeFromTarkov_Data\StreamingAssets\Windows).
2. Open the 'windows.json' file in your preferred text editor (VSCode, VSCodium, etc.) and format the code.
3. Find your desired weapon container and its dependencies in the windows.json.
4. Copy the entire section from the 'windows.json' and format it as a valid JSON section (remove trailing commas, surround it in curly brackets).
5. Run the attached 'filegrabber' script. Paste the JSON section into the script's input box.
6. Specify your source directory where EFT's game files are located (EscapeFromTarkov_Data\StreamingAssets\Windows), and the destination directory where you want to copy these files.
7. Click the 'Grab Tarkov Files' button to initiate the copying process.
""",
"Step 2: Convert Bundles": """
                                                            **Description:** 
In this step, you'll convert bundles to Unity format using Asset Ripper.
                                                            **Instructions:**
1. Drag the entire exported folders from Step 1 into Asset Ripper.
2. Export all assets to your specified export directory.
""",
"Step 3: Fix GUID References": """
                                                            **Description:** 
In this step, you'll fix all script GUID references to ensure your Unity project uses the correct SDK scripts.
                                                            **Instructions:**
1. Run the provided 'scriptfix' script to update script GUID references in your project.
2. Fill in the required inputs within the script's GUI:
- Main Asset folder: The "assets" directory of your weapon you exported from Asset Ripper in Step 2.
- Broken Scripts folder: The 'Scripts/AssemblyCSharp' folder inside the weapon you exported from Asset Ripper in Step 2.
- Working Scripts folder: The 'Scripts' folder inside the Escape From Tarkov SDK.
3. After successfully patching the GUIDs with 'scriptfix', delete the "Scripts" folder from your exported weapon project, as it's no longer needed and may cause Unity errors.
""",
"Step 4: Import to Unity": """
                                                            **Description:** 
In this step, you'll import your exported weapon into Unity.
                                                            **Instructions:**
1. Rename the main 'Assets' folder from the weapon you exported from AssetRipper in Step 2 to match the name of the item you're working on.
2. Import the Folder into Unity while preserving the folder structure and organization.
""",
"Step 5: Handling Audio": """
                                                            **Description:** 
In this step, you'll handle all audio assets, fixing any broken audio files caused by Asset Ripper.
                                                            **Instructions:**
1. Open the export folder containing the weapon container .bundle and dependencies from Step 1.
2. Export all AudioClip files from every file using Asset Studio GUI. NOTE: not every file is a .bundle. There is a 'generic' file with no extension that contains lots of shared audio.
3. Create a new folder, and place all the 'working audio' files in the same folder.
4. Run the provided 'audiofix' script to identify all the working and broken audio files and automatically replace the broken files while updating their .meta extension (if necessary).
5. Go through all your audio bank files (typically located in Assets/Content/Weapons/Audio/). Under Blend Options, replace the missing field with the SDK's 'Standart' DistanceBlendOption. (yes, 'Standart'. Not a typo.)
""",
"Step 6: Fixing Animations Part 1 (AssetStudioGUI)": """
                                                            **Description:** 
In this step, you'll export working animations from AssetStudioGUI for use in the next step.
                                                            **Instructions:**
1. Open the export folder containing the weapon container .bundle and dependencies from Step 1.
2. Import the 'client_assets.bundle' for the weapon container you are working on into AssetStudioGui.
3. In the 'Options' menu, ensure 'Display all assets' is checked.
4. In the 'Filter Type' menu, select 'Animator', 'AnimationClip', and 'Avatar'.
5. Find the avatar with the largest 'int size' in the list. This is USUALLY the correct avatar for exporting proper animations.
6. Select all the AnimationClips, the Avatar, and the matching Animator. Right-click and choose 'Export Animator + selected Animations'.
""",
"Step 7: Fixing Animations Part 2 (Blender)": """
                                                            **Description:** 
In this step, you'll fix animations in Blender, resetting scale, origin, and cleaning up extra bones from AssetStudioGUI.
                                                            **Instructions:**
1. Import the FBX file into Blender you just created in Step 6.
2. Reset the scale by pressing Alt + S. This will set the scale to 1.
3. In Pose Mode, select the main bone in the armature, which is usually standing up vertically and named the same name as the weapon you exported.
4. Set the 3D cursor to the main bone in the armature using Shift + S > 'Cursor to Selected'.
5. In Object Mode, select the armature and set the origin to the 3D cursor using 'Object' > 'Origin' > 'Set Origin to 3D Cursor'.
6. In Edit Mode, delete the main bone in the armature as it's not needed and may cause issues.
7. In Object Mode, select ONLY the armature and reset all transforms using Alt + G. This will move the armature to the origin near 0 0 0.
8. I recommend you make a backup of this file named WORKINGANIMATIONS_(yourweapon).blend, or something similar in case you need to go back to re-do animations or mesh edits.
9. Customize this mesh in Blender to create your new custom gun. Be sure to pair the meshes to the proper bones in the armature.
10. Save and export the new FBX into Unity with proper export settings. Ensure that 'Transform' > 'Apply Scaling' is set to 'FBX All,' and 'Armature' > 'Add Leaf Bones' is unchecked.
""",
"Step 8: Fixing Animations Part 3 (Unity)": """
                                                            **Description:** 
In this step, you'll fix the weapon's animations in Unity, replacing the broken ones from Asset Ripper with your working ones from Step 7.
                                                            **Instructions:**
1. In Unity, locate your exported Tarkov weapon you imported in Step 4.
2. Find the folder containing the weapon container, the controller, and .anim files. All the .anim files are currently broken from Asset Ripper.
3. Create a new folder in Unity, and move all the 'broken' .anim files for your exported weapon to the new folder, and name it accordingly.
4. NOTE: If you move these animations in Windows Explorer, also move their .meta files.
5. If not already done, import the Working Animations FBX file from Step 7 into Unity.
6. Select the working animations FBX file in Unity and under 'Inspector' > 'Rig' > 'Avatar Definition,' toggle it to 'Create from this model' and click 'Apply'.
7. Duplicate all the working animations outside the FBX file by selecting all the animations in Unity (toggle open the .fbx with the arrow) and use CTRL + D to duplicate them into .anim files.
8. Create a new folder in Unity, move all the new 'working' animation .anim files to the new folder and name it accordingly.
9. NOTE: If you move these animations in Windows Explorer, also move their .meta files.
10. Run the provided 'animrenamereplace' script, which helps automatically rename the working .anim files, compare the two directories for discrepancies, and replace the animations.
11. The 'animrenamereplace' script renames animations from their exported blender names, and replaces 'broken' animations with working ones while retaining original .meta files. This keeps all the animations intact in the animator controller.
""",
"Step 9: Left Hand Animations": """
                                                            **Description:** 
In this step, you'll update the left-hand animations in your Animator Controller with the SDK's animations using SamSWAT's LActionReplacer.
                                                            **Instructions:**
1. Use the attached 'lactionsfix' script to replace left-hand animations in your Animator Controller with the correct animations.
2. Click the 'Browse Directory' button to select the directory where your Animator Controller is located.
3. Once the directory is selected, click 'Run Script' to execute the replacement process.
4. The 'lactionsfix' script automates the replacement of left-hand animations in your Animator Controller, ensuring that the correct animations are applied.

Shoutout to SamSwat for the LActionReplacer.exe that this script uses.
""",
"Step 10: Avatar Masks for Animator Controller Layers": """
                                                            **Description:** 
In this step, you'll create avatar masks for each specific animation layer. This is a very complex process, and will differ weapon to weapon.
                                                            **Instructions:**
1. In Unity, locate the .fbx file of your model with animations and select it.
2. In the 'Inspector' window, navigate to the 'Rig' tab.
3. In the 'Avatar Definition' section, select 'Create From This Model' and click 'Apply'.
4. With the avatar generated, right-click in the 'Project' window and select 'Create' > 'Avatar Mask' to create a new avatar mask.
5. Select the newly created avatar mask in the 'Project' window.
6. In the 'Inspector' window, under 'Transform' > 'Use Skeleton From,' drag your generated avatar from your .fbx model to the entry, and click 'Import Skeleton'.
7. Duplicate this avatar mask to create separate masks for different animation layers. Use CTRL + D to duplicate the avatar mask.
8. Customize each avatar mask for different animation layers: 'Base Layer' requires no Avatar Mask, 'Hands' requires all bones selected, 'LActions' can use the Left_hand_actions Avatar Mask included with the SDK, and each of the other layers must be customized on a case-by-case basis. Each avatar mask is customized by selecting or deselecting the bones in the list to control their influence on animations.
""",
"Step 11: Creating your custom weapon Prefab": """
                                                            **Description:** 
In this step, you'll create a custom weapon prefab in Unity. This is your actual custom model that will be used in the game.
                                                            **Instructions:**
1. Select your custom weapon 'working animations' .fbx file you created in Step 7. Drag it onto the Scene, right click it, and Unpack Prefab Completely.
2. Select the Tarkov weapon model.generated and drag it onto the Scene.
3. Compare the two models and take note of the scripts that are attached to the Tarkov gameobjects.
4. The main game object should have Transform Links LOD Groups and Animator. The weapon_root children will have different types of scripts attached. These need to be compared gameobject-by-gameobject, and added to their match in your custom prefab.
    - NOTE: Muzzle Fume is broken from Asset Ripper. Fortunately, there is a example in the SDK you can compare and copy the values from (thanks SamSWWAT!).
5. Provided is a 'AutoTransformLinks.cs' editor script for Unity (located in the Tools folder of this program) that will automatically apply the transform links to your custom prefab.
6. To use, place the AutoTransformLinks.cs in your SDK Assets/Editor folder.
7. Select 'Tarkov Weapon Tools' from your toolbar, and select 'Transform Links Automation' to open it's GUI.
8. In the GUI, drag your custom prefab into the Main Gameobject entry, and click 'Apply Transform Links'.
9. Once all game objects have the correct scripts attached, drag your custom weapon prefab to the Project window. Rename the .prefab to your cusotm weapon name.
10. Select the main Weapon Container you imported in Step 4. Clear every entry in 'Weapon Prefab' except for Weapon Object and Original Animator Controller.
11. Select your new custom weapon prefab you just made and apply it over the Weapon Object entry in your main Weapon Container > Weapon Prefab.
""",
"Step 12: Building your Custom Weapon Bundle": """
                                                            **Description:** 
In this step, you'll clear the asset labels and build your custom weapon bundle.
                                                            **Instructions:**
1. All the imported Tarkov gameobjects retain their original asset labels from Tarkov (i.e. Assets/Content/Weapons/rhino/client_assets.bundle). 
2. There are two ways to clear the assetlabels. You can select every imported gameobject and set the Asset Label to 'None'. OR you can clear all the labels in the AssetBundleBrowser configure window, but be CAREFUL to not delete any of the SDK bundle labels, such as Shaders or Additional Hands, as these HAVE to be built in order for the PathID replacer to work.
3. Apply a new label to the main weapon container. This will be the name of the custom weapon bundle you are building for the game.
4. Build your new custom gun in the AssetBundleBrowser 'Build' tab, and continue on to test your weapon in the game using custom code to add it.

Congratulations! You have now built your custom gun! If everything went correctly, you should be able to add it using a server mod, and test it in the game!
""",
"Step 13: Final Notes - Errors and Making Edits": """

If your gun does not properly animate, the odds are it is an issue with one, or multiple Avatar Masks. You can edit these Avatar Masks, and rebuild the gun to further test your weapon.

If you need to make further adjustments to the mesh, you will need to do the following:
    1. Go back to the Working Animations .fbx file we used to make the Weapon Prefab in Step 11.
    2. Open the .fbx file in blender, and make your edits to the mesh
    3. Once your edits have been made, export the FBX file back into Unity. Ensure that 'Transform' > 'Apply Scaling' is set to 'FBX All,' and 'Armature' > 'Add Leaf Bones' is unchecked.
        - IF you made edits to bone locations, you will need to repeat the .anim replacement detailed in Step 8.
        - IF you added meshes to the bones, you will need to make new Avatar Masks
        - You MUST remake the Custom Weapon Bundle detailed in Step 11
""",
        }

           # Create the sidebar with step buttons
        self.create_sidebar()

        # Create a textbox for displaying step instructions
        self.textbox = ctk.CTkTextbox(self, width=250, state="disabled", wrap="word")
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.grid_rowconfigure(0, weight=1)

        # Create a frame for appearance, scaling, and the "Run Attached Script" button
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 20), sticky="nsew")

        # Create appearance mode option
        self.appearance_mode_label = ctk.CTkLabel(self.bottom_frame, text="Appearance Mode:", anchor="e")
        self.appearance_mode_label.grid(row=0, column=0, padx=(10, 20), pady=(10, 10), sticky="e")
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.bottom_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=0, column=1, padx=(0, 20), pady=(10, 10), sticky="w")
        self.appearance_mode_optionmenu.set("System")  # Set default value

        # Create UI scaling option
        self.scaling_label = ctk.CTkLabel(self.bottom_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=0, column=2, padx=(0, 20), pady=(10, 10), sticky="w")
        self.scaling_optionmenu = ctk.CTkOptionMenu(self.bottom_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=0, column=3, padx=(0, 20), pady=(10, 10), sticky="w")
        self.scaling_optionmenu.set("100%")  # Set default value

        # Create the "Run Attached Script" button at the bottom right
        self.run_script_button = ctk.CTkButton(self.bottom_frame, text="Run Attached Script", fg_color="transparent", state="disabled", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.run_script)
        self.run_script_button.grid(row=0, column=4, padx=(20, 10), pady=(10, 10), sticky="e")

        # Adjust the grid configuration for the bottom frame
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        # Set the default step to Main Menu
        self.set_step_text("Main Menu")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def create_sidebar(self):
        # Create the logo label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="WeaponAIOTool", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create step buttons on the sidebar
        num_steps = len(self.steps)
        for i, step_name in enumerate(self.steps.keys(), start=1):
            button = ctk.CTkButton(self.sidebar_frame, text=step_name, command=lambda s=step_name: self.set_step_text(s))
            button.grid(row=i, column=0, padx=20, pady=(10, 0), sticky="nsew")
            self.step_buttons.append(button)
            self.sidebar_frame.grid_rowconfigure(i, weight=1)

        # Add empty space at the bottom
        self.sidebar_frame.grid_rowconfigure(len(self.steps) + 1, minsize=20)

    def set_step_text(self, step_name):
        # Display step instructions and update the button state
        step_text = self.steps.get(step_name, "Step not found")
        script_path = self.get_script_path(step_name)
        self.current_step = step_name

        if script_path:
            self.run_script_button.configure(state="normal")
        else:
            self.run_script_button.configure(state="disabled")

        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")

        font = ctk.CTkFont(size=16)
        self.textbox.configure("custom", font=font, spacing1=10)
        self.textbox.insert("0.0", step_text, "custom")

        self.textbox.configure(state="disabled")

    def get_script_path(self, step):
        # Define script paths for steps that have attached scripts
        script_paths = {
            "Step 1: Copy Dependencies": "resources/filegrabber.exe",
            "Step 3: Fix GUID References": "resources/scriptfix.exe",
            "Step 5: Handling Audio": "resources/audiofix.exe",
            "Step 8: Fixing Animations Part 3 (Unity)": "resources/animrenamereplace.exe",
            "Step 9: Left Hand Animations": "resources/lactionsfix.exe",
        }

        return script_paths.get(step)

    def run_script(self):
        # Run the attached script if available
        if self.current_step:
            script_path = self.get_script_path(self.current_step)
            if script_path:
                try:
                    subprocess.Popen([script_path])
                except Exception as e:
                    messagebox.showerror("Script Execution Error", f"Error running script for {self.current_step}: {str(e)}")
            else:
                messagebox.showinfo("Script Not Found", f"No external script found for {self.current_step}.")


if __name__ == "__main__":
    # Create and run the application
    app = App()
    app.mainloop()