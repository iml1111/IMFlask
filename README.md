# IMFlask-Pymongo
**Boilerplate for Large Scale Flask Web Backend Structure with PyMongo (Edited 2021-06-02)**

Flask를 사용하여 대규모 어플리케이션 서버를 구축한다고 가정했을 때의 Baseline 코드입니다.

해당 코드는 Flask + Pymongo의 조합에 특화되어 있습니다.

여러 오픈 소스를 읽어보고 제 몸에 와닿는 직관적인 부분만 반영한 것이라 부족한 점이 많습니다.

피드백은 적극 환영합니다.



## Dependency

- **python 3.6+**
- **Flask==2.0.1**
- **flask-validation-extended==0.1.5**
- **pymongo==3.11.4**
- **python-dotenv==0.17.1**



## Environment variable

어플리케이션을 실행하기 위해서는 아래와 같은 환경 변수 설정이 필요합니다.

dotenv 라이브러리를 위해 config.py와 같은 경로에 .env 파일을 작성하셔도 되고, 직접 환경변수를 입력하셔도 상관없습니다.

- **<APP_NAME>_MONGODB_NAME**=MongoDB DB Name

  MongoDB 서버에 접속하기 위한 Database Name 입니다.

- **<APP_NAME>_MONGODB_URI**=MongoDB URI
  MongoDB 서버에 접속하기 위한 Database URI입니다.

- **<APP_NAME>_ERROR_LOG_PATH**=Server_Error_log Path
  에러를 기록할 별도의 로그 경로입니다.

- **FLASK_APP**="manage:application"
  Flask APP 객체의 위치를 가리키는 값입니다. 

- **FLASK_CONFIG**=Config type # development or production
  어떤 config 데이터를 주입시킬지 결정하는 값입니다.

- **FLASK_ENV**=# development or production
  어떠한 환경에서 Flask APP을 실행시킬지 결정하는 값입니다. 



## Get Started

운영체제마다 세부적인 실행방법이 다를 수 있습니다. 

```shell
# Get Repository
$ git clone https://github.com/iml1111/IMFlask-Pymongo
$ cd IMFlask-Pymongo/

# virtual env
$ python3 -m venv venv
$ source ./venv/bin/activate

# Install dependency
$ pip install -r ./requirements/requirements.txt

$ cd IMFlask/

# DB init
$ flask db-init
[IMFlask] MongoDB Initialization Completed.

# App test
$ flask test
test_app_exists (test_basics.BasicsTestCase)
Application 검증 테스트 ... ok
...

# App start
$ flask run
```

