#!/usr/bin/bash

python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd simple_chat
python manage.py makemigrations chat
python manage.py migrate
python manage.py runserver