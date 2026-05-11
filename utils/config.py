import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
QA_EMAIL = os.getenv("QA_EMAIL")
QA_PASSWORD = os.getenv("QA_PASSWORD")
