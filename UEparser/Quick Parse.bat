@echo off
echo Running ueparser.py
python ueparser.py
timeout /t 1 > nul
echo Running UE-DC_Parser.py
python UE-DC_Parser.py
timeout /t 1 > nul
echo Running the_parser.py
python the_parser.py

echo Done
pause
