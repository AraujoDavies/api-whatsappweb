from code.whatsweb_interactions import WhatsWebAPI
from os import getenv

from dotenv import load_dotenv
from pytest import fixture

load_dotenv()

app = WhatsWebAPI(1, getenv('VALID_PROFILE_PATH'))
print(getenv('VALID_PROFILE_PATH'))


@fixture
def test_app():
    return app
