@echo off
mkdir venv
python -m venv venv
call venv\Scripts\activate
python -m pip install pip-tools python-dotenv
python -m pip install pip-tools python-dotenv
call install