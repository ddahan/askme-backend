# Simple script to install all dependencies for the askme project, and more
# generally, any Django/PGSQL project on Ubuntu server.

echo "#########################################################################"
echo "SYSTEM UPDATE"
echo "#########################################################################"
sudo apt-get update

echo "#########################################################################"
echo "INSTALLING ESSENTIALS"
echo "#########################################################################"

# Git install and configuration
sudo apt-get -y install git
git config --global core.autocrlf true

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
