from playwright.sync_api import Page, expect
from selector.selectors import (
    NavSelectors,
    PartnersPageSelectors,
    EditMenuSelectors
)


class PartnersPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        from utils.config import BASE_URL
        self.page.goto(f"{BASE_URL}{NavSelectors.PARTNERS_PATH}")
        expect(
            self.page.locator(PartnersPageSelectors.TABLE_ROW).first
        ).to_be_visible(timeout=10000)

    def open_create_form(self) -> None:
        self.page.locator(PartnersPageSelectors.NEW_PARTNER_BUTTON).click()

    @staticmethod
    def partner_name_selector(name: str) -> str:
        """Build a selector that matches a partner name cell containing *name*.

        Centralises the selector pattern so tests and helpers never
        need to reference the raw ``PARTNER_NAME_CELL`` class directly.
        """
        return (
            f"{PartnersPageSelectors.PARTNER_NAME_CELL}:has-text('{name}')"
        )

    def get_row_by_name(self, name: str):
        """Return the table row locator that contains *name* in the name cell."""
        return self.page.locator(
            f"{PartnersPageSelectors.TABLE_ROW}"
            f":has({self.partner_name_selector(name)})"
        )

    def assert_partner_visible(self, name: str) -> None:
        """Assert a partner with *name* is visible in the partners table."""
        loc = self.page.locator(self.partner_name_selector(name))
        try:
            expect(loc).to_be_visible(timeout=10000)
        except AssertionError:
            raise AssertionError(
                f"Partner '{name}' was not found in the partners table"
            )

    def open_edit_for_partner(self, name: str) -> None:
        row = self.get_row_by_name(name)
        row.locator(PartnersPageSelectors.ACTION_BUTTON).click()
        self.page.locator(EditMenuSelectors.EDIT_BUTTON).click()