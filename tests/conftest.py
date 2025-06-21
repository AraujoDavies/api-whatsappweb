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

VALID_PHONE_NUMBER = '2'
INVALID_PHONE_NUMBER = '3'
HEADLESS_CHOOSE_FOR_TEST = False   # True | False

app_on = WhatsWebAPI(
    VALID_PHONE_NUMBER, headless=HEADLESS_CHOOSE_FOR_TEST
)   # in this we need to scan QRCODE
app_off = WhatsWebAPI(
    INVALID_PHONE_NUMBER, headless=HEADLESS_CHOOSE_FOR_TEST
)   # start browser without QRCODE session


@fixture
def test_zap_on():
    return app_on


@fixture
def test_zap():
    return app_off
