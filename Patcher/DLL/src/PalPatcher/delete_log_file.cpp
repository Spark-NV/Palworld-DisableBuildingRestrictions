#include "delete_log_file.h"
#include "logging.h"

void DeleteLogFile()
{
    if (remove("Palpatcher_Log.txt") == 0)
    {
        Log("Old Log file deleted.");
    }
    else
    {
        Log("Error deleting Old log file.");
    }
}