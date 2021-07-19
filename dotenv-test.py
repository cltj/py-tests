# pip install python-dotenv
# create a .env file
# create a .gitignore file and add .env

from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

account_name = os.getenv("STORAGE_ACCOUNT_NAME")
account_password = os.getenv("STORAGE_ACCOUNT_PASSWORD")

print(account_name, account_password)
