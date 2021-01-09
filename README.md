# IMFlask
**Large Scale Web Backend Structure for Flask (Edited at 2020-09-25)** 

공부하는 내용을 정리하는 겸, Flask를 사용하여 대규모 어플리케이션 서버를 구축한다고 가정했을 때의 baseline 코드를 구현한 것입니다. 

여러 오픈 소스를 읽어보고 제 몸에 와닿는 직관적인 부분만 반영한 것이라 부족한 점이 많습니다.

피드백은 적극적으로 환영합니다.



## TO DO 
- 커버리지 적용하기
- 인스턴스 사용해보기

# Concept



### Application Factory

어플리케이션은 개발(development), 테스팅(Testing), 상용(Production) Level에서 다르게 동작해야 합니다. 따라서 실행하고자 하는 환경에 따라 config를 다르게 주입시키는 애플리케이션 팩토리를 구현했습니다.



### Flask Extension을 지양하자

Flask extension는 유용하지만 몇가지 문제가 있다고 생각했습니다.

- 몇몇 extension은 업데이트가 되지 않고 있습니다. 대표적으로 많은 Flask open source에서 사용하고 있는 **flask_script**가 그렇습니다. 
- 확실히 쓰면 편리하지만, 몇몇 package는 오히려 자체의 rule을 강요받는다는 느낌이 들었습니다.
  저의 생각과 일치하거나, 제가 직접 구현이 불가능한 수준이 아니라면 굳이 확장 패키지**(flask_moment, flask-restful 등)**를 사용하지 않았습니다.

따라서 Flask 및 Python 자체에서 기본적으로 지원하는 기능을 충실히 활용하도록 노력했습니다.



### 저수준의 DB 드라이버를 사용하자

해당 코드는 RDBMS, NoSQL(Document based, Key-value based) 등의 **총 3가지의 DB(MySQL, MongoDB, Redis)**와 연동한 예제 코드가 작성되어 있습니다. 

단, 해당 repo는 MySQL 서버만 실행중일 경우, 실행이 가능합니다.

모든 DB단 연동 코드에는 **ORM, ODM과 같은 Database Abstraction Module을 사용하지 않았습니다.**

당연히 Large Scale이라면, Abstraction을 사용하는게 보편적이지만, 저는 공부하는 입장에서 제가 직접 DB까지 전달되는 처리를 가능한 한 자세하게 관여할 수 있도록 구조를 구현하였습니다.

또한 저 자신이 공부가 부족해서인지 아직, 이러한 Abstraction에 대한 중요성이 와닿지 않아서 적용시키지 않았습니다. (+사실 괜히 DB를 3개나 연결시켰나? 싶어서 수정할까 고민중입니다...)



### view 함수가 비대해지는 것을 최대한 막자

모든 웹 어플리케이션 서버는 최종적으로 api 로직을 다루는 view(혹은 route) 함수단이 핵심이 되며, 가장 코드의 양이 비대해질 수 밖에 없습니다. 따라서 최대한 해당 로직의 코드를 분할시키기 위해, View, Controller, Model로 코드의 특징을 나누어 설계하였습니다. 이럴 경우, 다음과 같은 이점이 발생합니다.

- **View(route) function**이 굉장히 심플해집니다. client 단에서 전송된 input Parameters를 받고 validate한 후, Controller 단의 function를 호출해서 반환받은 값을 return하면 끝.

- 다른 API지만, 종종 같은 query, 같은 로직을 사용하는 경우가 존재합니다. 이 경우, **controller**를 독립적으로 뽑아내서 각각의 api에 대한 재사용성을 높일 수 있습니다.

- 저수준의 DB 드라이버를 사용하는 만큼의 코드 사이사이에 query가 난무한다면 굉장히 코드에 대한 가독성이 떨어질 수 있습니다. 따라서 **커서를 인자로 받아서 동작하는 커스텀 클래스(유사 모델?)을 구현**하여, 최대한 위의 3가지를 분리시키도록 했습니다.
  
  

### 딱히 REST API는 아닙니다

제가 들은 지식을 바탕으로 가능한한 RESTful스럽게 구현을 해보긴 했습니다만, 역시나 얕게 들은 지식인 만큼 완전하지 않습니다. 다만, 적어도 아래와 같은 규약을 적용해보았습니다.

- 모든 API는 **GET, POST, PUT, DELETE 내에서 규격화하여 url을 단축**시켰습니다.
- 모든 API의 **request/response의 data tranfer format은 JSON으로 일관적으로 처리**하였습니다.

후에 파일 업로드 처리는 어떻게 할 것이냐는 숙제가 남아있습니다만, 이 경우 예외적으로 multipart/form-data을 활용하거나 다른 방안을 생각해봐야 할 것 같습니다.



# Required Environment variable

해당 WAS가 동작하기 위해서는 아래와 같은 환경 변수 설정이 필요합니다.

Windows의 경우, IMLFlask/requirements/env.bat 을 CLI에서 실행시켜 바로 일관적으로 등록할 수 있습니다.

타 OS의 경우, 같은 경로의 env.cfg의 내용을 복사하여 직접 환경 변수를 등록해주셔야 합니다.

각각의 환경 변수 정보는 다음과 같습니다.

- **FLASK_SECRET_KEY**

  JWT 인증에 사용되는 secret_key 입니다.

- **FLASK_TEST_ACCESS_TOKEN**

  테스트 프레임워크를 위한 Admin Access Token입니다.

- **FLASK_MYSQL_URI**

  MySQL 서버에 접속하기 위한 Database URI입니다.

