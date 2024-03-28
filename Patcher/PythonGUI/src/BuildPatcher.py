import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import webbrowser
import os
import shutil
import platform
import winreg
import re
import threading
from ttkthemes import ThemedStyle

def apply_modifications(exe_path, modifications, output_text):
    try:
        with open(exe_path, "rb") as f:
            exe_hex = f.read().hex()
        
        successfully_applied_mods = []

        for mod_name, pattern, patch in modifications:
            if (res := re.search(pattern, exe_hex, re.IGNORECASE)) is not None:
                addr = res.span()[0]
                exe_hex = exe_hex[:addr] + patch + exe_hex[addr + len(patch):]
                successfully_applied_mods.append(mod_name)
                output_text.insert(tk.END, f"\n{mod_name} modification applied successfully")
            else:
                output_text.insert(tk.END, f"\n{mod_name} modification not applied. Pattern not found")

        if len(successfully_applied_mods) == len(modifications):
            with open(exe_path, "wb") as f:
                f.write(bytes.fromhex(exe_hex))
            output_text.insert(tk.END, f"\n\nAll modifications applied successfully")
            return True
        else:
            output_text.insert(tk.END, f"\n\nNOT ALL MODIFICATIONS WERE SUCCESSFULL. DID THE GAME UPDATE AND NOW PALPATCHER NEEDS UPDATED?\n NO CHANGES WERE MADE...")
            return False

    except Exception as e:
        output_text.insert(tk.END, f"\nError applying modifications: {e}")
        return False

def create_backup(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text):
    try:
        steamapps_path = os.path.join(steam_install_path, "steamapps")
        app_manifest = os.path.join(steamapps_path, f"appmanifest_{app_id}.acf")
        last_updated = "unknown"
        if os.path.isfile(app_manifest):
            with open(app_manifest, "r") as manifest_file:
                lines = manifest_file.readlines()
                for line in lines:
                    if "lastupdated" in line:
                        last_updated = line.split('"')[3]
                    if "installdir" in line:
                        install_dir = line.split('"')[3]
                    if last_updated != "unknown" and install_dir is not None:
                        break
                else:
                    output_text.insert(tk.END, f"\nEither 'lastupdated' or 'installdir' not found.")
                install_folder = os.path.join(steamapps_path, "common", install_dir)
                if not os.path.exists(os.path.join(install_folder, "Palpatcher_Backup")):
                    os.makedirs(os.path.join(install_folder, "Palpatcher_Backup"))
                backup_folder = os.path.join(install_folder, "Palpatcher_Backup")
                if is_palworld:
                    backup_name = f"{last_updated}_Palworld-Win64-Shipping.bak"
                elif is_palserver:
                    backup_name = f"{last_updated}_PalServer-Win64-Test.bak"
                elif is_palserver_cmd:
                    backup_name = f"{last_updated}_PalServer-Win64-Test-Cmd.bak"
                backup_path = os.path.join(backup_folder, backup_name)
                if not os.path.exists(backup_path):
                    shutil.copy(exe_path, backup_path)
                    output_text.insert(tk.END, f"\nBackup created successfully: {backup_name}")
                else:
                    output_text.insert(tk.END, f"\nBackup file exists, checking if we need to make a new backup...")
                    if is_palworld:
                        backup_last_updated = re.search(r"(\d+)_Palworld-Win64-Shipping\.bak", backup_name).group(1)
                    elif is_palserver:
                        backup_last_updated = re.search(r"(\d+)_PalServer-Win64-Test\.bak", backup_name).group(1)
                    elif is_palserver_cmd:
                        backup_last_updated = re.search(r"(\d+)_PalServer-Win64-Test-Cmd\.bak", backup_name).group(1)
                    output_text.insert(tk.END, f"\ngot : {backup_last_updated}")
                    if backup_last_updated != last_updated:
                        shutil.copy(exe_path, backup_path)
                        output_text.insert(tk.END, f"\nBackup updated successfully: {backup_name}")
                    else:
                        output_text.insert(tk.END, f"\nSkipping backup as it already exists: {backup_name} \n")
    except Exception as e:
        output_text.insert(tk.END, f"\nError creating backup: {e}")

