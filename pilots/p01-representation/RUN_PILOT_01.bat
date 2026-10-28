@echo off
setlocal
cd /d "%~dp0"
title Pilot 01 - embeddings
echo.
echo  Pilot 01: embedding run
echo  -----------------------
echo  This downloads four Ollama models (first time only) and embeds the pilot texts.
echo  Leave this window open until it says DONE.
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

for %%M in (nomic-embed-text mxbai-embed-large bge-m3 qwen3-embedding:0.6b) do (
  echo  Downloading %%M ...
  ollama pull %%M
)

echo.
echo  Embedding texts ...
%PY% scripts\run_embeddings.py > runs_console.txt 2>&1
type runs_console.txt
echo.
echo  DONE. Tell Claude it is finished.

:end
echo.
pause
