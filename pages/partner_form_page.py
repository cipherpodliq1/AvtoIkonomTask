import os
from playwright.sync_api import Page, expect
from selectors.selectors import PartnerFormSelectors


class PartnerFormPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_name(self, name: str) -> None:
        self.page.locator(PartnerFormSelectors.NAME_INPUT).fill(name)

    def select_type_service(self) -> None:
        self.page.locator(PartnerFormSelectors.TYPE_DROPDOWN).click()
        self.page.locator(PartnerFormSelectors.TYPE_SERVICE_OPTION).click()

    def select_first_service(self) -> None:
        self.page.locator(PartnerFormSelectors.SERVICES_DROPDOWN).click()
        self.page.locator(PartnerFormSelectors.FIRST_DROPDOWN_OPT).first.click()
        # Close the dropdown by clicking the name field
        self.page.locator(PartnerFormSelectors.NAME_INPUT).click()

    def select_first_subscription(self) -> None:
        self.page.locator(PartnerFormSelectors.SUBSCRIPTION_DROP).click()
        self.page.locator(PartnerFormSelectors.FIRST_DROPDOWN_OPT).first.click()

    def fill_address(self, address: str) -> None:
        self.page.locator(PartnerFormSelectors.ADDRESS_INPUT).fill(address)

    def fill_phone(self, phone: str) -> None:
        self.page.locator(PartnerFormSelectors.PHONE_INPUT).fill(phone)

    def fill_contact_person(self, name: str) -> None:
        self.page.locator(PartnerFormSelectors.CONTACT_INPUT).fill(name)

    def fill_description(self, text: str) -> None:
        self.page.locator(PartnerFormSelectors.DESCRIPTION_INPUT).fill(text)

    def upload_logo(self) -> None:
        logo_path = os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "test_logo.png"
        )
        self.page.locator(PartnerFormSelectors.UPLOAD_INPUT).set_input_files(
            os.path.abspath(logo_path),
            force=True
        )

    def submit(self) -> None:
        self.page.locator(PartnerFormSelectors.SAVE_BUTTON).click()

    def wait_for_modal_close(self) -> None:
        expect(
            self.page.locator(PartnerFormSelectors.MODAL_WRAPPER)
        ).to_be_hidden(timeout=10000)