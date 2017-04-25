# RealBack
TDT4140 - Software Engineering

This project is a part of the subject "Software Engineering", 
and will be the final delivered software.

## Tools used in development:
- Python 3.6.0
- Django 1.10.5

## How to run the software
To run RealBack on a local server, use the following
commands after cloning our repository from github.
Our software requires that you install Python 3.6.0
or newer.

step 1 (clone repository):
```
git clone https://github.com/martinlunde/RealBack
```
step 2 (move into directory):
```
cd realback
```
step 3 (install requirements):
```
pip install -r requirements.txt
```
step 4 (run server):
```
python manage.py runserver
```
step 5 (open browser):<br/>
The server will then be running on port 8000:
http://localhost:8000

Note:
If you were not able to start the server or see any
major flaws in the program, please check if you have
correct versions of python installed and that you are
not using any version older than 3.6.


## Set up development environment

Download and install [Python 3.6.x](https://www.python.org/downloads/) (Make sure pip is selected)

Open command prompt / terminal and **navigate to git repo folder**

### For your own sanity you might want to use a virtual environment
Run `pip install virtualenv`. if (error) admin();

Run `virtualenv venv`

Run the activate script:  
`venv/bin/activate` on *nix  
`venv\Scripts\activate` on Windows

*You should now have a (venv) prompt in your terminal.*

Check python version with `python --version`  
#### If the version is wrong
Run the `deactivate` script and delete the `venv` folder.  
Rerun `virtualenv venv` with the `-p [path to correct Python version]` option.  
Examples:  
```
virtualenv -p C:\Python36\python.exe venv
virtualenv -p /usr/bin/python3.6 venv
```

### Moving on
Install required Python packages:
```
pip install -r requirements.txt
```

Run the development server:
```
python manage.py runserver
```

Code

## Changing the models
If you make changes to the `models.py` files you also need to run:
```
python manage.py makemigrations
python manage.py migrate
```

## Run tests locally
You can run the Django unittests locally with:
```
python manage.py test
```