def get_steam_install_path(output_text):
    try:
        if platform.architecture()[0] == '32bit':
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        else:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Valve\Steam")
        install_path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        return install_path
    except Exception as e:
        output_text.insert(tk.END, f"\nError: {e}")
        return None

def get_game_install_folder_with_exe(steam_install_path, app_id, exe_name):
    steamapps_path = os.path.join(steam_install_path, "steamapps")
    app_manifest_path = os.path.join(steamapps_path, f"appmanifest_{app_id}.acf")
    if os.path.exists(app_manifest_path):
        with open(app_manifest_path, "r") as manifest_file:
            lines = manifest_file.readlines()
            for line in lines:
                if "installdir" in line:
                    install_dir = line.split('"')[3]
                    install_folder = os.path.join(steamapps_path, "common", install_dir)
                    for root, dirs, files in os.walk(install_folder):
                        for file in files:
                            if file.lower() == exe_name.lower() and file.endswith(".exe"):
                                return os.path.join(root, file)
    return None

def open_url(url):
    webbrowser.open(url)

def restore_exe(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text):
    try:
        steamapps_path = os.path.join(steam_install_path, "steamapps")
        app_manifest = os.path.join(steamapps_path, f"appmanifest_{app_id}.acf")
        last_updated = "unknown"
        if os.path.isfile(app_manifest):
            with open(app_manifest, "r") as manifest_file:
                lines = manifest_file.readlines()
                for line in lines:
                    if "lastupdated" in line:
                        last_updated = line.split('"')[3]
                    if "installdir" in line:
                        install_dir = line.split('"')[3]
                    if last_updated != "unknown" and install_dir is not None:
                        break
                else:
                    output_text.insert(tk.END, f"\nEither 'lastupdated' or 'installdir' not found.")
                install_folder = os.path.join(steamapps_path, "common", install_dir)
                backup_folder = os.path.join(install_folder, "Palpatcher_Backup")
                if is_palworld:
                    backup_name = f"{last_updated}_Palworld-Win64-Shipping.bak"
                elif is_palserver:
                    backup_name = f"{last_updated}_PalServer-Win64-Test.bak"
                elif is_palserver_cmd:
                    backup_name = f"{last_updated}_PalServer-Win64-Test-Cmd.bak"
                backup_path = os.path.join(backup_folder, backup_name)
                try:
                    output_text.insert(tk.END, f"\nMoving {backup_path} \nto\n {exe_path}")
                    shutil.move(backup_path, exe_path)
                    output_text.insert(tk.END, f"\n\nMove complete")
                except Exception as e:
                    output_text.insert(tk.END, f"\nError restoring exe: {e}")
    except Exception as e:
        output_text.insert(tk.END, f"\nError restoring exe: {e}")

def palserver(output_text):
    output_text.insert(tk.END, "\nFinding Palserver")
    steam_install_path = get_steam_install_path(output_text)
    is_palserver = True
    is_palserver_cmd = False
    is_palworld = False
    if steam_install_path:
        output_text.insert(tk.END, f"\nFound Steam!, Steam Install Path: {steam_install_path}")
        app_id = "2394010"
        exe_name = "PalServer-Win64-Test.exe"
        exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
        output_text.insert(tk.END, f"\nFound Palserver!, Install Path: {exe_path}")
        create_backup(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)
    else:
        output_text.insert(tk.END, f"\nNo executable file found for App ID {app_id} and exe name {exe_name}.")
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support_Restriction_Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(exe_path, patterns_and_patches, output_text)
    
