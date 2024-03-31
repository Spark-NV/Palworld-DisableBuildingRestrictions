import os
import sys
import shutil
import re

def apply_modifications(Fpath, modifications):
    try:
        with open(Fpath, "rb") as f:
            Ehex = f.read().hex()
        
        successfully_applied_mods = []

        for mod_name, pattern, patch in modifications:
            if (res := re.search(pattern, Ehex, re.IGNORECASE)) is not None:
                addr = res.span()[0]
                Ehex = Ehex[:addr] + patch + Ehex[addr + len(patch):]
                successfully_applied_mods.append(mod_name)
                print(f"\n{mod_name} modification applied successfully")
            else:
                print(f"\n{mod_name} modification not applied. Pattern not found")

        if len(successfully_applied_mods) == len(modifications):
            with open(Fpath, "wb") as f:
                f.write(bytes.fromhex(Ehex))
            print(f"\n\nAll modifications applied successfully")
            input("Press Enter to continue...")
            return True
        else:
            print(f"\n\nNOT ALL MODIFICATIONS WERE SUCCESSFULL. DID THE GAME UPDATE AND NOW PALPATCHER NEEDS UPDATED?\n NO CHANGES WERE MADE...")
            input("Press Enter to continue...")
            return False

    except Exception as e:
        print(f"\nError applying modifications: {e}")
        input("Press Enter to continue...")
        return False

def create_backup(Fpath, install_folder, is_palworld, is_palserver, is_palserver_cmd):
    try:
        backup_folder = os.path.join(install_folder, "Palpatcher_Backup")
        if is_palworld:
            backup_name = f"Palworld-Win64-Shipping.bak"
        elif is_palserver:
            backup_name = f"PalServer-Win64-Test.bak"
        elif is_palserver_cmd:
            backup_name = f"PalServer-Win64-Test-Cmd.bak"
        backup_path = os.path.join(backup_folder, backup_name)
        if not os.path.exists(os.path.join(install_folder, "Palpatcher_Backup")):
            os.makedirs(os.path.join(install_folder, "Palpatcher_Backup"))
        if not os.path.exists(backup_path):
            shutil.copy(Fpath, backup_path)
            print(f"\nBackup created successfully: {backup_name}")
        else:
            print(f"\nBackup file exists, skipping backup: {backup_name}")
    except Exception as e:
        print(f"\nError creating backup: {e}")

def palserver(Fpath):
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support Restriction Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(Fpath, patterns_and_patches)

def palserver_cmd(Fpath):
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support Restriction Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(Fpath, patterns_and_patches)

def patch_palworld(Fpath):
    patterns_and_patches = [
        ("Allow Building Next To Palbox", "7415488B9EA8020000B2020FB64B30E8....0F00", "EB15"),
        ("Allow Building In Air", "0F84..000000488D8DE0000000E8......00", "909090909090"),
        ("Overlapping Bases", "75..488B9F000100004863BF0801000048C1E7044803","9090"),
        ("Disable World Collision", "7407B0..E9..0100000FB60B85C90F84..01000083F9","EB07"),
        ("Allow Building On Water", "..0E0FB64E30B2..E8......008846304C8D9C2460020000","EB0E"),
        ("Support Restriction Remove", "7E68488B4C24284885C97405E8......00488B4D..33DB","9090"),
        ("Support Restriction Remove2", "7309C7432801000000EB35C74328000000004863DE8D7301","9090"),
    ]
    apply_modifications(Fpath, patterns_and_patches)

def main():
    if len(sys.argv) > 1:
        Fpath = sys.argv[1]
        Ename = os.path.basename(Fpath).lower()
        install_folder = os.path.dirname(Fpath)

        if "palworld" in Ename:
            is_palworld = True
            is_palserver = False
            is_palserver_cmd = False
            print(f"\nPatching Palworld")
            create_backup(Fpath, install_folder, is_palworld, is_palserver, is_palserver_cmd)
            patch_palworld(Fpath)
        elif "palserver" in Ename and "cmd" not in Ename:
            is_palworld = False
            is_palserver = True
            is_palserver_cmd = False
            print(f"\nPatching Palserver")
            create_backup(Fpath, install_folder, is_palworld, is_palserver, is_palserver_cmd)
            palserver(Fpath)
        elif "palserver" in Ename and "cmd" in Ename:
            is_palworld = False
            is_palserver = False
            is_palserver_cmd = True
            print(f"\nPatching Palserver CMD")
            create_backup(Fpath, install_folder, is_palworld, is_palserver, is_palserver_cmd)
            palserver_cmd(Fpath)
        else:
            print("\nInvalid file. this patcher only supports Palworld, Palserver, or Palserver-Cmd.")
            input("Press Enter to exit...")
    else:
        print("\nNo input file provided. Either drag and drop the file onto this script, or execute the script with the file to be patched as an argument in a terminal window like this: python palpatcher.py /path/to/Palworld-Win64-Shipping")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()