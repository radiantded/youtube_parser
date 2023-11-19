from os import getenv

from dotenv import load_dotenv


load_dotenv()

# Youtube urls config
PATH_TO_URLS = './urls.json'

# db config
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
