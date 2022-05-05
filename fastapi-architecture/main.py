from fastapi import FastAPI
from services.auth import router
from services.auth.utility import NotAuthenticatedException, not_authenticated_exception_handler


app = FastAPI()

app.include_router(router.endpoint)
app.add_exception_handler(NotAuthenticatedException,not_authenticated_exception_handler)
