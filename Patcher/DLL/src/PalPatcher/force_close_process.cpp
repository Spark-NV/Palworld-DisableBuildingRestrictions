#include "force_close_process.h"
#include "logging.h"

#include <windows.h>

void ForceCloseProcess()
{
    Log("Palpatcher is Forcefully closing the process...");
    TerminateProcess(GetCurrentProcess(), 1);
}