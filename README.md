# cafe-api

Cafe-api is a Flask API application allowing to collect data for the cafes in a particular city and figure out which ones are suitable for remote-work. All data are storage in the SQL database, hence they are accessible even when server is down.

## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Run Flask

```
$ python main.py
```
In Flask, Default port is `5000`

Swagger document page:  `http://127.0.0.1:5000/`

## API Functionality Documentation:
[Documentation](https://documenter.getpostman.com/view/23649987/2s8ZDU75EM)

## Reference

Offical Websites:

- [Flask](http://flask.pocoo.org/)
- [Flask-SQLalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
