from http import HTTPStatus


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


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{
        'username': 'test',
        'email': 'test@test.com',
        'id': 1,
    },]}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'updated_test',
            'email': 'email@email.com',
            'password': 'updated_test',
        })

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'updated_test',
        'email': 'email@email.com',
        }


def test_update_non_existent_user(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'non_existent',
            'email': '',
            'password': 'non_existent',
        })
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.json() == {'message': 'User deleted successfully'}
