from dotenv import load_dotenv
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

load_dotenv()

env = Config()

DATABASE_URL = env("DATABASE_URL", cast=str)
BOT_TOKEN = env("BOT_TOKEN", cast=str)
GSPREAD = env("GSPREAD", cast=str)
