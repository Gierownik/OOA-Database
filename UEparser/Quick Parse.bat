@echo off
echo Running ueparser.py
python ueparser.py
timeout /t 10 > nul
echo Running UE-DC_Parser.py
python UE-DC_Parser.py

echo Done
pause
