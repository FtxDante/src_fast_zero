from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    response_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response_token
    assert 'token_type' in response_token
