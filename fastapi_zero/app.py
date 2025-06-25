from fastapi import FastAPI

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import MessageOutput

app = FastAPI(title='FastAPI Zero')

app.include_router(auth.router)
app.include_router(users.router)


@app.get('/')
def read_root() -> MessageOutput:
    return {'message': 'Hello World'}
