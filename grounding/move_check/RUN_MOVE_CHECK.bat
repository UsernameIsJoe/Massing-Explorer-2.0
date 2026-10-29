@echo off
setlocal
cd /d "%~dp0"
title Move check - embeddings
echo.
echo  Move check: embedding about 65 short texts with the four local encoders.
echo  No downloads. About 2 minutes.
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
%PY% embed.py
echo.
echo  DONE. Tell Claude it is finished.
:end
echo.
pause
