
CREATE FLASK APP
================

This utility is answer on my personal demand. Creating repository and building all flask project
dependencies from scratch for every new project is time consumming and boring. Install this package,
call ``create-flask-application`` utility, answer basic questions and enjoy your new project.


Installation
^^^^^^^^^^^^
To install ``create-flask-application`` utility, just type:

```
$ pip install create-flask-application
```

This module is only available for **python3** (for now).


Usage
^^^^^

In your console, type:
```
$ create-flask-application
```

You will be asked few questions. A new directory will be created inside 
your CWD. Its name is the same as you specified answering first question about project name.

``create-flask-application`` will spawn templates with:
 - basic rest api implementation
 - optional flask-mail support
 - optional socketio support
 - wsgi application config
 - general application config with random generated secret key
 - optional sqlalchemy initial setup



Limitations
^^^^^^^^^^^

``create-flask-application`` will:
 - create project directory
 - create virtualenv directory called *venv*
 - install all required python dependencies
 - render all requiered code templates
 - spawn basic *gitignore* file

``create-flask-application`` will **not**:
 - create git repository
 - work under python 2
 - support databases other than **postgresql** with **psycopg2** driver (I will update it to all databases supported by sqlalchemy soon)

Note that you have to have **python3-venv** installed.
