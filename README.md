# Base-Django
<h3>Base to use Python Django</h3>
with two languages:<br>
###### for ubuntu:
```commandline
sudo apt-get install gettext
```

###### for windows:
https://mlocati.github.io/articles/gettext-iconv-windows.html

# First of all:
###### python env command
```
pip install requirements.txt

python manage.py migrate
```
copy .env-example to .env and replace a fill variables<br>
if you use vscode:<br>
  Go to File menu.<br>
  Select Preferences.<br>
  Then select Settings.<br>
  Click on small settings.json file icon in upper right corner.<br>
  copy settings.json-example-vscode and paste in settings.json

## Too to debug django
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# Deploy ------------------------------------------------------
Little steps to deploy an app django

## Creating a Server

In this case we are using a vm-ubuntu 22
but is soo much better have a vm in cloud, like azure, google cloud platform etc

### SSH Keys
###### linux command
To create ssh keys:
```commandline
ssh-keygen -t rsa -b 4096 -f PATH/NAME_KEY
```
Remember, if you are using windows, you must have a folder .ssh on folders of your user, 
it's common raise errors without it.

To use ssh key:
###### linux command
```commandline
ssh IP_HOST -i PATH/NAME_KEY
```

### First actions before deploy the project:
###### linux command
```commandline
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install curl -y
sudo apt install git
```
### Postgres as DB:
replace username with your username preference and pass with one stronger;
replace name_database too.
###### postgres command
```
sudo -u postgres psql
CREATE ROLE username WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD 'pass';
GRANT ALL PRIVILEGES ON DATABASE name_database to suporte;
\q
```
```commandline
systemctl restart postgresql
```
### Setup git
###### linux command on server
```commandline
git config --global user.name 'your name'
git config --global user.email 'your_email@domain.com'
git config --global init.defaultBranch main
ssh-keygen -t rsa -b 4096 -C "youremail@domain.com"
```
after run ssh-keygen chose a any name for repo that will be used to send project from dev
### A Transitional repo (like github).
###### linux command on server
```
mkdir -p ~/app_bare
cd ~/app_bare
git init --bare
cd ~
```

### The Repo for app
###### linux command on server
```
mkdir -p ~/app_repo
cd ~/app_repo
git init
git remote add origin ~/app_bare
git add . && git commit -m 'Initial'
cd ~
```
### git pull on app_bare
##### git dev side: 
```
git remote add app_bare NAME_CREATED_AT_SSH_KEYGEN:~/app_bare
or
git remote add app_bare user_server@DJANGO-SERVER:~/app_bare

git push app_bare <branch>
```
use properly branch instead <branch>
#### Server side:
```
cd ~/app_repo
git pull origin <branch>
```
## Create a virtual env:
```commandline
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
...more
pip install psycopg2
pip install gunicorn
```
pyscopg2 serves to PostgreSQL and python
gunicorn serves to communicate between nginx and django
### Modify env variables
##### on .env file fill the places according to demand
```commandline
cp .env-example .env
nano .env
```
## After it, we've already able to turn on the server
```commandline
python manage.py runserver
python manage.py migrate
```
... migrate to sinc database

# GUNICORN service and socket config
To install socket and service for our django project do this: <a href="./DEPLOY-SERVER-UTILS/GUNICORN SERVICE AND SOCKET.txt"> 'GUNICORN SERVICE AND SOCKET'</a>

# NGINX HTTP or HTTPS
Replace the fields __ __FIELDS__ __ according to <a href="./DEPLOY-SERVER-UTILS/NGINX-HTTP">NGINX-HTTP CONFIG</a> or <a href="./DEPLOY-SERVER-UTILS/NGINX-HTTP">NGINX-HTTP CONFIG</a>
<br>has described and do this after:
```

sudo systemctl restart ndinx
or
sudo systemctl restart project-django.socket && sudo systemctl restart project-django.serv
ice && sudo systemctl restart nginx
```