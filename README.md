<img width="600" alt="KakaoTalk_Photo_2022-05-02-23-21-00" src="https://user-images.githubusercontent.com/29897277/166250424-81f61df5-b05a-428f-a4cc-68ee74cb6ac0.png">

# IMFlask

**Boilerplate for Large Scale Flask Web Backend Structure (Edited 2022-05-03)**

This is boilerplate, assuming you are building a large-scale application server using `Flask`.

I look forward to your feedback.



If you use Mongodb with `pymongo`, I recommend this.

- [IMFlask-Pymongo](https://github.com/iml1111/IMFlask-Pymongo)



## Dependency

- python 3.6+

- Flask >= 2.1.2
- flask-validation-extended >= 0.1.7
- python-dotenv >= 0.20.0

## Environment variables

To run the application, you need to set the following environment variables.  

For the dotenv library, you can write an `.env` file in the same path as `config.py`, or you can directly enter an environment variable.

```shell
FLASK_APP=manage:application
FLASK_ENV=development
FLASK_CONFIG=development
```

## Get Started

```shell
# Get Repository
$ git clone https://github.com/iml1111/IMFlask
$ cd IMFlask/

# virtualenv
$ python3 -m venv venv
$ source ./venv/bin/activate

# Install dependency
$ pip install -r ./requirements/requirements.txt
$ cd IMFlask/

# App test
$ flask test
test_app_exists (test_basics.BasicsTestCase)
Application 검증 테스트 ... ok
...

# App start
$ flask run
```

## Flask Extended Example

You can apply the Flask Extend library in `app/__init__.py`.

```python
...
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt_manager = JWTManager()
cors = CORS()
...

def create_app(config):
	  ...
	  jwt_manager.init_app(app)
    cors.init_app(app)
    ...
```

# Concept

### Application Factory

Applications should operate differently at development, testing, and production levels.

### Avoid Flask Extension

Avoid Flask extension as much as possible and implement feature based on Basic Python.

However, [flask-validation-extended](https://github.com/iml1111/flask-validation-extended) is a good library. :)

### Dependency Separation

All Controllers and Models must be independently executable except for API endpoint functions.


### No Database Abstraction

Do not use Database Abstraction Module such as ORM or ODM for all DB interface code.

### RESTful friendly

Take it as RESTful as possible, but don't overdo it.

# Directories

```
IMFlask
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── decorator.py
│   │   ├── error_handler.py
│   │   ├── response.py
│   │   ├── sample_api
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   ├── template.py
│   │   └── validation.py
│   └── asset
│       └── index.html
├── config.py
├── controller
│   ├── __init__.py
│   ├── calculator.py
│   ├── log.py
│   └── util.py
├── manage.py
├── model
│   ├── __init__.py
└── tests
    ├── __init__.py
    ├── mock.py
    ├── test_basics.py

```





