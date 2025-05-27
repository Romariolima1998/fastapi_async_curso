
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from fastapi_zero.schemas import (
    MessageOutput,
    UserSchemaInput,
    UserSchemaOutput,
    UserListSchema,
)

app = FastAPI(title='FastAPI Zero', version='0.1.0')

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
    user_dict = user.model_dump()
    user_dict['id'] = len(database) + 1
    database.append(user_dict)

    return user_dict


@app.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserListSchema,
)
def get_user():
    return {'users': database}


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
    status_code=HTTPStatus.NO_CONTENT,
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