# Simple script to install all dependencies for the askme project, and more
# generally, any Django/PGSQL project on Ubuntu server.

# First system update
sudo apt-get update

echo "#########################################################################"
echo "INSTALLING ESSENTIALS"
echo "#########################################################################"

# Git install and configuration
sudo apt-get -y install git
git config --global core.autocrlf true

echo "#########################################################################"
echo "CONFIGURING UTF-8 SYSTEM-WIDE" # http://perlgeek.de/en/article/set-up-a-clean-utf8-environment
echo "#########################################################################"

echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
echo "export LANG=en_US.UTF-8" >> ~/.bashrc
echo "export LANGUAGE=en_US.UTF-8" >> ~/.bashrc
source ~/.bashrc

# WARN : seems to be inneficient when run in bootstrap.sh but works manually

echo "#########################################################################"
echo "INSTALLING POSTGRESQL"
echo "#########################################################################"

sudo apt-get -y install postgresql
sudo apt-get -y install libpq-dev

echo "#########################################################################"
echo "INSTALLING PYTHON TOOLS"
echo "#########################################################################"

# Note that Python3.4 is already installed
sudo apt-get -y install python3-pip
sudo apt-get install python3.4-venv

echo "#########################################################################"
echo "CREATING A VIRTUALENV ENVIRONMENT"
echo "#########################################################################"

python3 -m venv venv # WARN : check write rights
