#include "patcher.h"

#include "get_module_base_address.h"
#include "modify_memory.h"
#include "log_process_info.h"
#include "force_close_process.h"
#include "display_message_box.h"
#include "get_executable_path.h"
#include "delete_log_file.h"
#include "get_module_size.h"
#include "pattern_error_message_box.h"
#include "find_pattern.h"
#include "pattern_not_found_force_close.h"
#include "logging.h"

#include <windows.h>
#include <codecvt>
#include <algorithm>

std::vector<MemoryModification> modifications;

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    std::wstring expectedMD5;

    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        Sleep(1000);
        DeleteLogFile();
        Log("PalPatcher Initializing.");

        std::wstring executablePath = GetExecutablePath();
        std::wstring executableName = executablePath.substr(executablePath.find_last_of(L"\\") + 1);
        std::transform(executableName.begin(), executableName.end(), executableName.begin(), towlower);

        if (executableName.find(L"palworld") != std::wstring::npos)
        {
            const BYTE Allow_Building_Close_To_Palbox_Pattern[] = { 0x74, 0x15, 0x48, 0x8B, 0x9E, 0xA8, 0x02, 0x00, 0x00, 0xB2, 0x02, 0x0F, 0xB6, 0x4B, 0x30, 0xE8, 0xCC, 0xCC, 0x0F, 0x00 };
            const BYTE Building_In_Mid_Air_Pattern[] = { 0x0F, 0x84, 0xCC, 0x00, 0x00, 0x00, 0x48, 0x8D, 0x8D, 0xE0, 0x00, 0x00, 0x00, 0xE8, 0xCC, 0xCC, 0xCC, 0x00, 0x48, 0xCC, 0xCC };
            const BYTE Overlapping_Bases_Pattern[] = { 0x75, 0xCC, 0x48, 0x8B, 0x9F, 0x00, 0x01, 0x00, 0x00, 0x48, 0x63, 0xBF, 0x08, 0x01, 0x00, 0x00, 0x48, 0xC1, 0xE7, 0x04, 0x48, 0x03, 0xFB };
            const BYTE Disable_World_Collision_Pattern[] = { 0x74, 0x07, 0xB0, 0xCC, 0xE9, 0xCC, 0x01, 0x00, 0x00, 0x0F, 0xB6, 0x0B, 0x85, 0xC9, 0x0F, 0x84, 0xCC, 0x01, 0x00, 0x00, 0x83, 0xF9, 0x01 };
            const BYTE Allow_Building_On_Water_Pattern[] = { 0xCC, 0x0E, 0x0F, 0xB6, 0x4E, 0x30, 0xB2, 0xCC, 0xE8, 0xCC, 0xCC, 0xCC, 0x00, 0x88, 0x46, 0x30, 0x4C, 0x8D, 0x9C, 0x24, 0x60, 0x02, 0x00, 0x00 };
            const BYTE Support_Restriction_Remove_Pattern[] = { 0x7E, 0x68, 0x48, 0x8B, 0x4C, 0x24, 0x28, 0x48, 0x85, 0xC9, 0x74, 0x05, 0xE8, 0xCC, 0xCC, 0xCC, 0x00, 0x48, 0x8B, 0x4D, 0xCC, 0x33, 0xDB };
            const BYTE Support_Restriction_Remove2_Pattern[] = { 0x73, 0x09, 0xC7, 0x43, 0x28, 0x01, 0x00, 0x00, 0x00, 0xEB, 0x35, 0xC7, 0x43, 0x28, 0x00, 0x00, 0x00, 0x00, 0x48, 0x63, 0xDE, 0x8D, 0x73, 0x01 };

            // PALWORLD
            Log("Found palworld!");
            modifications = {
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Allow_Building_Close_To_Palbox_Pattern, sizeof(Allow_Building_Close_To_Palbox_Pattern)), new BYTE[2]{0xEB, 0x15}, 2}, // Allow building close to palbox
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Building_In_Mid_Air_Pattern, sizeof(Building_In_Mid_Air_Pattern)), new BYTE[6]{0x90, 0x90, 0x90, 0x90, 0x90, 0x90}, 6}, // Building in mid air
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Overlapping_Bases_Pattern, sizeof(Overlapping_Bases_Pattern)), new BYTE[2]{0x90, 0x90}, 2}, // Overlapping bases
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Disable_World_Collision_Pattern, sizeof(Disable_World_Collision_Pattern)), new BYTE[2]{0xEB, 0x07}, 2}, // Disable world collision
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Allow_Building_On_Water_Pattern, sizeof(Allow_Building_On_Water_Pattern)), new BYTE[2]{0xEB, 0x0E}, 2}, // Allow building on water
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Support_Restriction_Remove_Pattern, sizeof(Support_Restriction_Remove_Pattern)), new BYTE[2]{0x90, 0x90}, 2}, // Support Restriction Remove
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Support_Restriction_Remove2_Pattern, sizeof(Support_Restriction_Remove2_Pattern)), new BYTE[2]{0x90, 0x90}, 2} // Support Restriction Remove2
            };
        }
        else if (executableName.find(L"palserver") != std::wstring::npos)
        {
            const BYTE Allow_Building_Close_To_Palbox_Pattern[] = { 0x74, 0x15, 0x48, 0x8B, 0x9E, 0xA8, 0x02, 0x00, 0x00, 0xB2, 0x02, 0x0F, 0xB6, 0x4B, 0x30, 0xE8, 0xCC, 0xCC, 0x0F, 0x00, 0x88 };
            const BYTE Building_In_Mid_Air_Pattern[] = { 0x0F, 0x84, 0xCC, 0x00, 0x00, 0x00, 0x48, 0x8D, 0x8D, 0xE0, 0x00, 0x00, 0x00, 0xE8, 0xCC, 0xCC, 0xCC, 0x00, 0x48, 0xCC, 0xCC };
            const BYTE Overlapping_Bases_Pattern[] = { 0x75, 0xCC, 0x48, 0x8B, 0x9F, 0x00, 0x01, 0x00, 0x00, 0x48, 0x63, 0xBF, 0x08, 0x01, 0x00, 0x00, 0x48, 0xC1, 0xE7, 0x04, 0x48, 0x03, 0xFB };
            const BYTE Disable_World_Collision_Pattern[] = { 0x74, 0x07, 0xB0, 0xCC, 0xE9, 0xCC, 0x01, 0x00, 0x00, 0x0F, 0xB6, 0x0B, 0x85, 0xC9, 0x0F, 0x84, 0xCC, 0x01, 0x00, 0x00, 0x83, 0xF9, 0x01 };
            const BYTE Allow_Building_On_Water_Pattern[] = { 0xCC, 0x0E, 0x0F, 0xB6, 0x4E, 0x30, 0xB2, 0xCC, 0xE8, 0xCC, 0xCC, 0x10, 0x00, 0x88, 0x46, 0x30, 0x4C, 0x8D, 0x9C, 0x24, 0x60, 0x02, 0x00, 0x00 };
            const BYTE Support_Restriction_Remove2_Pattern[] = { 0x73, 0x09, 0xC7, 0x43, 0x28, 0x01, 0x00, 0x00, 0x00, 0xEB, 0x35, 0xC7, 0x43, 0x28, 0x00, 0x00, 0x00, 0x00, 0x48, 0x63, 0xDE, 0x8D, 0x73, 0x01 };

            // PALSERVER
            Log("Found palserver!");
            modifications = {
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Allow_Building_Close_To_Palbox_Pattern, sizeof(Allow_Building_Close_To_Palbox_Pattern)), new BYTE[2]{0xEB, 0x15}, 2}, // Allow building close to palbox
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Building_In_Mid_Air_Pattern, sizeof(Building_In_Mid_Air_Pattern)), new BYTE[6]{0x90, 0x90, 0x90, 0x90, 0x90, 0x90}, 6}, // Building in mid air
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Overlapping_Bases_Pattern, sizeof(Overlapping_Bases_Pattern)), new BYTE[2]{0x90, 0x90}, 2}, // Overlapping bases
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Disable_World_Collision_Pattern, sizeof(Disable_World_Collision_Pattern)), new BYTE[2]{0xEB, 0x07}, 2}, // Disable world collision
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Allow_Building_On_Water_Pattern, sizeof(Allow_Building_On_Water_Pattern)), new BYTE[2]{0xEB, 0x0E}, 2}, // Allow building on water
                {FindPattern(GetModuleBaseAddress(), GetModuleSize(), Support_Restriction_Remove2_Pattern, sizeof(Support_Restriction_Remove2_Pattern)), new BYTE[2]{0x90, 0x90}, 2} // Support Restriction Remove2
            };
        }
        else
        {
            Log("Did not find palserver or palworld!");
            DisplayMessageBox(
                L"Executable is not palserver or palworld.\nThis patcher is meant for either of those 2 executables.");
            break;
        }

        std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

        Log("EXE Path: " + converter.to_bytes(executablePath));

        if (!ModifyMemory(modifications))
        {
            DisplayMessageBox(
                L"Failed to apply modifications. The game has been forcefully closed to protect your base.\nPlease see the GitHub Instructions.txt or the Nexusmods mod page for more info.");
            ForceCloseProcess();
            return FALSE;
        }

        LogProcessInfo();
        break;
    }

    return TRUE;
}