@echo off
echo Starting CodeWarrior Arena Server...
echo.
echo This will:
echo - Start the Python Flask server
echo - Open arena.html in your browser automatically
echo - Provide backend API for game challenges
echo.
echo Press any key to start the server...
pause > nul

cd /d "%~dp0"
python backend3ds.py

echo.
echo Server stopped. Press any key to exit...
pause > nul