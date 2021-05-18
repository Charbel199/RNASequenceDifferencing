@echo off
title RNA Sequence Differencing
echo Starting ...
echo IR or TED
set /P program=Enter mode:
if "%program%"=="IR"  goto IR
if "%program%"=="TED"  goto TED
goto wronginput
:IR
cd IR
goto pythonlogic
:TED
cd TED
goto pythonlogic



:pythonlogic
python gui.py
goto end

:wronginput
echo Wrong input





:end



