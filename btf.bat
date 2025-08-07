@echo off
cd /d "%~dp0"

REM 
call venv\Scripts\activate

REM 
echo Vamos ligar o Delorean...

REM 
py painel.py

echo.
echo Delorean ligado. Pressione qualquer tecla para continuar...
pause

REM 
deactivate

REM 
echo.
echo Pressione qualquer tecla para fechar...
pause
