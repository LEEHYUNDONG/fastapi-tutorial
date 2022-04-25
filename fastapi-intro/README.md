
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

