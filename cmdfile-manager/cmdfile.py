# cmdfile.py

import os
import shutil
import sys
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from pyfiglet import Figlet
from colorama import init, Fore, Style
from termcolor import colored

init(autoreset=True)
console = Console()
f = Figlet(font='slant')

# -------------------- Lock Screen --------------------
def lock_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f.renderText("🔒 Secure Access"), style="bold red")
    for _ in range(3):
        pwd = Prompt.ask("[bold yellow]Enter password to unlock[/bold yellow]")
        if pwd == PASSWORD:
            print_success("Access granted.")
            time.sleep(1)
            return
        else:
            print_error("Wrong password.")
    console.print("[bold red]Too many attempts. Exiting...[/bold red]")
    sys.exit()

# -------------------- Banner --------------------
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(f.renderText("CMD File Manager"), style="bold blue")
    console.print("By HexFearCore  |  GitHub CLI Project\n", style="bold green")

# -------------------- Utility --------------------
def pause():
    input(Fore.YELLOW + "\nPress Enter to continue...")

def print_error(message):
    console.print(f"[bold red]✖ {message}[/bold red]")

def print_success(message):
    console.print(f"[bold green]✔ {message}[/bold green]")

def print_info(message):
    console.print(f"[cyan]> {message}[/cyan]")

# -------------------- List Directory --------------------
def list_directory(path):
    try:
        entries = os.listdir(path)
        table = Table(title=f"📁 Listing for: {path}")
        table.add_column("Name", justify="left")
        table.add_column("Type", justify="center")
        table.add_column("Size", justify="right")
        table.add_column("Last Modified", justify="center")

        for entry in entries:
            full_path = os.path.join(path, entry)
            entry_type = "Dir" if os.path.isdir(full_path) else "File"
            size = os.path.getsize(full_path)
            modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
            table.add_row(entry, entry_type, f"{size} B", modified)

        console.print(table)

    except Exception as e:
        print_error(f"Failed to list directory: {e}")

# -------------------- Change Directory --------------------
def change_directory(current_path):
    target = Prompt.ask("Enter folder name or path")
    new_path = os.path.abspath(os.path.join(current_path, target))
    if os.path.isdir(new_path):
        return new_path
    else:
        print_error("Invalid directory.")
        return current_path

# -------------------- Make Directory --------------------
def make_directory(current_path):
    name = Prompt.ask("Enter new folder name")
    try:
        os.mkdir(os.path.join(current_path, name))
        print_success("Folder created.")
    except Exception as e:
        print_error(f"Error creating folder: {e}")

# -------------------- Delete File/Folder --------------------
def delete_entry(current_path):
    name = Prompt.ask("Enter file/folder name to delete")
    full_path = os.path.join(current_path, name)
    try:
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
        print_success("Deleted successfully.")
    except Exception as e:
        print_error(f"Delete failed: {e}")

# -------------------- Rename File/Folder --------------------
def rename_entry(current_path):
    old_name = Prompt.ask("Old name")
    new_name = Prompt.ask("New name")
    try:
        os.rename(
            os.path.join(current_path, old_name),
            os.path.join(current_path, new_name)
        )
        print_success("Renamed successfully.")
    except Exception as e:
        print_error(f"Rename failed: {e}")

# -------------------- View File --------------------
def view_file(current_path):
    name = Prompt.ask("Enter filename to view")
    file_path = os.path.join(current_path, name)
    try:
        if not os.path.isfile(file_path):
            print_error("File does not exist.")
            return
        console.print(f"\n[bold green]--- Content of {name} ---[/bold green]")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                console.print(line.rstrip())
    except Exception as e:
        print_error(f"Error reading file: {e}")

# -------------------- Create and Write File --------------------
def create_write_file(current_path):
    name = Prompt.ask("Enter new filename")
    file_path = os.path.join(current_path, name)
    try:
        content = []
        console.print("[cyan]Enter your content below. Type '::save' to save and exit.[/cyan]")
        while True:
            line = input()
            if line.strip() == '::save':
                break
            content.append(line)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        print_success("File created and written.")
    except Exception as e:
        print_error(f"Write failed: {e}")

# -------------------- Search Entry --------------------
def search_entry(current_path):
    keyword = Prompt.ask("Enter keyword to search")
    found = []
    for root, dirs, files in os.walk(current_path):
        for name in files + dirs:
            if keyword.lower() in name.lower():
                found.append(os.path.join(root, name))

    if found:
        console.print(f"[bold green]✔ Found {len(found)} item(s):[/bold green]")
        for path in found:
            console.print(f" - {path}")
    else:
        print_error("No matching files/folders found.")

# -------------------- File Info --------------------
def file_info(current_path):
    name = Prompt.ask("Enter file or folder name")
    path = os.path.join(current_path, name)
    if not os.path.exists(path):
        print_error("File/Folder does not exist.")
        return
    size = os.path.getsize(path)
    modified = datetime.fromtimestamp(os.path.getmtime(path))
    created = datetime.fromtimestamp(os.path.getctime(path))
    ftype = "Directory" if os.path.isdir(path) else "File"

    console.print(f"\n[bold blue]Info for {name}[/bold blue]")
    console.print(f"Type       : {ftype}")
    console.print(f"Size       : {size} bytes")
    console.print(f"Created    : {created}")
    console.print(f"Modified   : {modified}")
    console.print(f"Full Path  : {os.path.abspath(path)}")

