
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy import select

from fastapi_zero.schemas import (
    MessageOutput,
    UserSchemaInput,
    UserSchemaOutput,
    UserListSchema,
)
from fastapi_zero.models import User

app = FastAPI(title='FastAPI Zero')

database = []


@app.get('/')
def read_root() -> MessageOutput:
    return {'message': 'Hello World'}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaOutput,
)
def create_user(user: UserSchemaInput):
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine

    from fastapi_zero.settings import settings

    engine = create_engine(settings.DATABASE_URL)
    session = Session(engine)

    user_db = session.scalar(
        select(User).where(
            (User.username == user.username)
            |
            (User.email == user.email)
        )
    )

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='username already exists'
            )
        elif user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email already exists'
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserListSchema,
)
def get_user():
    
    

    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaOutput,
)
def update_user(user_id: int, user: UserSchemaInput):
    for db_user in database:
        if db_user['id'] == user_id:
            db_user.update(user.model_dump())
            return db_user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail='User not found'
        )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageOutput
)
def delete_user(user_id: int):
    global database
    database = [user for user in database if user['id'] != user_id]
    if not any(user['id'] == user_id for user in database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )
    return {'message': 'User deleted successfully'}
