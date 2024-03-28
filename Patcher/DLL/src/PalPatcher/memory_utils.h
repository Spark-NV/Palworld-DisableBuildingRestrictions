#pragma once

#include <windows.h>

struct MemoryModification
{
    LPVOID address;
    BYTE* bytes;
    SIZE_T size;
};