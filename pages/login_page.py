import re
from playwright.sync_api import Page, expect
from selector.selectors import LoginSelectors


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, email: str, password: str) -> None:
        self.page.locator(LoginSelectors.EMAIL_INPUT).fill(email)
        self.page.locator(LoginSelectors.PASSWORD_INPUT).fill(password)
        self.page.locator(LoginSelectors.SUBMIT_BUTTON).click()

    def assert_logged_in(self) -> None:
        expect(self.page).not_to_have_url(
            re.compile(r".*login.*"),
            timeout=10000
        )