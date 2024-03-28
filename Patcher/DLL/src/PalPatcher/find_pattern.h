#pragma once

#include <windows.h>

LPVOID FindPattern(LPVOID startAddress, SIZE_T size, const BYTE* pattern, SIZE_T patternSize);