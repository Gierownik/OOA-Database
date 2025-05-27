@echo off
echo Running ueparser.py
python ueparser.py
timeout /t 1 > nul
echo Running UE-DC_Parser.py
python UE-DC_Parser.py

echo Done
pause
