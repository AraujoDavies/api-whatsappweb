from code.main import app
from os import getenv

import pytest
from fastapi.testclient import TestClient

VALID_PHONE_NUMBER = '2'


def test_if_print_doesnt_works_without_browser():
    with TestClient(app) as ac:
        response = ac.get(
            f'/screenshot?phone_number={VALID_PHONE_NUMBER}'
        )
    assert '<h3>Browser is not instanciated</h3>' in response.text


@pytest.mark.apitest
def test_stop_route_without_open_browser():
    with TestClient(app) as ac:
        response = ac.get(f'/stop?phone_number={VALID_PHONE_NUMBER}')
    assert 'Browser is not instanciated' in response.text


@pytest.mark.apitest
def test_start_route():
    with TestClient(app) as ac:
        response = ac.get(
            f'/start?phone_number={VALID_PHONE_NUMBER}'
        )
    assert (
        'Browser is open.' in response.text
        or 'browser already running' in response.text
    )


@pytest.mark.apitest
def test_browsers_instacited():
    with TestClient(app) as ac:
        response = ac.get('/browsers')
    assert f'["{VALID_PHONE_NUMBER}"]' in response.text


@pytest.mark.apitest
def test_if_screenshot_works_like_hoped():
    with TestClient(app) as ac:
        response = ac.get(
            f'/screenshot?phone_number={VALID_PHONE_NUMBER}'
        )
    assert (
        f'<h1>  </h1> <img src="screenshot/user_{VALID_PHONE_NUMBER}.png" alt="file not found.">'
        in response.text
    )


@pytest.mark.apitest
def test_if_find_chat_and_if_message_is_sended():
    with TestClient(app) as ac:
        findchat = ac.post(
            '/find-chat',
            json={
                'phone_number': VALID_PHONE_NUMBER,
                'chat_name': getenv('VALID_CHAT_NAME'),
            },
        )
        sendmessage = ac.post(
            '/send-message',
            json={
                'phone_number': VALID_PHONE_NUMBER,
                'message': 'pytest.',
            },
        )
        stop = ac.get(
            f'/stop?phone_number={VALID_PHONE_NUMBER}'
        )   # para nao perder sessão do whats.
    assert 'Chat found.' in findchat.text
    assert 'Message sended' in sendmessage.text
    assert 'Browser killed' in stop.text
