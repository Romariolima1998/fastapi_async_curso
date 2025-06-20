from http import HTTPStatus

from fastapi_zero.schemas import UserSchemaOutput


def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
    }


def test_read_users(client, user, token):
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'}
        )

    user_schema = UserSchemaOutput.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'updated_test',
            'email': 'email@email.com',
            'password': 'updated_test',
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'updated_test',
        'email': 'email@email.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
)

    assert response.json() == {'message': 'User deleted successfully'}


def test_jwt_with_token_invalid(client, user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer token_invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.password_clean, }
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token