# -------------------- Clear Screen --------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# -------------------- Global State --------------------
THEME = "dark"
LOG_FILE = "cmd_file_log.txt"
FAV_FILE = "favorites.txt"
RECYCLE_BIN = ".recycle_bin"
PASSWORD = "admin123"  # You can customize this

# -------------------- Log Activity --------------------
def log_action(action):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action}\n")

# -------------------- Recycle Bin Init --------------------
def init_recycle_bin(base_path):
    bin_path = os.path.join(base_path, RECYCLE_BIN)
    if not os.path.exists(bin_path):
        os.makedirs(bin_path)
    return bin_path

# -------------------- Soft Delete --------------------
def soft_delete(current_path):
    name = Prompt.ask("Enter file/folder name to recycle")
    full_path = os.path.join(current_path, name)
    bin_path = init_recycle_bin(current_path)
    try:
        if not os.path.exists(full_path):
            print_error("Entry doesn't exist.")
            return
        shutil.move(full_path, os.path.join(bin_path, name))
        print_success("Moved to recycle bin.")
        log_action(f"Soft deleted: {name}")
    except Exception as e:
        print_error(f"Recycle failed: {e}")

# -------------------- Restore From Recycle Bin --------------------
def restore_from_bin(current_path):
    bin_path = init_recycle_bin(current_path)
    if not os.listdir(bin_path):
        print_error("Recycle bin is empty.")
        return
    list_directory(bin_path)
    name = Prompt.ask("Enter name to restore")
    try:
        shutil.move(os.path.join(bin_path, name), os.path.join(current_path, name))
        print_success("Restored successfully.")
        log_action(f"Restored: {name}")
    except Exception as e:
        print_error(f"Restore failed: {e}")

# -------------------- Theme Switcher --------------------
def switch_theme():
    global THEME
    THEME = "light" if THEME == "dark" else "dark"
    print_success(f"Switched to {THEME} theme.")
    log_action(f"Theme changed to {THEME}")

# -------------------- Add Favorite --------------------
def add_favorite(path):
    try:
        with open(FAV_FILE, "a", encoding="utf-8") as f:
            f.write(f"{path}\n")
        print_success("Added to favorites.")
    except Exception as e:
        print_error(f"Favorite failed: {e}")

# -------------------- View Favorites --------------------
def view_favorites():
    try:
        if not os.path.exists(FAV_FILE):
            print_error("No favorites found.")
            return
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        console.print("\n[bold cyan]★ Favorite Paths:[/bold cyan]")
        for line in lines:
            console.print(f" - {line.strip()}")
    except Exception as e:
        print_error(f"Failed to read favorites: {e}")



# -------------------- Main Menu --------------------
def main():
    current_path = os.getcwd()
    while True:
        print_banner()
        print_info(f"Current Directory: {current_path}")
        console.print("\n[bold magenta]Available Commands:[/bold magenta]")
        console.print("[yellow]1.[/yellow] List files/folders")
        console.print("[yellow]2.[/yellow] Change directory")
        console.print("[yellow]3.[/yellow] Make folder")
        console.print("[yellow]4.[/yellow] Delete file/folder")
        console.print("[yellow]5.[/yellow] Rename file/folder")
        console.print("[yellow]6.[/yellow] View file contents")
        console.print("[yellow]7.[/yellow] Create/write file")
        console.print("[yellow]8.[/yellow] Search files/folders")
        console.print("[yellow]9.[/yellow] File/Folder info")
        console.print("[yellow]10.[/yellow] Clear screen")
        console.print("[yellow]11.[/yellow] Soft delete (to recycle bin)")
        console.print("[yellow]12.[/yellow] Restore from recycle bin")
        console.print("[yellow]13.[/yellow] Switch theme (dark/light)")
        console.print("[yellow]14.[/yellow] Add to favorites")
        console.print("[yellow]15.[/yellow] View favorites")
        console.print("[yellow]0.[/yellow] Exit\n")


        choice = Prompt.ask("Enter your choice")

        if choice == '1':
            list_directory(current_path)
        elif choice == '2':
            current_path = change_directory(current_path)
        elif choice == '3':
            make_directory(current_path)
        elif choice == '4':
            delete_entry(current_path)
        elif choice == '5':
            rename_entry(current_path)
        elif choice == '6':
            view_file(current_path)
        elif choice == '7':
            create_write_file(current_path)
        elif choice == '8':
            search_entry(current_path)
        elif choice == '9':
            file_info(current_path)
        elif choice == '10':
            clear_screen()
        elif choice == '11':
            soft_delete(current_path)
        elif choice == '12':
            restore_from_bin(current_path)
        elif choice == '13':
            switch_theme()
        elif choice == '14':
            add_favorite(current_path)
        elif choice == '15':
            view_favorites()
        elif choice == '0':
            console.print("\n[bold blue]Exiting... Goodbye![/bold blue]")
            time.sleep(1)
            break
        else:
            print_error("Invalid choice!")

        pause()

if __name__ == "__main__":
    main()
