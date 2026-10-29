@echo off
setlocal
cd /d "%~dp0"
title Pilot 4 - style-normalised meaning test
echo.
echo  Pilot 4: restate every concept in one plain template, then embed
echo  ----------------------------------------------------------------
echo  Uses models already on this PC (no downloads). Runs unattended, roughly 20 minutes.
echo  You can close the window and double-click again later: it continues where it stopped.
echo.
where ollama >nul 2>nul
if errorlevel 1 (
  echo  Ollama was not found. Start the Ollama app, then double-click this file again.
  goto :end
)
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY ( where python >nul 2>nul && set PY=python )
if not defined PY (
  echo  Python was not found. Install Python 3 from python.org, then run this again.
  goto :end
)
%PY% run_normalize.py
echo.
echo  DONE. Tell Claude it is finished.
:end
echo.
pause
