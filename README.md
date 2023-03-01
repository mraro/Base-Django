# Base-Django
Base to use Python Django

# First of all:
in env:
```
pip install requirements.txt
```
```
python manage.py migrate
```
copy .env-example to .env and replace a fill variables<br>
if you use vscode:<br>
  Go to File menu.<br>
  Select Preferences.<br>
  Then select Settings.<br>
  Click on small settings.json file icon in upper right corner.<br>
  copy settings.json-example-vscode and paste in settings.json<br>


# Deploy
little steps to deploy an app django

## Creating a Server

In this case we are using a vm-ubuntu 22
but is soo much better have a vm in cloud, like azure, google cloud platform etc

### SSH Keys

To create ssh keys:
```
ssh-keygen -t rsa -b 4096 -f PATH+NAME_KEY
```
Remember, if you are using windows, you must have a folder .ssh on folders of your user, 
it's common raise errors without it.

To use ssh key:

```
ssh IP_HOST -i PATH+NAME_KEY
```

### First actions before deploy the project:

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git
```
