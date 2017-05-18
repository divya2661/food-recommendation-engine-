Requirements:
1. Python2.7

Setup virtual environment
pip install virtualenv
git clone "repolink"
cd repo
---inside repo---
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
