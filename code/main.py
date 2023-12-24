from os import getenv

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from whatsweb_interactions import WhatsWebAPI

app = FastAPI()

from views import *

# mount to use static files.
app.mount('/screenshot', StaticFiles(directory='prints'), name='prints')

# if __name__ == '__main__':
# zap = WhatsWebAPI(5511942280030, getenv('VALID_PROFILE_PATH'), headless=False)
# zap = WhatsWebAPI(getenv('VALID_PHONE_NUMBER'), headless=True)
# zap.run_browser()
# zap.get_login_code(getenv('VALID_PHONE_NUMBER'))
# zap.find_chat('Sla')
# zap.kill_browser()
