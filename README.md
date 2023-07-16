# Flask Application with SQLite3

## Commands
### Start venv
`.env\Scripts\activate.bat`

### Run App
`flask --app flaskr run --debug`

### Init Database
`flask --app flaskr init-db`


### Install testing 
pip install pytest coverage


## After Development and Testing
### Build and install
```
$ pip install build
$ python -m build --wheel
```

You can find the file in dist/flaskr-1.0.0-py3-none-any.whl. The file name is in the format of {project name}-{version}-{python tag} -{abi tag}-{platform tag}.

Copy this file to another machine, set up a new virtualenv, then install the file with pip.

```
pip install flaskr-1.0.0-py2.py3-none-any.whl
```

Pip will install your project along with its dependencies.
Since this is a different machine, you need to run init-db again to create the database in the instance folder.

```
$ flask --app flaskr init-db
```

### Configure the Secret Key
In the beginning of the tutorial that you gave a default value for SECRET_KEY. This should be changed to some random bytes in production. Otherwise, attackers could use the public 'dev' key to modify the session cookie, or anything else that uses the secret key.

You can use the following command to output a random secret key:

```
$ python -c 'import secrets; print(secrets.token_hex())'
```

```
(.venv) D:\code\test>python -c "import secrets; print(secrets.token_hex())"     
110943200992fd3ca5fb88a27794016c24ab4aece42fc5538cc964bc173cdd0a
```

Create the config.py file in the instance folder, which the factory will read from if it exists. Copy the generated value into it.

.venv/var/flaskr-instance/config.py
SECRET_KEY = '110943200992fd3ca5fb88a27794016c24ab4aece42fc5538cc964bc173cdd0a'
You can also set any other necessary configuration here, although SECRET_KEY is the only one needed for Flaskr.

### Run with a Production Server
When running publicly rather than in development, you should not use the built-in development server (flask run). The development server is provided by Werkzeug for convenience, but is not designed to be particularly efficient, stable, or secure.

Instead, use a production WSGI server. For example, to use Waitress, first install it in the virtual environment:

$ pip install waitress
You need to tell Waitress about your application, but it doesn’t use --app like flask run does. You need to tell it to import and call the application factory to get an application object.

$ waitress-serve --call "flaskr:create_app"

Serving on http://0.0.0.0:8080