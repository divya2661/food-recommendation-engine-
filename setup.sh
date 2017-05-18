apt-get install python-numpy
pip install virtualenv
git clone "https://divn@git.shehack.go-jek.com/divn/noobs.git"
cd noobs
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
