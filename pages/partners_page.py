from playwright.sync_api import Page, expect
from selector.selectors import (
    NavSelectors,
    PartnersPageSelectors,
    EditMenuSelectors,
)
from utils.config import BASE_URL


class PartnersPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        self.page.goto(f"{BASE_URL}{NavSelectors.PARTNERS_PATH}")
        expect(
            self.page.locator(PartnersPageSelectors.TABLE_ROW).first
        ).to_be_visible(timeout=10000)

    def open_create_form(self) -> None:
        self.page.locator(PartnersPageSelectors.NEW_PARTNER_BUTTON).click()

    def get_row_by_name(self, name: str):
        """Locate a table row that contains the given partner name in the NAME column."""
        return self.page.locator(
            f"{PartnersPageSelectors.TABLE_ROW}:has("
            f"{PartnersPageSelectors.NAME_COLUMN}:has-text('{name}'))"
        )

    def assert_partner_visible(self, name: str) -> None:
        """Assert a partner with the given name is visible in the partners table."""
        row = self.get_row_by_name(name)
        expect(row).to_be_visible(timeout=10000)

    def open_edit_for_partner(self, name: str) -> None:
        row = self.get_row_by_name(name)
        row.locator(PartnersPageSelectors.ACTION_BUTTON).click()
        self.page.locator(EditMenuSelectors.EDIT_BUTTON).click()
