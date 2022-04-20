# fastapi-tutorial
> FastAPI docs 

<br><br>

## Install requirements.txt

`run`

```python
pip install -r requirements.txt
```

`gets`
```python
anyio==3.5.0
asgiref==3.5.0
click==8.1.2
fastapi==0.75.2
h11==0.13.0
idna==3.3
pydantic==1.9.0
sniffio==1.2.0
starlette==0.17.1
typing_extensions==4.2.0
uvicorn==0.17.6 
```

### Intro
```python
from typing import Optional
from fastapi import FastAPI

app = FastAPI() # API 호출

@app.get("/") # root url
def read_root(): # root에 해당 dict 보여준다.
    return {"Hello" : "World"}

@app.get("/items/{item_id}") # url 정보
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id" :item_id, "q" : q}
```

- put요청 json으로 읽음, 각각의 데이터 타입이 일치하는지 검사
- get, put 요청에 item_id가 경롤에 있는지 검증
- get, put 요청에 item_id 데이터 타입 확인
- get 요청에 q = 선택적인 쿼리 매개 확인 (None-선택사항, None없음-필수사항)

<br><br>

### pydantic-tutorial
- ujson
    - 빠른 json 파싱
- email_validator
    - 이메일 유효성 검사


```python
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel): # 좀 더 복잡한 모델
    name :str
    price :float
    is_offer : Optional[bool] = None # None이 아니면 필수 사항이다.

...

@app.put("/items/{item_id}")
def update_item(item_id : int, item: Item):
    return {"item_name": item.name, "item_id":item_id}
```

`매개변수 타입, 본문 등을 함수 매개변수로 한번에 선언 ex) item_id : int`

`복잡한 모델 선언 ex) item: Item //객체 형태로 넘겨준다.`

- 위와 같은 선언으로 얻은 것
    - 편집기 지원 
        - 자동완성
        - 타입검사
    - 데이터 검증
        - 데이터가 유효하지 않을 때 자동으로 생성하는 명확한 에러
        - 중첩된 json 객체에 대한 유효성 검사
    - 입력 데이터 변환 - 네트워크에서 파이썬 데이터 및 타입으로 전송.
        - json
        - 경로 매개변수
        - 쿼리 매개변수
        - 쿠키
        - 헤더
        - 폼
        - 파일
    - 출력 데이터 변환 - 파이썬 데이터 및 타입을 네트워크 데이터로 전환(json)
        - 파이썬 타입 변환
        - datetime 객체
        - uuid
        - 데이터베이스 모델
pydantic은 타입 어노테이션을 사용한 데이터 검증 도구이다. 추가적인 validation, nested validation 등 가능하며 속도도 빠르다. validation 성능 drf비해 12배 빠름. 유효하지 않은 타입에 한해서 에러를 발생시켜준다.

[pydantic reference1](https://fastapi.tiangolo.com/ko/)
[pydantic reference2](https://wookkl.tistory.com/62)