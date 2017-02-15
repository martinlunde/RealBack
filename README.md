# RealBack
TDT4140 - Software Engineering

This project is a part of the subject "Software Engineering", 
and will be the final delivered software.

## Tools used in development:
- Python
- Django

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

Rund the development server:
```
python manage.py runserver
```
