#include "display_message_box.h"

#include <windows.h>

void DisplayMessageBox(const std::wstring& message)
{
    MessageBox(nullptr, message.c_str(), L" PalPatcher Error", MB_ICONERROR | MB_OK);
}