- **FLASK_CONFIG**

  어떤 config 데이터를 주입시킬지 결정하는 값입니다. (development / production / testing)

- **FLASK_ENV**

  어떠한 환경에서 Flask APP을 실행시킬지 결정하는 값입니다. (development / production)

- **FLASK_APP**

  Flask APP 객체의 위치를 가리키는 값입니다. (manage.py의 app 변수 -> manage:app)



# Get Started

아래는 Windows 내에서 실행해볼 경우의 방법입니다. 타 OS에서도 같은 맥락으로 실행시켜주시면 됩니다.

```shell
# In Windows
$ git clone <IMFlask Repository URL>
$ cd IMFlask/

# 가상 환경 세팅
$ python3 -m venv ./venv
$ ./venv/Script/activate.bat

# 환경 변수 등록
$ ./requirements/env.bat

# DB init 및 실행
$ cd IMFlask/
$ flask db-init
$ flask run 

# App Test
$ flask test
```
![image](https://user-images.githubusercontent.com/29897277/92383059-a536e900-f148-11ea-9e3d-3168d2a48241.png)

![image](https://user-images.githubusercontent.com/29897277/92383045-9e0fdb00-f148-11ea-9808-a5f0372731d0.png)

![image](https://user-images.githubusercontent.com/29897277/92383074-a9fb9d00-f148-11ea-97c2-2c9c94efef63.png)

![image](https://user-images.githubusercontent.com/29897277/92383128-baac1300-f148-11ea-8489-4c8de69f99e5.png)

# Folder Tree

해당 코드는 다음과 같은 디렉터리 구조를 가집니다.

```
   IMFlask
		│  config.py
		│  manage.py
		│  wsgi.ini
		│  wsgi.py
		│
		├─app
		│  │  __init__.py
		│  │
		│  ├─api
		│  │  │  auth.py
		│  │  │  decorators.py
		│  │  │  errors.py
		│  │  │  template.py
		│  │  │  __init__.py
		│  │  │
		│  │  └─v1
		│  │        author.py
		│  │        __init__.py
		│  │
		│  ├─client
		│  │      __init__.py
		│  │
		│  ├─controllers
		│  │      author_con.py
		│  │      user_con.py
		│  │      __init__.py
		│  │
		│  ├─models
		│  │  │  __init__.py
		│  │  │
		│  │  ├─mongodb
		│  │  │      master_config.py
		│  │  │      user.py
		│  │  │      __init__.py
		│  │  │
		│  │  ├─mysql
		│  │  │      master_config.py
		│  │  │      tables.py
		│  │  │      __init__.py
		│  │  │
		│  │  └─redis
		│  │          redis_model.py
		│  │          __init__.py
		│  │
		│  ├─static
		│  │      __init__.py
		│  │
		│  └─templates
		│          index.html
		│          __init__.py
		│
		├─modules
		│      __init__.py
		│
		└─tests
		        test_author_api.py
		        test_auth_api.py
		        test_basics.py
		        __init__.py
```

- **manage.py**

flask 웹 어플리케이션을 실행시키기 위한 메인 코드입니다. flask application 객체를 생성하고, 각종 shell context 설정 및 cli command 설정을 담당합니다.

- **config.py**

어플리케이션 구동시, OS에 저장된 환경변수를 기반으로 Config를 작성하는 코드입니다. 상황에 맞게 적절한 config를 app 객체에 주입할 수 있도록 합니다.

- **app/__ init __.py**

어플리케이션의 중심이 되는 application 객체를 생성하는 곳입니다. 입력된 인자를 바탕으로 각 환경에 맞는 config를 주입하고, flask extension 및 초기 설정 초기화 및 app/api/에 있는 코드를 불러와 URL mapping을 수행합니다.

- **app/templates, app/static, app/client**

template 및 static 파일을 다루는 경로입니다. flask structure 자체에는 직접적인 연관이 없기 때문에, 일단 비워놓았습니다.

- **app/api/**

application 객체에 등록한 Blueprint 및 각종 route 함수를 다루고 있습니다. 

1. 해당 api 카테고리의 요구사항이 작을 경우, **auth.py**와 같이 단일 파일로 다룰 수 있습니다.
2. 만약 요구사항이 많을 경우, **app/api/v1/**의 형태로 내부를 더 구조화하여 다룰 수 있습니다.
3. **errors.py**는 각종 에러 핸들러를 관리합니다.
4. **decorators.py**는 route 함수의 공통적인 기능을 묶어 커스텀 데코레이터를 구현하였습니다.
5. **template.py**는 html template을 호출하는 API들을 모아놓은 곳 입니다.

- **app/controllers/**

본래 route(app/api/)에 다루어야 할 핵심 로직 코드를 옮겨놓은 곳입니다. 이를 통해 각 controller 함수들의 재사용성을 높일 수 있고, 단독적으로 실행하여 쉽게 디버깅을 진행할 수 있습니다. 

- **app/models/**

저수준의 DB 드라이버로 구현한 커스템 모델 코드입니다. DB 내의 각 table/collection별로 코드가 나누어져 있고, 이곳에 직접 원하는 쿼리를 작성하고 메소드별로 optimizing을 수행할 수 있습니다. 이를 통해 controller와 마찬가지로 재사용성을 높이고, 단독으로 실행하여 쉽게 디버깅을 진행할 수 있습니다.

- **/modules/**

Flask Application 외의 자체 개발된 외부 모듈을 관리하는 공간입니다. 현재는 Flask 자체와 직접적으로 연관이 없기 때문에 비워두었습니다.


# References

https://github.com/JoMingyu/Flask-Large-Application-Example

https://github.com/miguelgrinberg/flasky
