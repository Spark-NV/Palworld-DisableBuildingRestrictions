#include "logging.h"

#include <fstream>

void Log(const std::string& message)
{
    std::ofstream logFile("Palpatcher_Log.txt", std::ios::app);
    if (logFile.is_open())
    {
        logFile << message << std::endl;
        logFile.close();
    }
}