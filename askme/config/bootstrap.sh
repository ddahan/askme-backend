# Simple script to install all dependencies for the askme project, and more
# generally, any Django/PGSQL project on Ubuntu server.

# First system update
sudo apt-get update

echo "INSTALLING ESSENTIALS"
# Git install and configuration
sudo apt-get -y install git
git config --global core.autocrlf true

echo "INSTALLING POSTGRESQL"
sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

echo "INSTALLING PYTHON TOOLS"
sudo apt-get install python3.5
sudo apt-get -y install python-setuptools python-dev build-essential

echo "INSTALLING VIRTUALENV"
yes | easy_install pip
yes | pip install --upgrade virtualenv

echo "CREATING A VIRTUALENV ENVIRONMENT AND ACTIVATE IT"
/usr/local/bin/python3.5 -m venv amvenv
source ~/amvenv/bin/activate
