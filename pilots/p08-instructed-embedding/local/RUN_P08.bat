@echo off
setlocal
cd /d "%~dp0"
title Pilot 8 - embeddings
echo.
echo  Pilot 8: embed 140 short texts with qwen3-embedding:4b
echo  ---------------------------------------------------------------
echo  No downloads. Takes a few minutes. Safe to run again: it continues where it stopped.
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
  echo  Python was not found.
  goto :end
)
%PY% run_local.py
echo.
echo  DONE. Attach local\embeddings.jsonl in the chat with Claude.
:end
echo.
pause
