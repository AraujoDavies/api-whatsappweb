from os import getenv

from dotenv import load_dotenv

load_dotenv()

from whatsweb_interactions import WhatsWebAPI

if __name__ == '__main__':
    app = WhatsWebAPI(1, getenv('VALID_PROFILE_PATH'), headless=False)

    # app.run_browser()
    # app.get_login_code(getenv('VALID_PHONE_NUMBER'))
    # app.find_chat('Sla')
    # app.kill_browser()