def palserver_cmd(output_text):
    output_text.insert(tk.END, "\nFinding Palserver cmd")
    steam_install_path = get_steam_install_path(output_text)
    is_palserver = False
    is_palserver_cmd = True
    is_palworld = False
    if steam_install_path:
        output_text.insert(tk.END, f"\nFound Steam!, Steam Install Path: {steam_install_path}")
        app_id = "2394010"
        exe_name = "PalServer-Win64-Test-Cmd.exe"
        exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
        output_text.insert(tk.END, f"\nFound Palserver cmd!, Install Path: {exe_path}")
        create_backup(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)
    else:
        output_text.insert(tk.END, f"\nNo executable file found for App ID {app_id} and exe name {exe_name}.")
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support_Restriction_Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(exe_path, patterns_and_patches, output_text)

def val_world(output_text):
    output_text.insert(tk.END, "\nValidating Palworld Install")
    url = f"steam://validate/1623730"
    webbrowser.open(url)

def val_server(output_text):
    output_text.insert(tk.END, "\nValidating Palserver Install")
    url = f"steam://validate/2394010"
    webbrowser.open(url)

def restore_cmd(output_text):
    output_text.insert(tk.END, "\nRestoring palserver Exe")
    steam_install_path = get_steam_install_path(output_text)
    is_palserver = False
    is_palserver_cmd = True
    is_palworld = False
    app_id = "2394010"
    exe_name = "PalServer-Win64-Test-Cmd.exe"
    exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
    restore_exe(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)

def restore(output_text):
    output_text.insert(tk.END, "\nRestoring cmd Exe")
    steam_install_path = get_steam_install_path(output_text)
    is_palserver = True
    is_palserver_cmd = False
    is_palworld = False
    app_id = "2394010"
    exe_name = "PalServer-Win64-Test.exe"
    exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
    restore_exe(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)

def restore_palworld(output_text):
    output_text.insert(tk.END, "\nRestoring Exe")
    steam_install_path = get_steam_install_path(output_text)
    is_palworld = True
    is_palserver_cmd = False
    is_palserver = False
    app_id = "1623730"
    exe_name = "Palworld-Win64-Shipping.exe"
    exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
    restore_exe(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)

def nexusmods(output_text):
    output_text.insert(tk.END, "\nOpening nexusmods mod page")
    open_url('https://www.nexusmods.com/palworld/mods/809')
    
def github(output_text):
    output_text.insert(tk.END, "\nOpening Github Instructions")
    open_url('https://raw.githubusercontent.com/Spark-NV/Palworld-DisableBuildingRestrictions/master/Patcher/Instructions.txt') 

