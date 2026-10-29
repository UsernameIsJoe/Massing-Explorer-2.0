@echo off
setlocal
cd /d "%~dp0"
title Pilot 4 - scoring
echo.
echo  Pilot 4 scoring: embeddings and text-record check for the 40 cases
echo  -------------------------------------------------------------------
echo  Downloads one embedding model the first time (about 2.5 GB), then runs unattended, roughly 50 minutes.
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
echo  Getting qwen3-embedding:4b ...
ollama pull qwen3-embedding:4b
echo.
%PY% run_local.py
echo.
echo  DONE. Tell Claude it is finished.
:end
echo.
pause
