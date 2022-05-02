<img width="600" alt="KakaoTalk_Photo_2022-05-02-23-21-00" src="https://user-images.githubusercontent.com/29897277/166250424-81f61df5-b05a-428f-a4cc-68ee74cb6ac0.png">

# IMFlask

**Boilerplate for Large Scale Flask Web Backend Structure (Edited 2022-05-03)**

Flask를 사용하여 대규모 어플리케이션 서버를 구축한다고 가정했을 때의 Baseline 코드입니다.

여러 오픈 소스를 읽어보고 제 몸에 와닿는 직관적인 부분만 반영한 것이라 부족한 점이 많습니다.

피드백은 적극 환영합니다.

## Dependency

- python 3.6+

- Flask==2.1.2
- flask-validation-extended==0.1.7
- python-dotenv==0.20.0

## Environment variables

어플리케이션을 실행하기 위해서는 아래와 같은 환경 변수 설정이 필요합니다.

dotenv 라이브러리를 위해 config.py와 같은 경로에 .env 파일을 작성하셔도 되고, 직접 환경변수를 입력하셔도 상관없습니다.

```shell
FLASK_APP=manage:application
FLASK_ENV=development
FLASK_CONFIG=development
```

## Get Started

운영체제마다 세부적인 실행방법이 다를 수 있습니다. 

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

app/\__init\__.py에서 Flask Extend 라이브러리를 적용할 수 있습니다.

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

어플리케이션은 개발(development), 테스팅(Testing), 상용(Production) Level에서 다르게 동작해야 한다.

### Flask Extension을 지양하자

Flask extension는 최대한 지양하고 Basic Python 기반으로 기능을 충실히 구현하자.

하지만, [flask-validation-extended](https://github.com/iml1111/flask-validation-extended)는 좋은 라이브러리입니다. :)

### 의존성 분리

Api endpoint 단 함수를 제외한 **모든 Controller 및 Model들은 독립적으로 실행이 가능해야 한다.**


### 저수준의 DB 드라이버를 사용하자

모든 DB단 연동 코드에는 **ORM, ODM과 같은 Database Abstraction Module을 사용하지 말자.**

### 할 수 있는 만큼 RESTful를 지향하자

가능한한 RESTful스럽게 가져가되, 무리하지는 말자.

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