def patch_palworld(output_text):
    output_text.insert(tk.END, "\nFinding Palworld")
    steam_install_path = get_steam_install_path(output_text)
    is_palworld = True
    is_palserver = False
    is_palserver_cmd = False
    if steam_install_path:
        output_text.insert(tk.END, f"\nFound Steam!, Steam Install Path: {steam_install_path}")
        app_id = "1623730"
        exe_name = "Palworld-Win64-Shipping.exe"
        exe_path = get_game_install_folder_with_exe(steam_install_path, app_id, exe_name)
        output_text.insert(tk.END, f"\nFound Palworld!, Install Path: {exe_path}")
        create_backup(exe_path, app_id, steam_install_path, is_palworld, is_palserver, is_palserver_cmd, output_text)
    else:
        output_text.insert(tk.END, f"\nNo executable file found for App ID {app_id} and exe name {exe_name}.")
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support Restriction Remove", "7E68488B4C24284885C97405E8......00488B4D..33DB","9090"),
        ("Support_Restriction_Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(exe_path, patterns_and_patches, output_text)

def main():
    def button_callback(event):
        if event.widget["text"] == "Restore Palworld":
            threading.Thread(target=restore_palworld, args=(output_text,)).start()
        elif event.widget["text"] == "Restore Palserver":
            threading.Thread(target=restore_cmd, args=(output_text,)).start()
            threading.Thread(target=restore, args=(output_text,)).start()
        elif event.widget["text"] == "Nexusmods Page":
            threading.Thread(target=nexusmods, args=(output_text,)).start()
        elif event.widget["text"] == "Instructions":
            threading.Thread(target=github, args=(output_text,)).start()
        elif event.widget["text"] == "Patch Palworld":
            threading.Thread(target=patch_palworld, args=(output_text,)).start()
        elif event.widget["text"] == "Patch Palserver":
            threading.Thread(target=palserver, args=(output_text,)).start()
            threading.Thread(target=palserver_cmd, args=(output_text,)).start()
        elif event.widget["text"] == "Validate Palworld":
            threading.Thread(target=val_world, args=(output_text,)).start()
        elif event.widget["text"] == "Validate Palserver":
            threading.Thread(target=val_server, args=(output_text,)).start()

    root = tk.Tk()
    root.title('Tkinter PalPatcher')
    root.minsize(width=700, height=400)

    style = ThemedStyle(root)
    style.theme_use('vista')

    def show_info(row, output_text):
        if row == 0:
            output_text.insert(tk.END, "Webpage Buttons:\n"
                                       "Nexusmods Page: Opens the Nexusmods page for the mod.\n"
                                       "Instructions: Opens the GitHub instructions for the mod.\n")
        elif row == 1:
            output_text.insert(tk.END, "Modification Buttons:\n"
                                       "These buttons will first make a backup of the executable then apply all the modifications to the Palworld/Palserver executable.\n")
        elif row == 2:
            output_text.insert(tk.END, "Restore Buttons:\n"
                                       "These restore the original executable from the backup made from the Patch/Modification buttons.\n")
        elif row == 3:
            output_text.insert(tk.END, "Validate Buttons:\n"
                                       "These buttons call the steam validate function, this will restore the Installation/Executables in the event the backups are either bad or dont exist.\n")
    
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    for row_index in range(4):
        button_row = ttk.Frame(button_frame)
        button_row.grid(row=row_index, column=0, sticky="w")
    
        info_button = ttk.Button(button_row, text="?", width=2, command=lambda row=row_index: show_info(row, output_text))
        info_button.grid(row=0, column=0, padx=(15, 0))
    
        if row_index == 0:
            nexus_button = ttk.Button(button_row, text="Nexusmods Page")
            nexus_button.bind("<Button-1>", button_callback)
            nexus_button.grid(row=0, column=1, padx=(0, 10))
    
            instructions_button = ttk.Button(button_row, text="Instructions")
            instructions_button.bind("<Button-1>", button_callback)
            instructions_button.grid(row=0, column=2, padx=(10, 0))
    
        elif row_index == 1:
            palworld_button = ttk.Button(button_row, text="Patch Palworld")
            palworld_button.bind("<Button-1>", button_callback)
            palworld_button.grid(row=0, column=1, padx=(0, 10))
    
            palserver_button = ttk.Button(button_row, text="Patch Palserver")
            palserver_button.bind("<Button-1>", button_callback)
            palserver_button.grid(row=0, column=2, padx=(23, 0))
    
        elif row_index == 2:
            restore_palworld_button = ttk.Button(button_row, text="Restore Palworld")
            restore_palworld_button.bind("<Button-1>", button_callback)
            restore_palworld_button.grid(row=0, column=1, padx=(0, 10))
    
            restore_palserver_button = ttk.Button(button_row, text="Restore Palserver")
            restore_palserver_button.bind("<Button-1>", button_callback)
            restore_palserver_button.grid(row=0, column=2, padx=(14, 0))
    
        elif row_index == 3:
            validate_button = ttk.Button(button_row, text="Validate Palworld")
            validate_button.bind("<Button-1>", button_callback)
            validate_button.grid(row=0, column=1, padx=(0, 10))
    
            validate_button = ttk.Button(button_row, text="Validate Palserver")
            validate_button.bind("<Button-1>", button_callback)
            validate_button.grid(row=0, column=2, padx=(12, 0))
    
    output_frame = ttk.Frame(root)
    output_frame.pack()

    output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=100, height=20)
    output_text.pack()

    original_insert = output_text.insert

    def insert_text(index, text, *args):
        original_insert(index, text + '\n')
        output_text.see(tk.END)

    output_text.insert = insert_text

    root.mainloop()

if __name__ == "__main__":
    main()
