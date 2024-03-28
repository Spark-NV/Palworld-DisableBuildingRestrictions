@echo off
setlocal enabledelayedexpansion

for /f "tokens=2*" %%A in ('reg query "HKCU\Software\Valve\Steam" /v "SteamPath" 2^>nul') do set "steamPath=%%B"
echo Steam installation directory: %steamPath%

for /f "usebackq delims=" %%A in ("%steamPath%\steamapps\appmanifest_1623730.acf") do (
    echo %%A | find /i "installdir" > nul && set "Palworld_InstallDir=%%A"
)
if exist "%steamPath%\steamapps\appmanifest_2394010.acf" (
for /f "usebackq delims=" %%A in ("%steamPath%\steamapps\appmanifest_2394010.acf") do (
    echo %%A | find /i "installdir" > nul && set "Palserver_InstallDir=%%A")
)
if exist "%steamPath%\steamapps\appmanifest_2394010.acf" (
    set "Clean_Palserver_InstallDir=!Palserver_InstallDir:installdir=!"
    set "Clean_Palserver_InstallDir=!Clean_Palserver_InstallDir:"=!"
    set "Clean_Palserver_InstallDir=!Clean_Palserver_InstallDir: =!"
    set "Clean_Palserver_InstallDir=!Clean_Palserver_InstallDir:	=!"
    set "SERVER_ROOT=%steamPath%\steamapps\common\!Clean_Palserver_InstallDir!"
    set "SERVER_ROOT=!SERVER_ROOT:/=\!"
	echo.
	echo Palserver Directory found: !SERVER_ROOT!
) else (
    echo.
    echo Palserver Directory not found.
)

set "Clean_Palworld_InstallDir=!Palworld_InstallDir:installdir=!"
set "Clean_Palworld_InstallDir=!Clean_Palworld_InstallDir:"=!"
set "Clean_Palworld_InstallDir=!Clean_Palworld_InstallDir: =!"
set "Clean_Palworld_InstallDir=!Clean_Palworld_InstallDir:	=!"
set "WORLD_ROOT=%steamPath%\steamapps\common\!Clean_Palworld_InstallDir!"
set "WORLD_ROOT=!WORLD_ROOT:/=\!"

echo Palworld Directory found: %WORLD_ROOT%
echo.

:choice
echo Choose an option:
echo 1. Install DLL
echo 2. Download Exe Patcher
echo 9. Remove/Uninstall DLL
set /p choice="Enter your choice: "

if "%choice%"=="1" goto dll
if "%choice%"=="2" goto patcher
if "%choice%"=="9" goto uninstall

echo Invalid choice
goto choice

:dll
echo installing the dll into palworlds directory...
echo.
curl -o "%WORLD_ROOT%\Pal\Binaries\Win64\d3d9.dll" -L "https://github.com/t4bby/dll-plugin-loader/releases/download/1.0/d3d9.dll"
mkdir "%WORLD_ROOT%\Pal\Binaries\Win64\Plugins"
curl -o "%WORLD_ROOT%\Pal\Binaries\Win64\Plugins\Palpatcher.dll" -L "https://github.com/Spark-NV/Palworld-DisableBuildingRestrictions/raw/master/Patcher/DLL/Palpatcher.dll"
echo.
echo File d3d9.dll has been downloaded to "%WORLD_ROOT%\Pal\Binaries\Win64\".
echo Palpatcher has been downloaded to "%WORLD_ROOT%\Pal\Binaries\Win64\Plugins\".
echo.

if exist "%steamPath%\steamapps\appmanifest_2394010.acf" (
    echo installing the dll into palserver directory...
    echo.
    curl -o "%SERVER_ROOT%\Pal\Binaries\Win64\d3d9.dll" -L "https://github.com/t4bby/dll-plugin-loader/releases/download/1.0/d3d9.dll"
    mkdir "%SERVER_ROOT%\Pal\Binaries\Win64\Plugins"
    curl -o "%SERVER_ROOT%\Pal\Binaries\Win64\Plugins\Palpatcher.dll" -L "https://github.com/Spark-NV/Palworld-DisableBuildingRestrictions/raw/master/Patcher/DLL/Palpatcher.dll"
    echo.
    echo File d3d9.dll has been downloaded to "%SERVER_ROOT%\Pal\Binaries\Win64\".
    echo Palpatcher has been downloaded to "%SERVER_ROOT%\Pal\Binaries\Win64\Plugins\".
) else (
echo Palserver directory wasnt found, skipping palserver installation.
)

goto end

:patcher
echo downloading the patcher executable onto the desktop...
echo.
set "DESKTOP=%USERPROFILE%\Desktop"
curl -o "%DESKTOP%\BuildPatcher.exe" -L "https://github.com/Spark-NV/Palworld-DisableBuildingRestrictions/raw/master/Patcher/PythonGUI/BuildPatcher.exe"
echo BuildPatcher.exe has been downloaded to your dektop.
goto end

:uninstall
echo deleting dll files...
echo.
RMDIR /S /Q "!SERVER_ROOT!\Pal\Binaries\Win64\Plugins"
RMDIR /S /Q "!WORLD_ROOT!\Pal\Binaries\Win64\Plugins"
del "!SERVER_ROOT!\Pal\Binaries\Win64\d3d9.dll"
del "!WORLD_ROOT!\Pal\Binaries\Win64\d3d9.dll"

echo DLL files have been deleted.
goto end

:end
pause