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
        'email': 'test@test.com'
        }
    

def test_read_users_no_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    response = client.get('/users/')

    user_schema = UserSchemaOutput.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'updated_test',
            'email': 'email@email.com',
            'password': 'updated_test',
        })

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'updated_test',
        'email': 'email@email.com',
        }


def test_update_non_existent_user(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'non_existent',
            'email': 'no@exists.com',
            'password': 'non_existent',
        })
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.json() == {'message': 'User deleted successfully'}
