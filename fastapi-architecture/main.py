from fastapi import FastAPI
from services.auth import router


app = FastAPI()

app.include_router(router.endpoint)
app.exception_handler()
