#include "find_pattern.h"
#include "pattern_not_found_force_close.h"
#include "logging.h"

#include <windows.h>

LPVOID FindPattern(LPVOID startAddress, SIZE_T size, const BYTE* pattern, SIZE_T patternSize)
{
    for (SIZE_T i = 0; i < size - patternSize; ++i)
    {
        bool found = true;
        for (SIZE_T j = 0; j < patternSize; ++j)
        {
            if (pattern[j] != 0xCC && pattern[j] != *((BYTE*)startAddress + i + j))
            {
                found = false;
                break;
            }
        }

        if (found)
        {
            char buffer[256];
            sprintf_s(buffer, "Pattern found at address: 0x%p, ", (LPVOID)((DWORD_PTR)startAddress + i));

            const int bytesToShow = 10;
            for (int k = -bytesToShow; k <= bytesToShow; ++k)
            {
                char byteBuffer[32];
                sprintf_s(byteBuffer, "0x%02X ", *((BYTE*)startAddress + i + k));
                strcat_s(buffer, byteBuffer);
            }

            Log(buffer);

            return (LPVOID)((DWORD_PTR)startAddress + i);
        }
    }

    PatternNotFoundForceClose(pattern, patternSize);

    return nullptr;
}