from dataclasses import asdict
from typing import Optional
import uvicorn
from fastapi import FastAPI
from common.config import conf
from routes import index
from database.conn import db


def create_app():
    """앱 함수 실행"""
    c = conf()
    app = FastAPI()
    conf_dic = asdict(c)
    db.init_app(app, **conf_dic)
    # 데이터베이스 이니셜라이즈
    # 레디스 이니셜라이즈
    # 미들웨어 정의
    # 라우터 정의
    app.include_router(index.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)