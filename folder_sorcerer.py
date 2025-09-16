#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import datetime
from rich.console import Console
from rich.progress import track

console = Console()

# ------------------------
# CONFIG
# ------------------------
BASE_FOLDER = "."  # Current folder if no argument given
DRY_RUN = False    # Will be updated by command-line argument

# ------------------------
# Helper functions
# ------------------------
def move_file(file, dest):
    os.makedirs(dest, exist_ok=True)
    if DRY_RUN:
        console.log(f"📂 [yellow]Would move[/yellow] {file} ➡️ {dest}")
    else:
        # Rename if file already exists
        base, ext = os.path.splitext(file)
        counter = 1
        new_file = file
        while os.path.exists(os.path.join(dest, new_file)):
            new_file = f"{base}_{counter}{ext}"
            counter += 1
        shutil.move(file, os.path.join(dest, new_file))
        console.log(f"📂 Moved {file} ➡️ {dest} ✅")

def categorize_file(file):
    ext = file.lower().split('.')[-1]
    if ext in ["jpg","jpeg","png","gif","bmp","webp"]:
        return "Pictures"
    elif ext in ["mp4","mov","avi","mkv","flv"]:
        return "Videos"
    elif ext in ["pdf","docx","doc","txt","pptx","xlsx"]:
        return "Documents"
    elif ext in ["zip","tar","gz","rar"]:
        return "Archives"
    elif ext in ["py","js","html","css","cpp","c","java"]:
        return "Code"
    else:
        return "Misc"

# ------------------------
# Main logic
# ------------------------
if __name__ == "__main__":
    import sys

    folder = sys.argv[1] if len(sys.argv) > 1 else BASE_FOLDER
    if "--dry-run" in sys.argv:
        DRY_RUN = True

    console.rule(f"🧙‍♂️ Organizing folder: {os.path.abspath(folder)}")

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        console.log("[red]No files found in this folder.[/red]")
        exit()

    for file in track(files, description="✨ Sorting files..."):
        category = categorize_file(file)
        year_month = datetime.datetime.now().strftime("%Y/%B")
        dest_folder = os.path.join(folder, category, year_month)
        move_file(os.path.join(folder, file), dest_folder)

    console.rule("🎉 Folder organization complete!")
