from os import getenv, mkdir, getcwd, sep

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

from views import *

VALID_PRINTS_PATH = getcwd() + sep + 'prints'
# mount to use static files.
app.mount(
    '/screenshot',
    StaticFiles(directory=VALID_PRINTS_PATH),
    name='prints',
)

# from whatsweb_interactions import WhatsWebAPI
# if __name__ == '__main__':
# zap = WhatsWebAPI(5511942280030, getenv('VALID_PROFILE_PATH'), headless=False)
# zap = WhatsWebAPI(getenv('VALID_PHONE_NUMBER'), headless=True)
# zap.run_browser()
# zap.get_login_code(getenv('VALID_PHONE_NUMBER'))
# zap.find_chat('Sla')
# zap.kill_browser()
