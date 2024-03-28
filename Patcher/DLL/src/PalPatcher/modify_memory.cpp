#include "modify_memory.h"
#include "get_module_base_address.h"
#include "logging.h"

#include <windows.h>

bool ModifyMemory(const std::vector<MemoryModification>& modifications)
{
    Log("Applying Patches...");

    LPVOID moduleBaseAddress = GetModuleBaseAddress();
    if (moduleBaseAddress != nullptr)
    {
        Log("Number of modifications: " + std::to_string(modifications.size()));
        for (const auto& modification : modifications)
        {
            // Print information about the modification
            char buffer[256];
            sprintf_s(buffer, "Modification address: 0x%p", modification.address);
            Log(buffer);

            SIZE_T bytesWritten = 0;
            if (!WriteProcessMemory(GetCurrentProcess(), modification.address, modification.bytes, modification.size, &bytesWritten)
                || bytesWritten != modification.size)
            {
                sprintf_s(buffer, "Error modifying address (0x%p). Bytes written: %zu", modification.bytes, bytesWritten);
                Log(buffer);
                Log("Address modification failed.");
                return false;
            }
            Log("Address modified successfully.");
        }
    }
    else
    {
        Log("Error getting module base address.");
        return false;
    }

    return true;
}