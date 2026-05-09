from playwright.sync_api import Page, expect
from selectors.selectors import (
    NavSelectors,
    PartnersPageSelectors,
    EditMenuSelectors
)


class PartnersPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> None:
        self.page.goto(NavSelectors.PARTNERS_PATH)
        expect(
            self.page.locator(PartnersPageSelectors.TABLE_ROW).first
        ).to_be_visible(timeout=10000)

    def open_create_form(self) -> None:
        self.page.locator(PartnersPageSelectors.NEW_PARTNER_BUTTON).click()

    def get_row_by_name(self, name: str):
        return self.page.locator(
            f"tr.ant-table-row:has(span.Cq6YF:has-text('{name}'))"
        )

    def assert_partner_visible(self, name: str) -> None:
        expect(
            self.page.locator(
                f"{PartnersPageSelectors.PARTNER_NAME_CELL}:has-text('{name}')"
            )
        ).to_be_visible(
            timeout=10000
        ), f"Partner '{name}' was not found in the partners table"

    def open_edit_for_partner(self, name: str) -> None:
        row = self.get_row_by_name(name)
        row.locator(PartnersPageSelectors.ACTION_BUTTON).click()
        self.page.locator(EditMenuSelectors.EDIT_BUTTON).click()