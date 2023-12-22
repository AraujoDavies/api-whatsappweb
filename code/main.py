from os import getenv

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from whatsweb_interactions import WhatsWebAPI

if __name__ == '__main__':
    zap = WhatsWebAPI(1, getenv('VALID_PROFILE_PATH'), headless=False)

    # zap.run_browser()
    # zap.get_login_code(getenv('VALID_PHONE_NUMBER'))
    # zap.find_chat('Sla')
    # zap.kill_browser()