![image](https://user-images.githubusercontent.com/29897277/120597929-9d5e6800-c480-11eb-9d84-b009c3c6200f.png)



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

어플리케이션은 개발(development), 테스팅(Testing), 상용(Production) Level에서 다르게 동작해야 합니다. 따라서 실행하고자 하는 환경에 따라 config를 다르게 주입시키는 애플리케이션 팩토리를 구현했습니다.



### Flask Extension을 지양하자

Flask extension는 유용하지만 몇가지 문제가 있다고 생각했습니다.

- 몇몇 extension은 업데이트가 되지 않고 있습니다. 대표적으로 많은 Flask open source에서 사용하고 있는 **flask_script**가 그렇습니다. 
- 확실히 쓰면 편리하지만, 몇몇 package는 오히려 자체의 rule을 강요받는다는 느낌이 들었습니다.
  저의 생각과 일치하거나, 제가 직접 구현이 불가능한 수준이 아니라면 굳이 확장 패키지**(flask_moment, flask-restful 등)**를 사용하지 않았습니다.

따라서 Flask 및 Python 자체에서 기본적으로 지원하는 기능을 충실히 활용하도록 노력했습니다.
**(함께 import 되어 있는 flask-validation-extended는 제가 만든거라 넣어봤습니다 ㅎㅎ)**



### 모든 모듈은 각각 독립적으로 실행이 가능해야 한다

Api endpoint 단 함수를 제외한 **모든 Controller 및 Model들은 독립적으로 실행이 가능해야 합니다.**

따라서 대부분의 모듈에서 외부 의존성(특히 DB Connection 같은)이 발생하는 코드를 최대한 줄이고 필요할 경우, 따로 주입받을 수 있도록 구현되어 독립적으로 자유롭게 실행 및 테스트가 가능하게 하였습니다.

Api단에서 Model(DB)에 대한 의존성이 발생하는 경우, unittest 라이브러리에서 제공하는 Mocking을 통해 테스트단에서 원할한 실행이 가능하도록 합니다. 




### 저수준의 DB 드라이버를 사용하자

모든 DB단 연동 코드에는 **ORM, ODM과 같은 Database Abstraction Module을 사용하지 않았습니다.**

당연히 Large Scale이라면, Abstraction을 사용하는게 보편적이지만, 저는 공부하는 입장에서 제가 직접 DB까지 전달되는 처리를 가능한 한 자세하게 관여할 수 있도록 구조를 구현하였습니다.

또한 저 자신이 공부가 부족해서인지 아직, 이러한 Abstraction에 대한 중요성이 와닿지 않아서 적용시키지 않았습니다.



### 딱히 REST API는 아닙니다

제가 들은 지식을 바탕으로 가능한한 RESTful스럽게 구현을 해보긴 했습니다만, 역시나 얕게 들은 지식인 만큼 완전하지 않습니다. 다만, 적어도 아래와 같은 규약을 적용해보았습니다.

- 모든 API는 **GET, POST, PUT, DELETE 내에서 규격화하여 url을 단축**시켰습니다.
- 모든 API의 **request/response의 data transfer format은 JSON으로 일관적으로 처리**하였습니다.

후에 파일 업로드 처리는 어떻게 할 것이냐는 숙제가 남아있습니다만, 이 경우 예외적으로 multipart/form-data을 활용하거나 다른 방안을 생각해봐야 할 것 같습니다.





# Directories

```
IMFlask
	├── app
	│   ├── api
	│   │   ├── decorator.py
	│   │   ├── error_handler.py
	│   │   ├── __init__.py
	│   │	│
	│   │   ├── sample_api
	│   │   │   ├── calculator.py
	│   │   │   ├── info.py
	│   │   │   └── __init__.py
	│   │	│	
	│   │   └── template.py
	│   │	
	│   ├── asset
	│   │   └── index.html
	│   │
	│   └── __init__.py
	│
	├── config.py
	│
	├── controller
	│   ├── calculator.py
	│   ├── __init__.py
	│   └── util.py
	│
	├── manage.py
	│
	├── model
	│   ├── __init__.py
	│   └── mongodb
	│       ├── base.py
	│       ├── __init__.py
	│       ├── log.py
	│       └── master_config.py
	│
	└── tests
	    ├── __init__.py
	    ├── mock.py
	    ├── test_basics.py
	    ├── test_calc.py
	    └── test_info.py

```

- **manage.py**

flask 웹 어플리케이션을 실행시키기 위한 메인 코드입니다. flask application 객체를 생성하고, 각종 shell context 설정 및 cli command 설정을 담당합니다.

- **config.py**

어플리케이션 구동시, 환경변수를 기반으로 Config를 작성하는 코드입니다. 상황에 맞게 적절한 config를 app 객체에 주입할 수 있도록 합니다.

- **app/__ init __.py**

어플리케이션의 중심이 되는 application 객체를 생성하는 곳입니다. 입력된 인자를 바탕으로 각 환경에 맞는 config를 주입하고, flask extension 및 초기 설정 초기화 및 app/api/에 있는 코드를 불러와 URL mapping을 수행합니다.

- **app/asset**

template 및 static 파일을 다루는 경로입니다. flask structure 자체에는 직접적인 연관이 없기 때문에, 일단 비워놓았습니다.

- **app/api/**

application 객체에 등록한 Blueprint 및 각종 route 함수를 다루고 있습니다. 

1. 해당 api 카테고리의 요구사항이 작을 경우, **auth.py**와 같이 단일 파일로 다룰 수 있습니다.
2. 만약 요구사항이 많을 경우, **app/api/v1/**의 형태로 내부를 더 구조화하여 다룰 수 있습니다.
3. **errors.py**는 각종 에러 핸들러를 관리합니다.
4. **decorators.py**는 route 함수의 공통적인 기능을 묶어 커스텀 데코레이터를 구현하였습니다.
5. **template.py**는 html template을 호출하는 API들을 모아놓은 곳 입니다.

- **controller/**

본래 route(app/api/)에 다루어야 할 핵심 로직 코드를 옮겨놓은 곳입니다. 이를 통해 각 controller 함수들의 재사용성을 높일 수 있고, 단독적으로 실행하여 쉽게 디버깅을 진행할 수 있습니다. 

- **model/**

저수준의 DB 드라이버로 구현한 커스템 모델 코드입니다. DB 내의 각 collection별로 코드가 나누어져 있고, 이곳에 직접 원하는 쿼리를 작성하고 메소드별로 optimizing을 수행할 수 있습니다. 이를 통해 controller와 마찬가지로 재사용성을 높이고, 단독으로 실행하여 쉽게 디버깅을 진행할 수 있습니다.

- **model/<DB>/\_\_init\_\_.py**

모델 초기화 및 관리를 담당하는 코드입니다.

- **model/<DB>/base.py**

Collection에 대응되는 Model 클래스를 관리하기 위한 인터페이스 클래스입니다. 

- **tests/**

테스트 케이스를 관리하는 경로입니다.





