import os
import shutil
import subprocess
from pathlib import Path

# Configuration
SOURCE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = SOURCE_DIR / "resources"
TEMP_DIR = Path.cwd() / "temp"
FINAL_DIR = Path.cwd() / "Final Build"

def should_build(py_file, exe_file):
    """Check if the .exe needs to be built or updated."""
    if not exe_file.exists():
        return True
    return py_file.stat().st_mtime > exe_file.stat().st_mtime

def build_resources():
    """Build only necessary Python scripts in the resources directory to EXEs."""
    print("Checking resource scripts...")
    resource_files = list(RESOURCES_DIR.glob("*.py"))
    temp_resources_dir = TEMP_DIR / "resources"
    temp_resources_dir.mkdir(parents=True, exist_ok=True)

    for script in resource_files:
        exe_file = temp_resources_dir / (script.stem + ".exe")

        if should_build(script, exe_file):
            print(f"Building {script.name}...")
            try:
                subprocess.run([
                    "pyinstaller",
                    "--noconfirm",
                    "--onefile",
                    "--windowed",
                    "--clean",
                    "--icon", str(SOURCE_DIR / "icon.ico"),
                    "--add-data", f"{str(Path('C:/Python312/Lib/site-packages/customtkinter'))}{os.pathsep}customtkinter",
                    "--distpath", str(temp_resources_dir),
                    "--workpath", str(TEMP_DIR / "build"),
                    str(script)
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error building {script.name}: {e}")
                raise
        else:
            print(f"Skipping {script.name}, already up to date.")

def build_main_app():
    """Build the main application."""
    print("Building main application...")

    try:
        subprocess.run([
            "pyinstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--icon", str(SOURCE_DIR / "icon.ico"),
            "--hidden-import", "customtkinter",
            "--add-data", f"{str(TEMP_DIR / 'resources')}{os.pathsep}resources",
            "--add-data", f"{str(Path('C:/Python312/Lib/site-packages/customtkinter'))}{os.pathsep}customtkinter",
            "--distpath", str(FINAL_DIR),
            "--workpath", str(TEMP_DIR / "build"),
            str(TEMP_DIR / "weaponAIO.py")
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building main application: {e}")
        raise

def main():
    # Ensure necessary directories exist
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    # Build resource EXEs
    build_resources()

    # Copy main script to temp
    shutil.copy(SOURCE_DIR / "weaponAIO.py", TEMP_DIR)

    # Build main application
    build_main_app()

    print(f"Build complete! Final executable in: {FINAL_DIR}")

if __name__ == "__main__":
    main()
