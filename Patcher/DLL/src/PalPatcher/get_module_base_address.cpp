#include "get_module_base_address.h"
#include "logging.h"

LPVOID GetModuleBaseAddress()
{
    HMODULE hModule = GetModuleHandle(nullptr);

    if (hModule != nullptr)
    {
        Log("Module handle obtained.");

        auto baseAddress = hModule;

        char buffer[256];
        sprintf_s(buffer, "Base address of the module: 0x%p", baseAddress);
        Log(buffer);

        return baseAddress;
    }
    Log("Error obtaining module handle.");

    return nullptr;
}