import os
import pytest
from dotenv import load_dotenv
from faker import Faker
from playwright.sync_api import Browser, Page

from pages.login_page import LoginPage
from selectors.selectors import LoginSelectors

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
QA_EMAIL = os.getenv("QA_EMAIL")
QA_PASSWORD = os.getenv("QA_PASSWORD")

fake = Faker()

AUTH_FILE = "auth.json"


# ─── Auth Session ────────────────────────────────────────────────────────────
# Logs in once for the entire test session and saves the browser state.
# Every test reuses this state — no repeated logins.

@pytest.fixture(scope="session")
def auth_session(browser: Browser):
    context = browser.new_context()
    page = context.new_page()

    page.goto(BASE_URL)

    login_page = LoginPage(page)
    login_page.login(QA_EMAIL, QA_PASSWORD)

    page.wait_for_url(f"{BASE_URL}/**", timeout=10000)

    context.storage_state(path=AUTH_FILE)
    context.close()


# ─── Page ────────────────────────────────────────────────────────────────────
# Fresh page per test, auth state restored from session.
# Overrides the default pytest-playwright page fixture.

@pytest.fixture(scope="function")
def page(browser: Browser, auth_session) -> Page:
    context = browser.new_context(storage_state=AUTH_FILE)
    page = context.new_page()
    page.set_default_timeout(10000)
    yield page
    context.close()


# ─── Test Data ───────────────────────────────────────────────────────────────
# Generates unique partner data per test run.
# Timestamped name prevents collisions on the shared dev environment.

@pytest.fixture(scope="function")
def partner_data():
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_id = fake.lexify("??????").lower()

    return {
        "name": f"AutoTest Partner {timestamp}-{unique_id}",
        "phone": "+359123456789",
        "contact_person": fake.name(),
        "description": fake.sentence(nb_words=8),
        "address": "Sofia, Bulgaria",
    }