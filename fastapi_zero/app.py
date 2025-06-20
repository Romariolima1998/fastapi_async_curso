from http import HTTPStatus

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    MessageOutput,
    Token,
    UserListSchema,
    UserSchemaInput,
    UserSchemaOutput,
)
from fastapi_zero.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)


app = FastAPI(title='FastAPI Zero')


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )
    
    accsses_token = create_access_token(
        {'sub': user.email}
        )
    
    return {'access_token': accsses_token, 'token_type': 'Bearer'}


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
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='username already exists',
            )
        elif user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='email already exists'
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
)
def get_users(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserListSchema:
    users = session.scalars(select(User).limit(limit).offset(offset))

    return {'users': users}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaOutput,
)
def update_user(
    user_id: int,
    user: UserSchemaInput,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)

        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email alredy exists',
        )


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=MessageOutput
)
def delete_user(
    user_id: int, session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted successfully'}
