@echo off
setlocal
cd /d "%~dp0"
title Experiment 1 - grounding map
echo.
echo  Experiment 1: which traits does the concept text carry?
echo  --------------------------------------------------------
echo  Downloads two local models the first time (about 10 GB), then runs about 630 short calls.
echo  With a graphics card this takes roughly 1 to 2 hours; on CPU only it can take much longer.
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
for %%M in (qwen2.5:7b llama3.1:8b) do (
  echo  Getting %%M ...
  ollama pull %%M
)
echo.
%PY% run_extraction.py
echo.
echo  DONE. Tell Claude it is finished.
:end
echo.
pause
