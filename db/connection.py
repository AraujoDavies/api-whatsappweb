from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

engine = create_engine(getenv('DATABASE_URI'))
