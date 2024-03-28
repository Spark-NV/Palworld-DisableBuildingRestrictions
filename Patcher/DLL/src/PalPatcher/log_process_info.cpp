#include "log_process_info.h"
#include "logging.h"

#include <windows.h>
#include <fstream>
#include <iostream>

void LogProcessInfo()
{
    DWORD processId = GetCurrentProcessId();

    std::ofstream logFile("Palpatcher_Log.txt", std::ios::app);
    if (logFile.is_open())
    {
        logFile << "Process ID Found: " << processId << std::endl;
        logFile.close();
    }
}