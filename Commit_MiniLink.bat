@echo off
REM =============================
REM Script para subir MiniLink no GitHub
REM =============================

REM Caminho do projeto (altere se necessário)
cd C:\Users\marci\Desktop\minilink

REM Adiciona todos os arquivos
git add .
git reset Commit_MiniLink.bat.bat

REM Pede mensagem de commit
set /p msg="Digite a mensagem do commit: "

REM Faz commit
git commit -m "%msg%"

REM Seta branch principal como main
git branch -M main

REM Conecta ao repositório remoto (troque SEU_USUARIO)
git remote add origin https://github.com/samelfero/MiniLink.git 2>nul

REM Faz push para o GitHub
git push -u origin main

echo.
echo =============================
echo Push concluído!
pause
