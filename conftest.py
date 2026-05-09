import os
import re
import pytest
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from faker import Faker
from playwright.sync_api import Browser, Page
from pages.login_page import LoginPage

load_dotenv()

BASE_URL    = os.getenv("BASE_URL")
QA_EMAIL    = os.getenv("QA_EMAIL")
QA_PASSWORD = os.getenv("QA_PASSWORD")

fake      = Faker()
AUTH_FILE = str(Path(__file__).parent / "auth.json")


@pytest.fixture(scope="session")
def auth_session(browser: Browser) -> str:
    context = browser.new_context()
    page    = context.new_page()

    page.goto(f"{BASE_URL}/")

    login_page = LoginPage(page)
    login_page.login(QA_EMAIL, QA_PASSWORD)
    login_page.assert_logged_in()

    context.storage_state(path=AUTH_FILE)
    context.close()

    return AUTH_FILE


@pytest.fixture(scope="function")
def page(browser: Browser, auth_session: str) -> Page:
    context = browser.new_context(storage_state=auth_session)
    page    = context.new_page()
    page.set_default_timeout(10000)
    yield page
    context.close()


@pytest.fixture(scope="function")
def partner_data() -> dict:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_id = fake.lexify("??????").lower()
    return {
        "name":           f"AutoTest Partner {timestamp}-{unique_id}",
        "phone":          "+359123456789",
        "contact_person": fake.name(),
        "description":    fake.sentence(nb_words=8),
        "address":        "Sofia, Bulgaria",
    }