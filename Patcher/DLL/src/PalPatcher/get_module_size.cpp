#include "get_module_size.h"
#include "logging.h"

#include <windows.h>
#include <psapi.h>

SIZE_T GetModuleSize()
{
    HMODULE hModule = GetModuleHandle(nullptr);

    if (hModule == nullptr)
    {
        Log("Error: Module not found in GetModuleSize.");
        return 0;
    }

    MODULEINFO moduleInfo;
    if (GetModuleInformation(GetCurrentProcess(), hModule, &moduleInfo, sizeof(MODULEINFO)) == 0)
    {
        Log("Error: Unable to get module information in GetModuleSize.");
        return 0;
    }

    char buffer[256];
    sprintf_s(buffer, "Module found at address: 0x%p with size: 0x%X", hModule, moduleInfo.SizeOfImage);
    Log(buffer);

    return moduleInfo.SizeOfImage;
}