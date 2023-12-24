from os import getenv
from typing import Union

from fastapi.responses import HTMLResponse, RedirectResponse
from helpers import validate_number
from main import app
from models import FindChat, SendMessage
from whatsweb_interactions import WhatsWebAPI

# run_browser
# kill_browser
# save_screenshot
# get_login_code
# find_chat
# send_message

browsers = {}

# GET
@app.get('/start')
def start_browser(
    phone_number: Union[str, None] = None,
    # token: Union[str, None] = 'WITHOUT TOKEN',
):

    if phone_number in browsers.keys():
        return f'browser already running. see: /screenshot?phone_number={phone_number}'
    try:
        zap = WhatsWebAPI(phone_number)
        zap.run_browser()
        browsers[phone_number] = zap
        browsers[phone_number].driver[0].visit(getenv('URL_WHATSAPP'))

        return f'Browser is open. see: /screenshot?phone_number={phone_number}'
    except Exception as error:
        return error


@app.get('/stop')
def stop_browser(
    phone_number: Union[str, None] = None,
    # token: Union[str, None] = 'WITHOUT TOKEN'
):
    if phone_number in browsers.keys():
        kill = browsers[phone_number].kill_browser()
        browsers.pop(phone_number)
        return kill

    return 'Browser is not instanciated'


@app.get('/screenshot', response_class=HTMLResponse)
def get_screenshot(phone_number: Union[str, None] = None, title: str = ''):
    # return '<h2> test </h2>'
    if phone_number is None:
        return '<h3>Please input some phone number.</h3>'
    if phone_number in browsers.keys():
        if browsers[phone_number].save_screenshot() is True:
            loc_print = f'screenshot/user_{phone_number}.png'
            return f'<h1> {title} </h1> <img src="{loc_print}" alt="file not found.">'
        return '<h3>printscreen failed</h3>'
    return '<h3>Browser is not instanciated</h3>'


@app.get('/browsers')
def browsers_in_execution():
    browser_open = [phone for phone in browsers.keys()]
    return browser_open


@app.post('/find-chat')
def find_chat(body_find_chat: FindChat):
    if body_find_chat.phone_number in browsers.keys():
        find_chat_response = browsers[body_find_chat.phone_number].find_chat(
            body_find_chat.chat_name
        )

        if find_chat_response == 'Search bar not found.':
            return f'Are you scanned the QRCODE ? see: /screenshot?phone_number={body_find_chat.phone_number}'

        return find_chat_response
    return 'Browser is not instanciated'


@app.post('/send-message')
def find_chat(body: SendMessage):
    if body.phone_number in browsers.keys():
        return browsers[body.phone_number].send_message(body.message)
    return 'Browser is not instanciated'
