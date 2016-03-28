# Askme backend

## Deployment with Vagrant :

- Install vagrant and virtual box on your computer.
- Create a folder named "askme_vagrant"
- Clone the project git repository inside this folder
- Copy config/bootstrap.sh and config/Vagrantfile into askme_vagrant
- Run `vagrant up` : this should create a virtual machine and install all system
dependencies required to run the development server, according to bootstrap.sh

- Once done, ssh to the vm with `vagrant ssh`

- Configure UTF-8 system wide (seems to be inneficient when scripted)
```
echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
echo "export LANG=en_US.UTF-8" >> ~/.bashrc
echo "export LANGUAGE=en_US.UTF-8" >> ~/.bashrc
source ~/.bashrc
```

- Now we need to create a database to work on.
There is a set of commands in project/config/init_postgresql.txt.
Apply manually each command in your shell.

- Create and activate the virtual environment:
`python3 -m venv amvenv`
`source ~/amvenv/bin/activate`

- Go to project folder (/vagrant/project-folder) and install the python requirements for the project:
`pip install -r requirements.txt`

- Go to the root project directory and run `pip install -r requirements.txt`

- Create and fill your own `.env` file, following the `.env.example` example in project root directory.
