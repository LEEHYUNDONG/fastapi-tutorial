from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from router import index

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],

)

app.include_router(index.router)