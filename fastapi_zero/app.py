
from http import HTTPStatus

from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.schemas import (
    MessageOutput,
    UserSchemaInput,
    UserSchemaOutput,
    UserListSchema,
)
from fastapi_zero.models import User

app = FastAPI(title='FastAPI Zero')


@app.get('/')
def read_root() -> MessageOutput:
    return {'message': 'Hello World'}


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserSchemaOutput,
)
def create_user(
    user: UserSchemaInput, session: Session = Depends(get_session)
    ):
    
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
                status_code=HTTPStatus.CONFLICT,
                detail='username already exists'
            )
        elif user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
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
)
def get_user(
        offset: int = 0, limit: int = 10,
        session: Session = Depends(get_session)) -> UserListSchema:

    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaOutput,
)
def update_user(
        user_id: int, user: UserSchemaInput,
        session: Session = Depends(get_session)):

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
            )

    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password

        session.commit()
        session.refresh(db_user)

        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email alredy exists'
            )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageOutput
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
            )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted successfully'}
