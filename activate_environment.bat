@echo off
echo === Creando entorno virtual...
python -m venv .venv

echo === Activando entorno virtual...
call .venv\Scripts\activate

echo === Instalando dependencias...
pip install -r requirements.txt

echo === Iniciando el programa...
python gui.py

pause
