#!/usr/bin/env python3
import os
import shutil
import argparse
from datetime import datetime
from rich.console import Console
from rich.progress import track
from rich.panel import Panel

# Initialize console for rich outputs
console = Console()

# File type categories
FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Pictures": [".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"],
}

def get_category(file):
    ext = os.path.splitext(file)[1].lower()
    for category, exts in FILE_CATEGORIES.items():
        if ext in exts:
            return category
    return "Misc"

def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_file(file, src_folder, dest_folder, dry_run=False):
    src_path = os.path.join(src_folder, file)
    if not os.path.isfile(src_path):
        return
    category = get_category(file)
    year = datetime.now().year
    month = datetime.now().strftime("%B")
    target_folder = os.path.join(dest_folder, category, str(year), month)
    make_folder(target_folder)
    dest_path = os.path.join(target_folder, file)
    if dry_run:
        console.log(f"[yellow]Dry run:[/yellow] 📂 {file} -> {dest_path}")
    else:
        shutil.move(src_path, dest_path)
        console.log(f"[green]Moved[/green] 📂 {file} -> {dest_path}")

def main():
    parser = argparse.ArgumentParser(description="Folder Sorcerer 🧙‍♂️✨")
    parser.add_argument("folder", help="Folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)
    console.print(Panel(f"[bold cyan]Organizing folder:[/bold cyan] {folder}", expand=False))

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        console.print("[red]No files found in this folder.[/red]")
        return

    for file in track(files, description="Processing files..."):
        move_file(file, folder, folder, dry_run=args.dry_run)

    console.print(Panel("[bold green]Folder organization complete! 🎉[/bold green]", expand=False))

if __name__ == "__main__":
    main()
