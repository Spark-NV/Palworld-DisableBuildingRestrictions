#include "pattern_not_found_force_close.h"
#include "pattern_error_message_box.h"
#include "force_close_process.h"
#include "logging.h"

#include <windows.h>

void PatternNotFoundForceClose(const BYTE* pattern, SIZE_T patternSize)
{
    Log("Pattern not found in the specified memory range. Forcefully closing the process...");

    char patternBuffer[256];
    sprintf_s(patternBuffer, "Pattern not found. Pattern size: %zu. Pattern:", patternSize);
    strcat_s(patternBuffer, sizeof(patternBuffer), " ");

    for (SIZE_T i = 0; i < patternSize; ++i)
    {
        char byteBuffer[8];
        sprintf_s(byteBuffer, "0x%02X ", pattern[i]);
        strcat_s(patternBuffer, sizeof(patternBuffer), byteBuffer);
    }

    Log(patternBuffer);

    PatternErrorMessageBox(
        L"One or more search pattern's were not found.\nThis patcher tries to be as hardened as possible to updates, but it's possible the game updated and now the code has changed.\n\nYou might need to wait for an update for PalPatcher.\n\nYou can help by posting the contents of the PalPatcher.log");

    ForceCloseProcess();
}