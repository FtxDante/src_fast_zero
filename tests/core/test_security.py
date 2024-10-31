from http import HTTPStatus

from jwt import decode

from fast_zero.core.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, ALGORITHM)

    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'message': 'Could not validate credentials'}


def test_jwt_invalid_sub_email(client):
    jwt_fields = {'sub': ''}
    invalid_jwt = create_access_token(jwt_fields)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {invalid_jwt}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'message': 'Could not validate credentials'}


def test_jwt_invalid_sub_email_that_doesnt_exists(client):
    jwt_fields = {'sub': 'exemple@example.com'}
    invalid_jwt = create_access_token(jwt_fields)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {invalid_jwt}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'message': 'Could not validate credentials'}
