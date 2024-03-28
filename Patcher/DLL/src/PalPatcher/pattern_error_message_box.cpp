#include "pattern_error_message_box.h"

#include <windows.h>

void PatternErrorMessageBox(const std::wstring& message)
{
    MessageBox(nullptr, message.c_str(), L"Pattern Not Found Error", MB_ICONERROR | MB_OK);
}