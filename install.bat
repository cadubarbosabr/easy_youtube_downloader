@echo off
:: Check if the script is running as administrator
openfiles >nul 2>&1
if not %errorlevel%==0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Installing Python dependencies...
mkdir C:\ffmpeg
pip install -r requirements.txt

echo Downloading FFmpeg...
curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

echo Extracting FFmpeg...
mkdir C:\ffmpeg\ffmpeg-release-essentials
tar -xf ffmpeg.zip -C C:\ffmpeg\ffmpeg-release-essentials --strip-components=1

echo Setting up FFmpeg path...
set "FFMPEG_PATH=C:\ffmpeg\ffmpeg-release-essentials\bin"
setx /M PATH "%PATH%;%FFMPEG_PATH%"

echo Adding FFmpeg to current session path...
set PATH=%PATH%;%FFMPEG_PATH%

echo Cleanup...
del ffmpeg.zip

echo Installation complete.
pause
