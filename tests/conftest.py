import logging
from code.whatsweb_interactions import WhatsWebAPI
from os import getenv

from dotenv import load_dotenv
from pytest import fixture

logging.basicConfig(
    filename='pytest_logging.log',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s: %(message)s',
)

load_dotenv()

headless_choose = False   # True | False
app_on = WhatsWebAPI(
    getenv('VALID_PHONE_NUMBER'), headless=headless_choose
)   # in this we need to scan QRCODE
app_off = WhatsWebAPI(
    getenv('INVALID_PHONE_NUMBER'), headless=headless_choose
)   # start browser without QRCODE session


@fixture
def test_zap_on():
    return app_on


@fixture
def test_zap():
    return app_off
