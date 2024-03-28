#include "get_executable_path.h"

#include <windows.h>

std::wstring GetExecutablePath()
{
    wchar_t buffer[MAX_PATH];
    GetModuleFileName(nullptr, buffer, MAX_PATH);
    return buffer;
}