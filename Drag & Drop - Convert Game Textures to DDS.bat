@echo off
for %%F in (%*) do (
    python "%~dp0DIRT5-ONRUSH_convert_Game2DDS.py" %%F
)

pause