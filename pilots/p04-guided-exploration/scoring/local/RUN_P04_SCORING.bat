@echo off
setlocal
cd /d "%~dp0"
title Pilot 4 - scoring
echo.
echo  Pilot 4 scoring: embeddings and text-record check for the 40 cases
echo  -------------------------------------------------------------------
echo  Uses models already on this PC (no new downloads). Runs unattended, roughly 45 minutes.
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
%PY% run_local.py
echo.
echo  DONE. Tell Claude it is finished.
:end
echo.
pause
